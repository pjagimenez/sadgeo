# -*- coding: utf-8 -*-
"""
Created on Tue May 13 15:48:38 2025

@author: paulo.gimenez
"""

from __future__ import annotations

import os
import re
import sys

from sidgeo.util.strings import detectar_encoding
from sidgeo.infra.sqlplus_runner import ExecutorSQLPlus


class ProcessarBDADOSSIR:
    """ Classe para Processar o conteudo do B_DADOS.SIR arquivo """

    def __init__(self, caminho_arquivo_sir: str):
        self.b_dados_sir = caminho_arquivo_sir
                

    def _parse_geodetic_data(self, file_content):
        lines = file_content.split('\n')
        
        projeto = ''
        data_calculo = ''
        
        for line in lines:
            if 'PROJETO' in line:
                projeto = line.split('PROJETO')[-1].strip()
            if 'DATA DE CALCULO' in line:
                data_calculo = line.split('DATA DE CALCULO')[-1].strip()
        
        dash_line_index = next(i for i, line in enumerate(lines) if '---' in line)
        data_lines = lines[dash_line_index + 1:]
    
        inicio_dados = False
        for line in data_lines:
            if '-----------------------------------' in line:
                inicio_dados  = True
                continue
            if inicio_dados and line.strip():
                data_lines.append(line.strip())
                
        
        records = []
        for line in data_lines:
            # Quebra por dois ou mais espaços
            tokens = line.strip().split()
            
            if len(tokens) >= 11:
                records.append({
                    'identifier': tokens[0],
                    
                    'latitude_d': tokens[1],
                    'latitude_g': tokens[2],
                    'latitude_m': tokens[3],
                    'latitude_s': tokens[4],
                    #'latitude': " ".join(tokens[1:5]),                    
                    'lat_deviation': re.sub(r'[^0-9\.]', '', tokens[5]),
                    #'longitude': " ".join(tokens[6:10]),
                                        'longitude_d': tokens[6],
                    'longitude_g': tokens[7],
                    'longitude_m': tokens[8],
                    'longitude_s': tokens[9],
                    'lon_deviation': re.sub(r'[^0-9\.]', '', tokens[10]),
                    'ortometric_altitude': re.sub(r'[^0-9\.]', '', tokens[11]),
                    'geoidal_undulation': tokens[12],
                    'geometric_altitude': tokens[13],
                    'alt_deviation':  re.sub(r'[^0-9\.]', '', tokens[14]),
                    'measurement_date': tokens[15],
                    'project': projeto,    #tokens[16],
                    'calculated_date': data_calculo
                    })
        return records


    def transformaSignalLAT(self, valor):
        v = valor.upper()
        if v == 'S':
            return '-'
        elif v == 'N':
            return '+'
        else:
            return valor



    def _generate_sql_commands(self, records) -> str:
        sql_commands = []
        """
        O record['measurement_date'] naturalmente é o DAT_FIM_LEVANTAMENTO
        """
        for record in records:
            signal_lat = self.transformaSignalLAT(record['latitude_d'])
            
            sql = f"""
            update bdg_valida.t_sadgeo set dat_critica = to_date('{record['calculated_date']}','DD/MM/YYYY'), 
                status_vrf =3, ok_coord=2, disponivel_proj='S',
                sinal_lat = '{signal_lat}',
                grau_lat = {record['latitude_g']},
                min_lat = {record['latitude_m']},
                seg_lat =  {record['latitude_s']},                
                grau_lon = {record['longitude_g']},
                min_lon = {record['longitude_m']},
                seg_lon =  {record['longitude_s']},                
                arqsir_carregado = 'S', arqsir_filename = 'b_dados.sir', 
                arqsir_dat_calculo = to_date('{record['measurement_date']}','DD/MM/YYYY'), 
                sigma_lat = {record['lat_deviation']}, sigma_lon= {record['lon_deviation']}, 
                arqsir_val_altitude_geo= {record['geometric_altitude']}, arqsir_sigma_altitude={record['alt_deviation']}
              where cod_estacao =  '{record['identifier']}'
                and dat_fim_levantamento = to_date('{record['measurement_date']}','DD/MM/YYYY');
             commit;
                   """
            sql_commands.append(sql.strip())
        
        return sql_commands
     
 
    def executar(self) -> int : 
        # Extract the directory and filename without extension
        directory, filename = os.path.split(self.b_dados_sir)
        filename_without_ext = os.path.splitext(filename)[0]
           
        # Define the output SQL path
        arq_comando_sql = os.path.join(directory, f'{filename_without_ext}.sql')
        
        self.encoding = detectar_encoding(self.b_dados_sir)
        
        with open(self.b_dados_sir, 'r', encoding=self.encoding) as f:
            content = f.read()
    
            # Processamento e geraÃ§Ã£o dos comandos SQL
            records = self._parse_geodetic_data(content)
            sql_commands = self._generate_sql_commands(records)
     
            # Salvando em arquivo
            with open(arq_comando_sql, 'w') as f:
                f.write('\n'.join(sql_commands))
    
            return len(records), arq_comando_sql
        return -1, arq_comando_sql
        
    
# pylint: disable=W0703
def main() -> None:

    '''
        -- Entrada de Argumentos para Processamento
    '''         
    # Leitura do arquivo
    print("\nA seguir entre as informaões para processamento\n")
    arquivo_sir = input("Arquivo B_DADOS.SIR verificado (caminho completo): ")       
       
    # Solicita a string de conexão ao usuário
    conn_str = input("Digite a string de conexão (usuario/senha@bd): ").strip()

    try:

        # Processar o Arquivo SIDGEO
        proc_bdadossir = ProcessarBDADOSSIR(arquivo_sir)

        qtd_reg, arq_cmd_sql = proc_bdadossir.executar()
        if qtd_reg > 0:
            print(f"\n\t V {qtd_reg} registro(s) RRNN pronto para carregar SADGEO.")
            print(" ")

            # Processa atualização BD SADGEO com SqlPlus
            proc_sqlplus = ExecutorSQLPlus(arq_cmd_sql, conn_str)
            proc_sqlplus.executar()

        else:
            print(f"\n\t X {len(qtd_reg)} registros processados!:")
            print("\t .:. Verifique e Acerte os problemas antes de continuar. Encerrando execução...")
            sys.exit()
        
           
    except Exception as e:
        print(f"\n X Erro ao processar SIDGEO e carregar no BD SADGEO: {e}")



if __name__ == '__main__':
    main()
    