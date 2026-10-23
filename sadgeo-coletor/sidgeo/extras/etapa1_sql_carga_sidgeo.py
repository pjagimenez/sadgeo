# -*- coding: utf-8 -*-
"""
Created on Mon May  5 17:40:35 2025

@author: paulo.gimenez
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass

import pandas as pd

from sidgeo.domain.registro import Registro
from sidgeo.domain.registro_metadados import CAMPOS_OBRIGATORIOS
from sidgeo.infra.sqlplus_runner import ExecutorSQLPlus
from sidgeo.util.strings import detectar_encoding, truncar
from sidgeo.util.parsing import bool_to_str, parse_coordinate, parse_data
from sidgeo.util.sql_formatador import tratar_texto_sql

@dataclass
class Produtor:
    """ Classe de Tipo de dados Produtor """

    def __init__(self, cidade, estado, uf_anotador, uorg_anotador, protocolo_homolog):
        self.cidade = cidade
        self.estado = estado
        self.uf_anotador = uf_anotador
        self.uorg_anotador = uorg_anotador
        #dat_critica, 
        #self.dat_critica = dat_critica
        self.protocolo_homolog = protocolo_homolog

    def __str__(self):
        return f"Produtor(cidade={self.cidade}, estado={self.estado},\
            uf_anotador={self.uf_anotador}, uorg_anotador={self.uorg_anotador},\
            protocolo_homolog={self.protocolo_homolog})"


# pylint: disable=R0903


class ProcessarSIDGEO:
    """ Classe para Processar o conteudo do SIDGEO arquivo """

    def __init__(self, caminho_csv: str, produtor) -> None:
        self.caminho_csv = caminho_csv
        self.encoding = None
        self.registros = []
        self.erros_carga = []
        self.produtor = produtor


    @staticmethod
    def validar_registro(row: dict) -> list:
        """Retorna lista de campos obrigatórios ausentes"""
        faltantes = []
        for campo in CAMPOS_OBRIGATORIOS:
            if pd.isna(row.get(campo, '')) or str(row.get(campo)).strip() == '':
                faltantes.append(f"{campo} ({CAMPOS_OBRIGATORIOS[campo]})")
        return faltantes


    @staticmethod
    def gerar_bloco_plsql(registro: Registro, produtor: Produtor) -> str:
        """  Gerar a linha de comando SQL para processamento ja com os dados """
        # 06 = datum vertical
        # 2 = status registro SADGEO (1a critica)
        # 22
        lat_seg_dec = parse_coordinate(registro.lat_seg)
        lon_seg_dec = parse_coordinate(registro.lon_seg)

        # extrai só os 2 dígitos da situação
        situacao = str(registro.situacao)
        situacao_code = (situacao or '')[:2]

        ocup_gps = bool_to_str(registro.is_ocup_gps)
        ocup_mira = bool_to_str(registro.is_ocup_mira)
        ocup_grav = bool_to_str(registro.is_ocup_gravimetro)

        data_levantamento = parse_data(registro.data_levantamento)
        if data_levantamento is None:
            raise ValueError(
                f"Data de levantamento inválida para "
                f"{registro.cod_estacao}: {registro.data_levantamento!r}"
            )
        dat_levant = data_levantamento.strftime("%d/%m/%Y")

        dat_critica = parse_data(registro.data_critica).strftime("%d/%m/%Y")
        
        descr = tratar_texto_sql(registro.descricao)

        localizacao = tratar_texto_sql(registro.localizacao)
        itiner  = tratar_texto_sql(registro.itinerario)
        obs = tratar_texto_sql(registro.observacao)

        return f"""
            BEGIN
                DBMS_OUTPUT.PUT_LINE('Registro analise: {registro.cod_estacao}');

                 BDG_VALIDA.PCKG_SADGEO_PUT.CARREGA_ARQ_SIDGEO_3(
                    '{registro.cod_estacao}', '{registro.municipio}', '{registro.uf}', {descr}, '{registro.tipo_local}',
                    '{registro.monumentacao}', '{ocup_gps}', '{ocup_grav}', '{ocup_mira}', '{registro.inscr_chapa}',
                    '{registro.lat_sinal}', {registro.lat_grau}, {registro.lat_min}, {lat_seg_dec}, {registro.lon_grau}, {registro.lon_min}, {lon_seg_dec}, '06',
                    {localizacao}, {itiner}, {obs},
                    '{dat_levant}', '',
                    '{registro.informante}', '{registro.siape}', '{produtor.uf_anotador}', '{produtor.uorg_anotador}', null,
                    '{registro.projeto}', '{registro.campanha}', '{situacao_code}', '{registro.tipo_conexao}',
                    '{registro.conexao}', '{registro.caderneta}', '{registro.linha}', '{registro.rn_anterior}', 22,
                    '{registro.projeto}', '2', '{registro.informante}', '{registro.nue}'
                );


                update bdg_valida.t_sadgeo set dat_critica = TO_DATE('{dat_critica}','DD/MM/YYYY') , 
                        protocolo_homolog ='{produtor.protocolo_homolog}'
                    where dat_fim_levantamento = TO_DATE('{dat_levant}','DD/MM/YYYY')
                    and cod_estacao = '{registro.cod_estacao}';

                DBMS_OUTPUT.PUT_LINE('Registro inserido: {registro.cod_estacao}');
            EXCEPTION
                WHEN OTHERS THEN
                    DBMS_OUTPUT.PUT_LINE('Erro ao inserir {registro.cod_estacao}: ' || SQLERRM);
            END;
        """

    # pylint: disable=W0703
    def _carregar(self) -> None:
        """ Realiza a carga em memoria dos dados do arquivo SIDGEO """
        self.encoding = detectar_encoding(self.caminho_csv)
        df = pd.read_csv(self.caminho_csv, delimiter=';', encoding=self.encoding).fillna('')
        registros_validos = []
        erros = []

        for index, row in df.iterrows():
            row_dict = row.to_dict()

            # Validação de campos obrigatórios
            campos_faltando = ProcessarSIDGEO.validar_registro(row_dict)
            if campos_faltando:
                erros.append((row_dict.get('cod_estacao', f'Linha {index+2}'), campos_faltando))
                continue

            try:
                
                #Não existe 'T', que na verdade é 'M'
                tmonumentacao = 'M' if row_dict.get('monumentacao') == 'T' else row_dict.get('monumentacao')


                if row_dict.get('lat_sinal') == 'S':
                    lat_sinal = '-'
                else:
                    lat_sinal = '+'
                    
                if row_dict.get('lon_sinal') == 'W':
                    long_sinal = '-'
                else:
                    long_sinal = '+'
    
                reg = Registro(
                    versao_app= row_dict.get('versao_app'),                    
                    cod_estacao=row_dict.get('cod_estacao'),
                    monumentacao=tmonumentacao,
                    tipo_local=truncar(row_dict.get('tipo_local'), 2),
                    inscr_chapa=row_dict.get('inscr_chapa'),
                    situacao=row_dict.get('situacao'),
                    conexao=row_dict.get('conexao'),
                    tipo_conexao=row_dict.get('tipo_conexao'),
                    rn_anterior=row_dict.get('rn_anterior'),
                    campanha=row_dict.get('campanha').split('-', 1)[0].strip(),
                    data_levantamento=row_dict.get('data_levantamento'),
                    data_critica=row_dict.get('data_critica'),
                    projeto=truncar(row_dict.get('projeto'), 8),
                    nue=truncar(row_dict.get('nue'), 8),
                    linha=row_dict.get('linha'),
                    caderneta=row_dict.get('caderneta'),
                    informante=row_dict.get('informante'),
                    siape=row_dict.get('siape'),
                    tipo_fonte_coord=row_dict.get('tipo_fonte_coord'),
                    lat_sinal=lat_sinal,
                    lat_grau=int(row_dict.get('lat_grau', 0)),
                    lat_min=int(row_dict.get('lat_min', 0)),
                    lat_seg=float(parse_coordinate(row_dict.get('lat_seg', 0))),
                    lon_sinal=long_sinal,
                    lon_grau=int(row_dict.get('lon_grau', 0)),
                    lon_min=int(row_dict.get('lon_min', 0)),
                    lon_seg=float(parse_coordinate(row_dict.get('lon_seg', 0))),
                    is_atualizar_coord=row_dict.get('is_atualizar_coord'),
                    is_ocup_gps=row_dict.get('is_ocup_gps'),
                    is_ocup_mira=row_dict.get('is_ocup_mira'),
                    is_ocup_gravimetro=row_dict.get('is_ocup_gravimetro'),
                    descricao=row_dict.get('descricao'),
                    localizacao=row_dict.get('localizacao'),
                    itinerario=row_dict.get('itinerario'),
                    observacao=row_dict.get('observacao'),
                    seq=row_dict.get('seq', ''),
                    status_vrf=row_dict.get('status_vrf', ''),
                    municipio=row_dict.get('municipio',''),
                    uf=row_dict.get('uf',''),
                )
                registros_validos.append(reg)
            except Exception as e:
                print(f"DEBUG index: {index} ({type(index)})")
                erros.append((row_dict.get('cod_estacao', f'Linha {index+2}'), [str(e)]))


        self.registros = registros_validos
        self.erros_carga = erros


    def _gerar_sql(self) -> None:
        """ Gera o arquivo SQL com os comandos e dados para processamento """

        directory, filename = os.path.split(self.caminho_csv)
        filename_without_ext = os.path.splitext(filename)[0]

        saida_sql = os.path.join(directory, f'{filename_without_ext}.sql')

        with open(saida_sql, 'w', encoding=self.encoding) as f:
            f.write("set SERVEROUTPUT ON\n")
            f.write("BEGIN\n")
            f.write("    DBMS_OUTPUT.PUT_LINE('Inicio...');\n\n")
            for reg in self.registros:
                f.write(ProcessarSIDGEO.gerar_bloco_plsql(reg, self.produtor))
                f.write("\n")
            f.write("END;\n/\n")
             # Define the output SQL path

        return saida_sql

    def executar(self, toSQL: bool = True):
        """ Processa o arquivo carregando os dados em memoria, e se solicitado, grava no BD """
        self._carregar()
        if toSQL:
            saida_sql = self._gerar_sql()
        return len(self.registros), self.erros_carga, saida_sql


# pylint: disable=W0703
def main() -> None:

    '''
        -- Entrada de Argumentos para Processamento
    '''

    print("\nA seguir entre as informaões para processamento\n")
    caminho_csv = input("Arquivo SIDGEO (caminho completo): ")
    v_uf = input("UF do Produtor: ")
    v_cidade = input("Cidade do Produtor: ")
    v_uorganot = input("UORG Anotador:")
    #v_dat_critica = input("Data da Critica DD/MM/YYYY:")
    v_homologacao = input("Protoc Homologação:")

    # Solicita a string de conexão ao usuário
    conn_str = input("\tDigite a string de conexão (usuario/senha@bd): ").strip()


    produtor = Produtor(cidade=v_cidade, estado=v_uf, uf_anotador=v_uf, uorg_anotador=v_uorganot,                        
                         protocolo_homolog = v_homologacao,
                        )
    #dat_critica =v_dat_critica,
    try:

        # Processar o Arquivo SIDGEO
        proc_sidgeo = ProcessarSIDGEO(caminho_csv, produtor)

        qtd_reg, erros, saida_sql = proc_sidgeo.executar()
        if erros:
            print(f"\n\t X {len(erros)} registros com erro:")
            for cod, campos in erros:
                print(f"\t\t  - {cod}: campos ausentes ou inválidos -> {', '.join(campos)}")

            print("\t .:. Acerte os problemas antes de continuar. Encerrando execução...")
            sys.exit()
        else:
            print(f"\n\t V {qtd_reg} registro(s) RRNN pronto para carregar SADGEO.")
            print(" ")

            # Processa atualização BD SADGEO com SqlPlus
            proc_sqlplus = ExecutorSQLPlus(saida_sql, conn_str)
            proc_sqlplus.executar()

    except Exception as e:
        print(f"\n X Erro ao processar SIDGEO e carregar no BD SADGEO: {e}")



if __name__ == '__main__':
    main()
    