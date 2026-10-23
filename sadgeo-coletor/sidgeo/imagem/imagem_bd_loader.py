# -*- coding: utf-8 -*-
"""
file: /sidgeo/imagem/imagem_bd_loader.py
@created: 26-02-2025 pjag
@updated: 12-09-2025 pjag
"""

from datetime import datetime
import json
import pandas as pd
import math
from imagem_parser_nome import NomeArquivoParser
from imagem_oracle_utils import CampoOracle


class ImagemLoader:

    def __init__(self):

        self.truncados_metadados = 0
        self.truncados_erros = 0

    @staticmethod
    def carregar(arquivo):

        if arquivo.lower().endswith(".json"):
            return pd.read_json(arquivo)

        if arquivo.lower().endswith(".parquet"):
            return pd.read_parquet(arquivo)

        raise ValueError(
            "Formato não suportado"
        )

    @staticmethod
    def data(valor):
        if pd.isna(valor):
            return None
    
        # já é Timestamp do pandas
        if isinstance(valor, pd.Timestamp):
            return valor.to_pydatetime()
    
        # já é datetime
        if isinstance(valor, datetime):
            return valor
    
        # epoch em milissegundos
        if isinstance(valor, (int, float)):
            return datetime.fromtimestamp(valor / 1000)
    
        # string de data
        return pd.to_datetime(valor).to_pydatetime()


    def normalizar(self, valor):
        if isinstance(valor, float) and math.isnan(valor):
            return None
        return valor

    def limpar_exif(self, metadados_original):
    
        try:
    
            metadados = json.loads(
                metadados_original
            )
    
            texto = json.dumps(
                metadados,
                ensure_ascii=False
            )
    
            for lixo in (
                "\u200e",  # LEFT-TO-RIGHT MARK
                "\u200f",  # RIGHT-TO-LEFT MARK
                "\u202a",  # LEFT-TO-RIGHT EMBEDDING
                "\u202b",
                "\u202c",
                "\u202d",
                "\u202e",
                "¿"
            ):
                texto = texto.replace(
                    lixo,
                    ""
                )
    
            metadados = json.loads(texto)
    
            if (
                "exif" in metadados
                and isinstance(
                    metadados["exif"],
                    dict
                )
            ):
    
                metadados["exif"] = {
                    k: v
                    for k, v in metadados["exif"].items()
                    if not (
                        str(v).startswith("b'")
                        and "\\x" in str(v)
                    )
                }
    
            return json.dumps(
                metadados,
                ensure_ascii=False
            )
    
        except Exception:
    
            return metadados_original
        
        
    def transformar(
        self,
        df,
        id_base
    ):
        
        registros = []

        for _, row in df.iterrows():

            info = NomeArquivoParser.identificar(
                row["repo_nm_arquivo"]
            )

            metadados_original = row.get(
                "repo_tx_metadados_dump"
            )

            erros_original = row.get(
                "repo_tx_erros_dump"
            )

            if metadados_original is not None:
                metadados_original = self.limpar_exif(metadados_original)
                
                if len(str(metadados_original)) > 4000:
                    print("\n--- METADADOS GRANDES ---")
                    print(info.nome_arquivo_original)
                    print("Tamanho:", len(metadados_original))

                    dados = json.loads(metadados_original)
                    
                    if "exif" in dados:
    
                        for k, v in dados["exif"].items():
    
                            tamanho = len(str(v))
        
                            if tamanho > 100:
                                print(
                                info.nome_arquivo_original,
                                k,
                                tamanho
                                )

                    for secao, conteudo in dados.items():

                        tamanho = len(
                        json.dumps(
                        conteudo,
                        ensure_ascii=False
                        )
                        )

                        print(
                        secao,
                        tamanho
                        )
                    self.truncados_metadados += 1

            if erros_original is not None:
                if len(str(erros_original)) > 4000:
                    self.truncados_erros += 1

            registro = (
                
                    id_base,

                    info.nome_arquivo_original,
                    info.codigo_estacao,
                    info.tipo_imagem.value,

                    "S"
                    if info.origem_sadgeo
                    else "N",

                    row.get("imagem_tx_hash"),

                    self.data(
                        row.get("imagem_dt_hash")
                    ),

                    row.get(
                        "imagem_nr_tamanho_arquivo"
                    ),

                    row.get(
                        "imagem_nr_largura_imagem"
                    ),

                    row.get(
                        "imagem_nr_altura_imagem"
                    ),

                    row.get(
                        "imagem_tx_fabricante_dispositivo"
                    ),

                    row.get(
                        "imagem_tx_modelo_dispositivo"
                    ),

                    self.data(
                        row.get(
                            "imagem_dt_captura_imagem_original"
                        )
                    ),

                    row.get(
                        "imagem_tx_iso_imagem"
                    ),

                    row.get(
                        "imagem_tx_abertura_imagem"
                    ),

                    row.get(
                        "imagem_tx_tempo_exposicao"
                    ),

                    row.get(
                        "imagem_nr_resolucao_horizontal"
                    ),

                    row.get(
                        "imagem_nr_resolucao_vertical"
                    ),

                    row.get(
                        "imagem_gps_latitude"
                    ),

                    row.get(
                        "imagem_gps_longitude"
                    ),

                    row.get(
                        "imagem_gps_altitude"
                    ),

                    row.get(
                        "imagem_tx_dpi"
                    ),

                    row.get(
                        "imagem_tx_distancia_focal"
                    ),

                    self.data(
                        row.get(
                            "repo_dt_criacao_arquivo"
                        )
                    ),

                    self.data(
                        row.get(
                            "repo_dt_modificacao_arquivo"
                        )
                    ),

                    CampoOracle.varchar4000(
                        metadados_original,
                        "TX_METADADOS_DUMP"
                    ),

                    CampoOracle.varchar4000(
                        erros_original,
                        "TX_ERROS_DUMP"
                    )
                )
            
            registro = tuple(
                self.normalizar(v)
                    for v in registro
                )
            
            registros.append(registro)
            

        return registros