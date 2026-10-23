# -*- coding: utf-8 -*-
"""
Created on Mon May  5 17:40:35 2025

@author: paulo.gimenez
"""

from __future__ import annotations

import os
import sys

import pandas as pd

from sidgeo.domain.registro import Registro, campos_obrigatorios
from sidgeo.infra.sqlplus_runner import ExecutorSQLPlus
from sidgeo.util.strings import detectar_encoding, UtilConversorDados


class ProcessarSIDGEO:
    """ Classe para Processar o conteudo do SIDGEO arquivo """

    def __init__(self, caminho_csv: str, nom_carga: str, levar_bdg: str, nm_usuario: str) -> None:
        self.caminho_csv = caminho_csv
        self.nome_carga = nom_carga
        self.encoding = None
        self.registros = []
        self.erros_carga = []
        self.levar_bdg = levar_bdg
        self.nm_usuario = nm_usuario

    def nvl_str(self, valor):
        if valor is None or valor == "":
            return "NULL"
    
        valor = str(valor)
    
        # 1. Escapar aspas simples (OBRIGATÓRIO)
        valor = valor.replace("'", "''")
    
        # 2. Evitar problema com &
        valor = valor.replace("&", "' || chr(38) || '")
    
        # 3. Evitar problema com :
        valor = valor.replace(":", "' || chr(58) || '")
    
        return f"'{valor}'"

    def is_empty(self, val):
        return val is None or str(val).strip() == ""

            
    def map_ok_coord(self, valor):
        if valor == 'S':
            return '2'  # inserir coordenada
        elif valor == 'N':
            return '1'  # manter coordenada
        return None

    def validar_registro(self, row: dict) -> list:
        """Retorna lista de campos obrigatórios ausentes"""
        faltantes = []
        for campo in campos_obrigatorios:
            if pd.isna(row.get(campo, '')) or str(row.get(campo)).strip() == '':
                faltantes.append(f"{campo} ({campos_obrigatorios[campo]})")
        return faltantes

    
    def gerar_bloco_plsql(self,registro: Registro) -> str:
    
        lat_seg = UtilConversorDados.parse_coordinate(registro.lat_seg)
        lon_seg = UtilConversorDados.parse_coordinate(registro.lon_seg)
    
        situacao_code = (str(registro.situacao) or '')[:2]
    
        ocup_gps = UtilConversorDados.bool_to_str(registro.is_ocup_gps)
        ocup_mira = UtilConversorDados.bool_to_str(registro.is_ocup_mira)
        ocup_grav = UtilConversorDados.bool_to_str(registro.is_ocup_gravimetro)
    
        dat_critica = UtilConversorDados.parse_date(registro.data_critica)
    
        ok_coord = self.map_ok_coord(registro.is_atualizar_coord)

        

        dat_levant = UtilConversorDados.parse_date(registro.data_levantamento)
        
        # Passar o andamento da análise
        #p_tipo  STATUS_VRF
        #1,2,3,4  3
        #5–11     2
        #outro    4
        
        bloco_bdg = ""

        if self.levar_bdg == "S":

            bloco_bdg = f"""
               
               /* -- Envia para BDG
                bdg_valida.PCKG_CARGA_ALTIMETRIA.P_SADGEO_ENVIAR_BDG(
                    p_nm_usuario => '{self.nm_usuario}',
                    P_SEQ_SADGEO => '{registro.seq}'
                );
                  \n */ """

        if not self.is_empty(registro.seq):
            sql = f"""
            UPDATE bdg_valida.t_sadgeo
               SET dat_critica = TO_DATE('{dat_critica}','DD/MM/YYYY'),
                   nom_arq = '{self.nome_carga}'
             WHERE seq = '{registro.seq}';
            """
        else:
            sql = f"""
            UPDATE bdg_valida.t_sadgeo t
               SET t.dat_critica = TO_DATE('{dat_critica}','DD/MM/YYYY')
             WHERE t.cod_estacao = '{registro.cod_estacao}'
               AND t.dat_fim_levantamento = TO_DATE('{registro.dat_fim_levantamento}','DD/MM/YYYY');
            """
            
    
        
        return f"""
    BEGIN
      BDG_VALIDA.PCKG_SADGEO_PUT.ATUALIZA_SADGEO_WEB2(
        p_tipo => {registro.status_vrf},
        p_seq => {self.nvl_str(registro.seq)},
        p_cod_estacao => {self.nvl_str(registro.cod_estacao)},
        p_dsc_estacao => {self.nvl_str(registro.descricao)},
        p_tipo_monumentacao => {self.nvl_str(registro.monumentacao)},
        p_tipo_local => {self.nvl_str(registro.tipo_local)},
        p_cod_situacao_marco_principal => {self.nvl_str(situacao_code)},
        p_dsc_localizacao => {self.nvl_str(registro.localizacao)},
        p_dsc_itinerario => {self.nvl_str(registro.itinerario)},
        p_dsc_observacao => {self.nvl_str(registro.observacao)},
        p_i_ocupacao_gps => {self.nvl_str(ocup_gps)},
        p_i_ocupacao_gravim => {self.nvl_str(ocup_grav)},
        p_i_ocupacao_nivel => {self.nvl_str(ocup_mira)},
        p_inscricao_chapa => {self.nvl_str(registro.inscr_chapa)},
        p_sinal_lat => {self.nvl_str(registro.lat_sinal)},
        p_grau_lat => '{registro.lat_grau}',
        p_min_lat => '{registro.lat_min}',
        p_seg_lat => '{lat_seg}',
        p_grau_lon => '{registro.lon_grau}',
        p_min_lon => '{registro.lon_min}',
        p_seg_lon => '{lon_seg}',
        p_datum => '06',
        p_irregularidades => NULL,
        p_nomenclat_conex => {self.nvl_str(registro.conexao)},
        p_tipo_conexao => {self.nvl_str(registro.tipo_conexao)},
        p_projeto => {self.nvl_str(registro.projeto)},
        p_caderneta => {self.nvl_str(registro.caderneta)},
        p_rn_anterior => {self.nvl_str(registro.rn_anterior)},
        p_linha => {self.nvl_str(registro.linha)},
        p_disp_ggc => 'S',
        p_disp_proj => 'S',
        p_dat_critica => TO_DATE('{dat_critica}','DD/MM/YYYY'),
        p_critico => '{registro.informante}',
        p_fonte => {self.nvl_str(registro.tipo_fonte_coord)},
        p_ok_coord => '{ok_coord}'
      );
    
    -- Atualiza data crítica antes de enviar
     {sql}
        
    {bloco_bdg}
END;

    """

    def map_ok_coord(self, valor):
        if not valor:
            return None
        valor = valor.strip().upper()

        if valor == 'S':
            return '2'
        elif valor == 'N':
            return '1'

        return None
    
    
    def gerar_bloco_sqlupdate(self,registro: Registro) -> str:
        """  Gerar a linha de comando SQL para processamento ja com os dados """
        # 06 = datum vertical
        # 2 = status registro SADGEO (1a critica)
        # 22
        lat_seg_dec = UtilConversorDados.parse_coordinate(registro.lat_seg)
        lon_seg_dec = UtilConversorDados.parse_coordinate(registro.lon_seg)

        # extrai só os 2 dígitos da situação
        situacao = str(registro.situacao)
        situacao_code = (situacao or '')[:2]

        ocup_gps = UtilConversorDados.bool_to_str(registro.is_ocup_gps)
        ocup_mira = UtilConversorDados.bool_to_str(registro.is_ocup_mira)
        ocup_grav = UtilConversorDados.bool_to_str(registro.is_ocup_gravimetro)

        dat_levant = UtilConversorDados.parse_date(registro.data_levantamento)
        
        dat_critica = UtilConversorDados.parse_date(registro.data_critica)

        descr = self.nvl_str(UtilConversorDados.tratar_texto_sql(registro.descricao))

        localizacao = self.nvl_str(UtilConversorDados.tratar_texto_sql(registro.localizacao))
        itiner  = self.nvl_str(UtilConversorDados.tratar_texto_sql(registro.itinerario))
        obs = self.nvl_str(UtilConversorDados.tratar_texto_sql(registro.observacao))

        return f"""
            BEGIN
            DBMS_OUTPUT.PUT_LINE('Atualizando registro: ' || '{registro.cod_estacao}');
        
            UPDATE bdg_valida.t_sadgeo
               SET status_vrg = {registro.status_vrf},
                   municipio                  = '{registro.municipio}',
                   uf                         = '{registro.uf}',
                   tipo_local                 = '{registro.tipo_local}',
                   dsc_estacao                = {descr},
                   tipo_monumentacao          = '{registro.monumentacao}',
                   i_ocupacao_gps             = '{ocup_gps}',
                   i_ocupacao_gravimetro      = '{ocup_grav}',
                   i_ocupacao_nivel           = '{ocup_mira}',
                   inscricao_chapa            = '{registro.inscr_chapa}',
                   sinal_lat                  = '{registro.lat_sinal}',
                   grau_lat                   = {registro.lat_grau},
                   min_lat                    = {registro.lat_min},
                   seg_lat                    = {lat_seg_dec},
                   sinal_lon                  = '{registro.lon_sinal}',
                   grau_lon                   = {registro.lon_grau},
                   min_lon                    = {registro.lon_min},
                   seg_lon                    = {lon_seg_dec},
                   cod_fonte_coord            = '{registro.tipo_fonte_coord}',
                   datum                      = nvl(datum,'06'),
                   dsc_localizacao            = {localizacao},
                   dsc_itinerario             = {itiner},
                   dsc_observacao             = {obs},
                   dat_fim_levantamento       = TO_DATE('{dat_levant}','DD/MM/YYYY'),
                   anotador                   = '{registro.informante}',
                   siape_anotador             = '{registro.siape}',
                   projeto                    = '{registro.projeto}',
                   nom_arq                    = '{self.nome_carga}';
                   etapa_pta                  = '{registro.nue}',
                   campanha                   = '{registro.campanha}',
                   cod_situacao_marco_principal = '{situacao_code}',
                   tipo_conexao               = '{registro.tipo_conexao}',
                   nomenclat_conex            = '{registro.conexao}',
                   caderneta                  = '{registro.caderneta}',
                   linha                      = '{registro.linha}',
                   rn_anterior                = '{registro.rn_anterior}',
                   dat_critica                = TO_DATE('{dat_critica}','DD/MM/YYYY')
             WHERE seq = '{registro.seq}' and cod_estacao   = '{registro.cod_estacao}';
        
            DBMS_OUTPUT.PUT_LINE('Registro atualizado: ' || '{registro.cod_estacao}');
        EXCEPTION
            WHEN OTHERS THEN
                DBMS_OUTPUT.PUT_LINE('Erro ao atualizar {registro.cod_estacao}: ' || SQLERRM);
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
            try:
                
                #Não existe 'T', que na verdade é 'M'
                tmonumentacao = 'M' if row_dict.get('monumentacao') == 'T' else row_dict.get('monumentacao')

                reg = Registro(
                    versao_app= row_dict.get('versao_app'),                    
                    cod_estacao=row_dict.get('cod_estacao'),
                    monumentacao=tmonumentacao,
                    tipo_local=UtilConversorDados.truncar(row_dict.get('tipo_local'), 2),
                    inscr_chapa=row_dict.get('inscr_chapa'),
                    situacao=row_dict.get('situacao'),
                    conexao=row_dict.get('conexao'),
                    tipo_conexao=row_dict.get('tipo_conexao'),
                    rn_anterior=row_dict.get('rn_anterior'),
                    campanha=row_dict.get('campanha').split('-', 1)[0].strip(),
                    data_levantamento=row_dict.get('data_levantamento'),
                    data_critica=row_dict.get('data_critica'),
                    projeto=UtilConversorDados.truncar(row_dict.get('projeto'), 8),
                    nue=UtilConversorDados.truncar(row_dict.get('nue'), 8),
                    linha=row_dict.get('linha'),
                    caderneta=row_dict.get('caderneta'),
                    informante=row_dict.get('informante'),
                    siape=row_dict.get('siape'),
                    tipo_fonte_coord=row_dict.get('tipo_fonte_coord'),
                    lat_sinal=row_dict.get('lat_sinal'),
                    lat_grau=int(row_dict.get('lat_grau', 0)),
                    lat_min=int(row_dict.get('lat_min', 0)),
                    lat_seg=float(UtilConversorDados.parse_coordinate(row_dict.get('lat_seg', 0))),
                    lon_sinal=row_dict.get('lon_sinal'),
                    lon_grau=int(row_dict.get('lon_grau', 0)),
                    lon_min=int(row_dict.get('lon_min', 0)),
                    lon_seg=float(UtilConversorDados.parse_coordinate(row_dict.get('lon_seg', 0))),
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
            f.write("set DEFINE OFF\n")
            f.write("ALTER SESSION SET NLS_NUMERIC_CHARACTERS = '.,';\n")
            f.write("BEGIN\n")
            f.write("    DBMS_OUTPUT.PUT_LINE('Inicio...');\n\n")
            for reg in self.registros:
                f.write(self.gerar_bloco_plsql(reg))
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
    print("\nA seguir entre as informações para processamento\n")
    caminho_csv = input("Arquivo SIDGEO (caminho completo): ")

    
    levar_bdg = input("Levar para BDG? (S/N): ").strip().upper()
    nm_usuario = None
    nom_carga = ""
    
    if levar_bdg == "S":
        nm_usuario = input("Nome do usuário BDG: ").strip()
        # Solicita o rotulo/nome da carga
        nom_carga = input("\tDigite o nome (ateh 55char) desta carga )): ").strip()


    # Solicita a string de conexão ao usuário
    conn_str = input("\tDigite a string de conexão (usuario/senha@bd): ").strip()

    try:

        # Processar o Arquivo SIDGEO
        proc_sidgeo = ProcessarSIDGEO(caminho_csv,nom_carga, levar_bdg, nm_usuario)


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
    