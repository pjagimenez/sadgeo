# -*- coding: utf-8 -*-
#file imagem_diretorio_scanner.py

#!pip install pywin32 Pillow pandas requests openpyxl

import win32com.client

import os
import json
from pathlib import Path

import argparse

import pandas as pd
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from hashlib import file_digest
from datetime import datetime
import re
import unicodedata


from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE

from dataclasses import dataclass, asdict
from imagem_model import ( TImagem, TImagemEstacao, TImagemRepositorio)

# ========================================================
@dataclass(slots=True)
class TDadosGps:
    latitude: float | None = None
    longitude: float | None = None
    altitude: float | None = None

@dataclass(slots=True)
class TErroExtracao:
    campo: str
    erro: str  
    
    
class ArquivoImagemMetadadosExifExtrator:
    
    """
    Responsável por ler metadados do sistema de arquivos e EXIF (via Pillow)
    e construir um objeto ImagemMetadata totalmente preenchido.
    """

    def __init__(self):
        pass  
    
    def _obter_float(
        self,
        detalhes: dict,
        campo: str
    ) -> tuple[float | None, list[TErroExtracao]]:
    
        try:
    
            valor = detalhes.get(campo)
    
            if valor is None:
                return None, []
    
            # IFDRational
            try:
                return float(valor), []
            except Exception:
                pass
    
            # "300/1"
            if "/" in str(valor):
                num, den = str(valor).split("/")
                return float(num) / float(den), []
    
            return float(valor), []
    
        except Exception as e:
            return (
                None,
                [TErroExtracao(
                    campo=campo,
                    erro=str(e)
                )]
            )
    
    def _gps_to_float(self, v) -> float | None:
        try:
            if v is None:
                return None
        
            # tuple/list (numerador, denominador)
            if isinstance(v, (tuple, list)) and len(v) == 2:
                num, den = v
                
                if float(den) == 0:
                    return None
                
                return float(num) / float(den)
            
            # IFDRational e similares
            return float(v)
        
        except Exception:
            return None
        
    def _converter_gps(self, coordenada: tuple | list) -> float | None:
        if not coordenada:
            return None
        
        try:
            if len(coordenada) != 3:
                return None
            
            graus = self._gps_to_float(coordenada[0])
            minutos = self._gps_to_float(coordenada[1])
            segundos = self._gps_to_float(coordenada[2])
            
            if None in (graus, minutos, segundos):
                return None
            
            return graus + (minutos / 60) + (segundos / 3600)
        
        except Exception:
            return None
        

    def _obter_dados_gps(self, detalhes:dict) ->tuple[TDadosGps, list[TErroExtracao]] :
        """
        Recupera informações GPS do EXIF.
        Retorna:
            TDadosGps
            list[TErroExtracao]
        """
        erros: list[TErroExtracao] = []
        dados_gps = TDadosGps()        
        
        gps = detalhes.get("gps")    
        if not gps:
            return dados_gps, erros


        # Latitude
        try:
            latitude = gps.get("GPSLatitude")
            if latitude is not None:
                dados_gps.latitude = self._converter_gps(latitude)
                ref = str(gps.get("GPSLatitudeRef", "")).upper()
                if (dados_gps.latitude is not None and ref == "S"):
                    dados_gps.latitude *= -1
        except Exception as e:
            erros.append(TErroExtracao(campo="GPS_LATITUDE",erro=str(e)))
            
        # Longitude
        try:
            longitude = gps.get("GPSLongitude")
            if longitude is not None:
                dados_gps.longitude = self._converter_gps(longitude)
                ref = str(gps.get("GPSLongitudeRef", "")).upper()
                if (dados_gps.longitude is not None and ref == "W"):
                    dados_gps.longitude *= -1
        except Exception as e:
            erros.append(TErroExtracao(campo="GPS_LONGITUDE",erro=str(e)))    

        #Altitude
        try:
            altitude = gps.get("GPSAltitude")
            if altitude is not None:
                dados_gps.altitude = self._gps_to_float(altitude)
                ref = gps.get("GPSAltitudeRef", 0)
                if (dados_gps.altitude is not None and ref == 1):
                    dados_gps.altitude *= -1
                    
        except Exception as e:
            erros.append(TErroExtracao(campo="GPS_ALTITUDE",erro=str(e)))    

        return dados_gps, erros  

    def _obter_distancia_focal(self, detalhes:dict) -> tuple[str | None,  list[TErroExtracao]]:
         
        erros: list[TErroExtracao] = []
        distancia_focal = None
    
        try:
    
            distancia_focal = detalhes.get("FocalLength")
    
            if distancia_focal is not None:    
                distancia_focal = str(distancia_focal)
    
        except Exception as e:
            erros.append(TErroExtracao(campo="FocalLength",erro=str(e)))    

        return distancia_focal, erros            
    
    
    def _obter_data_captura(self, detalhes:dict) -> tuple[datetime | None,  list[TErroExtracao]]:
        
        erros: list[TErroExtracao] = []
        dt_captura = None

        try:
        
             valor_data = detalhes.get("DateTimeOriginal")
        
             if valor_data:
                 valor_data = self._limpar_texto_windows(valor_data)
                 dt_captura = datetime.strptime(valor_data,"%Y:%m:%d %H:%M:%S")
        
        except Exception as e:
            erros.append(TErroExtracao(campo="DateTimeOriginal",erro=str(e)))    

        return dt_captura, erros
              
    def _obter_texto(self, detalhes: dict, campo_exif: str) -> tuple[str | None, list[TErroExtracao]]:

        try:
            valor = detalhes.get(campo_exif)
            return (None if valor is None else str(valor),[])
        
        except Exception as e:
            return (None, [TErroExtracao(campo=campo_exif,erro=str(e))])
    
        
    def _obter_dados_brutos_exif(self, imagem) -> tuple[dict, str, list[TErroExtracao]]:
    
        erros: list[TErroExtracao] = []
        detalhes: dict = {}
    
        try:
    
            #TODO usar getexif() mas ver problemas com GPS se existem
            exif = imagem._getexif()
    
            if not exif:
                return detalhes, json.dumps({}), erros
    
            for tag_id, valor in exif.items():
    
                tag = TAGS.get(tag_id, tag_id)
    
                if tag == "GPSInfo":
    
                    gps = {}
    
                    for gps_tag_id, gps_valor in valor.items():
    
                        gps_tag = GPSTAGS.get(
                            gps_tag_id,
                            gps_tag_id
                        )
    
                        gps[gps_tag] = gps_valor
    
                    detalhes["gps"] = gps
    
                else:
    
                    detalhes[tag] = valor
    
        except Exception as e:
    
            erros.append(
                TErroExtracao(
                campo= "_obter_exif",
                erro= str(e)
                )
            )
    
        raw_exif = json.dumps(detalhes,default=str,ensure_ascii=False)
    
        return detalhes, raw_exif, erros


    def sanitizar_texto(self, texto):
    
        if texto is None:
            return None
    
        return re.sub(
            r"[\x00-\x08\x0B\x0C\x0E-\x1F]",
            "",
            str(texto)
        )
    
    def extrair(self, arquivo)-> tuple[TImagem, TImagemRepositorio] :
        
        metadados = TImagem(uuid_imagem=None, 
                            tx_hash=None, 
                            dt_hash=None)
        
        memoria = TImagemRepositorio(id_imagem_repositorio=None, 
                                     uuid_imagem=None, 
                                     id_repositorio=None, 
                                     nm_arquivo=None)
        
        todos_erros : list[TErroExtracao] = []
        
        try:   
            memoria.nm_arquivo = arquivo.name
            
            # Image Open    
            with Image.open(arquivo) as img:     
                
                largura, altura = img.size
                dpi = img.info.get("dpi")
                
                metadados.nr_largura_imagem =largura
                metadados.nr_altura_imagem = altura
                metadados.tx_dpi =  (    str(dpi)    if dpi is not None    else None)                
              
                # Usando mecanismo EXIF/Pillow
                dados_exif,raw_exif, erros_exif = (
                    self._obter_dados_brutos_exif(img)
                )
                
                #Dados brutos (dump) e erros eventuais
                memoria.tx_metadados_dump = self.sanitizar_texto(raw_exif)
                
                todos_erros.extend(erros_exif)
                
                if dados_exif:                       
        
                    # Dados GPS            
                    dados_gps, erros = self._obter_dados_gps(dados_exif)
                    metadados.gps_latitude = dados_gps.latitude
                    metadados.gps_longitude = dados_gps.longitude
                    metadados.gps_altitude = dados_gps.altitude
                    todos_erros.extend(erros)
                                                    
                    #Dados Distância focal
                    distancia_focal, erros = self._obter_distancia_focal(dados_exif)
                    metadados.tx_distancia_focal = distancia_focal
                    todos_erros.extend(erros)                       
           
                    #Data de captura da imagem                
                    dt_captura, erros = self._obter_data_captura(dados_exif)
                    metadados.dt_captura_imagem_original = dt_captura
                    todos_erros.extend(erros)
                    
                    # Dados negócio
                    fabricante, erros = self._obter_texto(dados_exif, "Make")
                    metadados.tx_fabricante_dispositivo = fabricante
                    todos_erros.extend(erros)      
                    
                    modelo, erros = self._obter_texto(dados_exif, "Model")
                    metadados.tx_modelo_dispositivo = modelo
                    todos_erros.extend(erros)
                    
                    iso, erros = self._obter_texto(dados_exif, "ISOSpeedRatings")
                    metadados.tx_iso_imagem = iso
                    todos_erros.extend(erros)
                    
                    abertura, erros = self._obter_texto(dados_exif, "FNumber")
                    metadados.tx_abertura_imagem = abertura
                    todos_erros.extend(erros)
                    
                    tempo_exposicao, erros = self._obter_texto(dados_exif,"ExposureTime") 
                    metadados.tx_tempo_exposicao = tempo_exposicao
                    todos_erros.extend(erros)
                              
                    resolucao_horizontal, erros = self._obter_float(dados_exif,"XResolution")
                    metadados.nr_resolucao_horizontal = resolucao_horizontal
                    todos_erros.extend(erros)
                        
                    resolucao_vertical, erros = self._obter_float(dados_exif,"YResolution")
                    metadados.nr_resolucao_vertical = resolucao_vertical
                    todos_erros.extend(erros)
                    
        except Exception as e:
            todos_erros.append(TErroExtracao(campo="IMG",erro=str(e)))

        finally:
            memoria.tx_erros_dump = self.sanitizar_texto(json.dumps([asdict(e) for e in todos_erros],ensure_ascii=False))

        return metadados, memoria
    
  

class ArquivoImagemMetadadosWindowsExtractor:
        
    def __init__(self):
        pass   
    
    @staticmethod
    def _limpar_texto_windows(cls, valor: str) -> str:
        if not valor:
            return valor
    
        return "".join(
            c for c in valor
            if unicodedata.category(c) != "Cf"
        ).strip()
       
    def _obter_dicionario_bruto_windows(self, folder, nome_arquivo) -> tuple[dict, str, list[TErroExtracao]]:
    
        erros: list[TErroExtracao] = []
        detalhes: dict = {}
        
        arquivo = folder.ParseName(nome_arquivo)
        if arquivo is None:
            erros.append(TErroExtracao(campo="ARQUIVO",erro=f"Arquivo não encontrado: {nome_arquivo}"))
            return {}, "{}", erros
            
        detalhes = {}
        
        for i in range(400):
            try:
                campo = folder.GetDetailsOf(None, i)
                valor = folder.GetDetailsOf(arquivo, i)
                if campo:
                    campo = str(campo).strip()
                if valor:
                    valor = str(valor).strip()
                if campo and valor:
                    #print(f"{nome}: {valor}")
                    detalhes[campo] = valor
            except Exception as e:
                erros.append(TErroExtracao(campo=f"WINDOWS_PROPERTY_{i}",erro=str(e)))
            
        raw_windows = json.dumps(detalhes,default=str,ensure_ascii=False)
        return detalhes, raw_windows, erros
    
   
    def _obter_texto_windows(
        self,
        detalhes: dict,
        campo_windows: str
    ) -> tuple[str | None, list[TErroExtracao]]:
    
        try:
            valor = detalhes.get(campo_windows)
    
            if valor is None:
                return None, []
    
            return str(valor).strip(), []
    
        except Exception as e:
            return (
                None,
                [TErroExtracao(
                    campo=campo_windows,
                    erro=str(e)
                )]
            )

    def _obter_data_windows(
        self,
        detalhes: dict,
        campo_windows: str
        ) -> tuple[datetime | None, list[TErroExtracao]]:

        try:
            valor = detalhes.get(campo_windows)
            if not valor:
                return None, []

            texto = str(valor).strip()

            formatos = [
                "%d/%m/%Y %H:%M",
                "%d/%m/%Y %H:%M:%S",
                "%Y-%m-%d %H:%M:%S"
                ]

            for formato in formatos:
                try:
                    texto = self._limpar_texto_windows(texto)
                    return datetime.strptime(texto, formato), []
                except ValueError:
                    pass

            raise ValueError(f"Formato de data não reconhecido: {texto}" )

        except Exception as e:
            return (
                None,
                [TErroExtracao(
                    campo=campo_windows,
                    erro=str(e)
                    )]
                )

    def sanitizar_texto(self, texto):
    
        if texto is None:
            return None
    
        return re.sub(
            r"[\x00-\x08\x0B\x0C\x0E-\x1F]",
            "",
            str(texto)
        )

    def extrair(self, folder, nome_arquivo)-> tuple[TImagem, TImagemRepositorio] :
           
        metadados = TImagem(uuid_imagem=None, 
                             tx_hash=None, 
                             dt_hash=None)
         
        memoria = TImagemRepositorio(id_imagem_repositorio=None, 
                                      uuid_imagem=None, 
                                      id_repositorio=None, 
                                      nm_arquivo=None)
        
        todos_erros : list[TErroExtracao] = []
        
        try:   
            memoria.nm_arquivo = nome_arquivo
            
            dados_windows, raw_windows, erros = (
                       self._obter_dicionario_bruto_windows(folder, nome_arquivo) 
            )
               
                   
            #Dados brutos (dump) e erros eventuais
            memoria.tx_metadados_dump = self.sanitizar_texto(raw_windows)
            
            todos_erros.extend(erros)
            
            if dados_windows:                            
                
                fabricante, erros = self._obter_texto_windows(
                     dados_windows,
                     "Fabricante da câmera"
                 )
                metadados.tx_fabricante_dispositivo = fabricante
                todos_erros.extend(erros)
                
                modelo, erros = self._obter_texto_windows(
                    dados_windows,
                    "Modelo da câmera"
                )
                metadados.tx_modelo_dispositivo = modelo
                todos_erros.extend(erros)
                
                #data de captura 
                data_captura, erros = self._obter_data_windows(
                    dados_windows,
                    "Tirada Em"
                )
                metadados.dt_captura_imagem_original = data_captura
                todos_erros.extend(erros)
                
                iso, erros = self._obter_texto_windows(
                    dados_windows,
                    "Velocidade ISO"
                )
                metadados.tx_iso_imagem = iso
                todos_erros.extend(erros)
                
                abertura, erros = self._obter_texto_windows(
                    dados_windows,
                    "Escala de número f"
                )
                metadados.tx_abertura_imagem = abertura
                todos_erros.extend(erros)
                
                tempo, erros = self._obter_texto_windows(
                    dados_windows,
                    "Tempo de exposição"
                )
                metadados.tx_tempo_exposicao = tempo
                todos_erros.extend(erros)
                                
                distancia_focal, erros = self._obter_texto_windows(
                    dados_windows,
                    "Distância focal"
                )
                metadados.tx_distancia_focal = distancia_focal
                todos_erros.extend(erros)
                
                #Resolução Horiz
                res_h, erros = self._obter_texto_windows(
                        dados_windows,
                        "Resolução horizontal"
                )
                todos_erros.extend(erros)
                if res_h:
                    try:
                        valor_limpo = re.sub(
                                r"[^\d.,]", "", str(res_h)
                            ).replace(",", ".")                                                    
                        if valor_limpo:
                            metadados.nr_resolucao_horizontal = float(valor_limpo)
                    except Exception as e:
                        todos_erros.append(
                            TErroExtracao(
                                campo="Resolução horizontal",
                                erro=str(e)
                                )
                            )
                               
                #Resolução Vert
                res_v, erros = self._obter_texto_windows(
                        dados_windows,
                        "Resolução vertical"
                )
                todos_erros.extend(erros)
                if res_v:
                    try:
                        valor_limpo = re.sub(
                                r"[^\d.,]", "", str(res_h)
                            ).replace(",", ".")               
                        if valor_limpo:
                            metadados.nr_resolucao_vertical = float(valor_limpo)
                    except Exception as e:
                        todos_erros.append(
                            TErroExtracao(
                                campo="Resolução vertical",
                                erro=str(e)
                                )
                            )                        
                
                flash, erros = self._obter_texto_windows(
                    dados_windows,"Modo do flash"
                )
                metadados.tx_modo_flash = flash
                todos_erros.extend(erros)
                
                balanco_de_branco, erros = self._obter_texto_windows(
                    dados_windows,"Balanço de branco"
                )
                metadados.tx_balanco_de_branco = balanco_de_branco
                todos_erros.extend(erros)
                
                orientacao, erros = self._obter_texto_windows(
                    dados_windows,"Orientação"
                )
                metadados.tx_orientacao = orientacao
                todos_erros.extend(erros)               
               
        except Exception as e:
            todos_erros.append(TErroExtracao(campo="IMG",erro=str(e)))

        finally:
            memoria.tx_erros_dump = self.sanitizar_texto(json.dumps([asdict(e) for e in todos_erros],ensure_ascii=False))

        return metadados, memoria
        
      

class GeradorHashArquivo:
    def __init__(self):
        pass    
    
    def obter_sha256(self, caminho : str) -> dict:
        with open(caminho, "rb") as f:
            return {
                "hash": file_digest(f, "sha256").hexdigest(),
                "dt_hash": datetime.now()
                }

#==========================================================================

class ProcessarPastaImagens:
    
    def __init__(self):
        pass

    def _complementar_campos(self, destino, origem):
        
        #Campos já tratados, consolidados
        campos_ignorados = {
            "tx_metadados_dump",
            "tx_erros_dump"
        }
        
        for campo in origem.__dataclass_fields__:
            
            if campo in campos_ignorados:
                continue
        
            if not hasattr(destino, campo):
                continue
            
            valor_origem = getattr(origem, campo, None)
            valor_destino = getattr(destino, campo, None)
    
            if valor_destino is None and valor_origem is not None:
                setattr(destino, campo, valor_origem)
        
            
    def _consolidar_dump(self, repo_exif, repo_windows, atributo, 
                         valor_padrao=None):
    
        if valor_padrao is None:
            valor_padrao = {}
        
        resultado = {
            "exif": valor_padrao.copy(),
            "windows": valor_padrao.copy()
        }
    
        fontes = {
            "exif": repo_exif,
            "windows": repo_windows
        }
    
        for fonte, repositorio in fontes.items():
    
            if repositorio is None:
                continue
    
            valor = getattr(repositorio, atributo, None)
    
            if not valor:
                continue
    
            try:
                resultado[fonte] = json.loads(valor)
            except Exception:
                resultado[fonte] = {"_raw": valor}
    
        return json.dumps(
            resultado,
            default=str,
            ensure_ascii=False
        )
    
        
    def executar(self, qpasta):
        pasta = qpasta
        folder  = shell.Namespace(pasta)        
        
        if folder is None:
           raise RuntimeError(
               f"Windows Shell não conseguiu acessar a pasta: {pasta}"
               )

        idx = 0

        extratorExif : ArquivoImagemMetadadosExifExtrator = ArquivoImagemMetadadosExifExtrator()
    
        extratorWindows : ArquivoImagemMetadadosWindowsExtractor= ArquivoImagemMetadadosWindowsExtractor()
   
        geradorHash : GeradorHashArquivo = GeradorHashArquivo()
        
        registros : list[tuple[TImagem, TImagemRepositorio, dict]] = []        
        
        for arquivo in Path(pasta).glob("*"):
            try:
                if arquivo.suffix.lower() not in extensoes:
                    print(f"Arquivo {arquivo} não é no formato desejado")
                    continue
                
                #if idx >= 1000:
                #    break
                
                erro = {
                    "arquivo": arquivo.name,
                    "stat": None,
                    "exif": None,
                    "windet": None,
                    "hash": None,
                    "img": None
                }
                
                #Imagem consolidada que será a valida final
                imagem : TImagem = TImagem()
                imagemrepo : TImagemRepositorio = TImagemRepositorio()
    
                img_repo_exif = None
                img_repo_windows = None
                
                #stats arquivo
                try:
                    stat = arquivo.stat()
                    imagemrepo.dt_criacao_arquivo = datetime.fromtimestamp(stat.st_ctime) #.isoformat()
                    imagemrepo.dt_modificacao_arquivo = datetime.fromtimestamp(stat.st_mtime) #.isoformat()
                    imagemrepo.nm_arquivo = arquivo.name
                    imagem.nr_tamanho_arquivo = stat.st_size
                except Exception as e:
                    erro["stat"] = str(e)        
            
                #Imagem somente do EXIF
                try:
                    imagem_exif, img_repo_exif = extratorExif.extrair(arquivo)
                    self._complementar_campos(imagem, imagem_exif)
                    self._complementar_campos(imagemrepo, img_repo_exif)
                except Exception as e:
                    erro["exif"] = str(e)        
        
            
                try: #Imagem somente do Windows
                    imagem_windows, img_repo_windows = extratorWindows.extrair(folder, arquivo.name)
                    self._complementar_campos(imagem, imagem_windows)
                    self._complementar_campos(imagemrepo, img_repo_windows)
                except Exception as e:
                    erro["windet"] = str(e)        
                       
                # Consolida os metadados brutos das duas fontes
                try:
                    imagemrepo.tx_metadados_dump = self._consolidar_dump(
                        img_repo_exif,
                        img_repo_windows,
                        "tx_metadados_dump",
                        {}
                    )
                    
                    imagemrepo.tx_erros_dump = self._consolidar_dump(
                        img_repo_exif,
                        img_repo_windows,
                        "tx_erros_dump",
                        []
                    )
                                            
                except Exception as e:
                    erro["img"] = str(e)
                    
                    
                # SHA256
                try:
                    #Gerar o hash a partir do caminho e nome de arquivo completo    
                    info_hash = geradorHash.obter_sha256(arquivo)            
                    imagem.tx_hash = info_hash.get("hash")
                    imagem.dt_hash = info_hash.get("dt_hash")
                except Exception as e:
                    erro["hash"] = str(e)
            
                    
                if any ([erro["img"],erro["windet"],erro["hash"], erro["stat"] , erro["exif"]]):
                    print(f"PARCIAL {arquivo.name} \n\t {erro}")
                else:   
                    print(f"OK {arquivo.name}")
            
                registros.append((imagem, imagemrepo, erro))
                idx += 1
            except Exception as e:
                print(f"Erro em {arquivo.name}: {e}")
          
        return registros
    
#==========================================================================
def limpar_excel(valor):
    if isinstance(valor, str):
        return ILLEGAL_CHARACTERS_RE.sub(
            "",
            valor
            )

    return valor


shell = win32com.client.Dispatch("Shell.Application")

extensoes = (".jpg", ".jpeg", ".png")

parser = argparse.ArgumentParser()
parser.add_argument(
    "pasta",
    nargs="?",
    help="Caminho da pasta de imagens"
)

args = parser.parse_args()

if args.pasta:
    PASTA = args.pasta
else:
    PASTA = input("Informe a pasta onde estão as imagens: ")

print(f"Pasta: {PASTA}")

processador : ProcessarPastaImagens = ProcessarPastaImagens()

registros = processador.executar(qpasta = PASTA)


registros_df = []

for imagem, repositorio, erro in registros:
    registro = {}

    registro.update({
        f"imagem_{k}": v
        for k, v in asdict(imagem).items()
    })

    registro.update({
        f"repo_{k}": v
        for k, v in asdict(repositorio).items()
    })
    
    registro.update({
        f"erro_{k}": v
        for k, v in erro.items()
    })

    registros_df.append(registro)
    

df = pd.DataFrame(registros_df)

arquivo_excel = os.path.join(PASTA, "imagens.xlsx")
arquivo_json = os.path.join(PASTA, "imagens.json")

for coluna in df.columns:
    if df[coluna].dtype == "object":
        df[coluna] = df[coluna].apply(
            lambda x: float(x)
            if hasattr(x, "numerator") and hasattr(x, "denominator")
            else x
            )

for c in df.columns:
    tipos = df[c].dropna().map(type).unique()
    if len(tipos) > 1:
        print()
        print(c)
        print(tipos)


df.to_parquet(
    os.path.join(PASTA, "imagens.parquet"),
    index=False
)

df.to_json(
    arquivo_json,
    orient="records",
    indent=4,
    force_ascii=False
)

df = df.map(limpar_excel)

df.to_excel(arquivo_excel, index=False)

print()
print(f"Excel: {arquivo_excel}")
print(f"JSON : {arquivo_json}")
print(f"Total: {len(df)} arquivos")

