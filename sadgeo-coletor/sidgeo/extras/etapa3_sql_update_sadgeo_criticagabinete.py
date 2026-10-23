# -*- coding: utf-8 -*-

import pandas as pd
from pathlib import Path
import re
import oracledb

def nvl_ok_coord(valor):
    if pd.isna(valor):
        return None

    valor = str(valor).strip().upper()

    if valor == "S":
        return "2"

    if valor == "N":
        return "1"

    return None

def nvl_sinal_coord(valor):
    if pd.isna(valor):
        return None

    valor = str(valor).strip().upper()

    conversao = {
        "S": "-",
        "O": "-",
        "N": "+",
        "L": "+"
    }
    return conversao.get(valor, valor)

def nvl_str(valor):
    if pd.isna(valor):
        return None

    valor = str(valor).strip()

    if valor == "":
        return None

    return valor

def nvl_int(valor):
    if pd.isna(valor):
        return None
    if str(valor).strip() == "":
        return None
    return int(valor)


def nvl_float(valor):
    if pd.isna(valor):
        return None
    if str(valor).strip() == "":
        return None
    return float(valor)


def validar_dataframe(df):

    # SEQ obrigatório
    sem_seq = df[
        df["seq"].astype(str).str.strip() == ""
    ]

    if not sem_seq.empty:
        raise Exception(
            f"Existem {len(sem_seq)} registros sem SEQ."
        )

    # STATUS_VRF obrigatoriamente = 2
    status_invalidos = df[
        df["status_vrf"].astype(str).str.strip() != "2"
    ]

    if not status_invalidos.empty:
        print("\nRegistros inválidos:\n")
        print(  status_invalidos[    ["seq", "cod_estacao", "status_vrf"]      ]        )
        raise Exception ("Nem todos os registros estão com STATUS_VRF=2." )

    print(df[
        df["lat_grau"].isna()
        | df["lat_min"].isna()
        | df["lon_grau"].isna()
        | df["lon_min"].isna()
        ][["seq","cod_estacao"]])

    print(f"Total registros: {len(df)}")
    print(f"STATUS_VRF=2: {len(df[df['status_vrf'].astype(str).str.strip()=='2'])}"   )    
    print(f"Validação OK. {len(df)} registros aptos para integração."   )


class BdgCargaExecutor:

    def __init__(self, connection):
        self.connection = connection

    def atualizar_complemento(self, df):
        try:
            dados = [
                (
                row["tem_foto"],
                row["tem_foto_chapa"],
                row["versao_app"],
                row["seq"],
                )
                for _, row in df.iterrows()
                ]
            
            cursor = self.connection.cursor()
            
            cursor.executemany(
                """
                UPDATE bdg_valida.t_sadgeo
                SET tem_foto = :1,
                tem_foto_chapa = :2,
                campo_atualizad = :3
                WHERE seq = :4
                """,
                dados
                )  
            
            
            self.connection.commit()

            total = len(dados)
            print(
                f"\nSUCESSO: {total} registros processados."
            )
            
        except oracledb.DatabaseError as e:
            self.connection.rollback()
            error_obj, = e.args
            print("Oracle Code:", error_obj.code)
            print("Oracle Message:", error_obj.message)
            raise

        finally:
            if cursor:
                cursor.close()

              
    def atualizar_critica(self, df):

        validar_dataframe(df)

        cursor = self.connection.cursor()

        total = len(df)

        try:

            for i, row in df.iterrows():

                print(
                    f"[{i+1}/{total}] "
                    f"{row['cod_estacao']} "
                    f"SEQ={row['seq']}"
                )

                cursor.callproc(
                    "BDG_VALIDA.PCKG_SADGEO_PUT.ATUALIZA_SADGEO_WEB_3",
                    [

                        # p_tipo
                        "1",

                        # p_seq
                        nvl_str(row["seq"]),

                        # p_cod_estacao
                        nvl_str(row["cod_estacao"]),

                        # p_dsc_estacao
                        nvl_str(row["descricao"]),

                        # p_tipo_monumentacao
                        nvl_str(row["monumentacao"]),

                        # p_tipo_local
                        nvl_str(row["tipo_local"]),

                        # p_cod_situacao_marco_principal
                        nvl_str(row["situacao"]),

                        # p_dsc_localizacao
                        nvl_str(row["localizacao"]),

                        # p_dsc_itinerario
                        nvl_str(row["itinerario"]),

                        # p_dsc_observacao
                        nvl_str(row["observacao"]),

                        # p_i_ocupacao_gps
                        nvl_str(row["is_ocup_gps"]),

                        # p_i_ocupacao_gravim
                        nvl_str(row["is_ocup_gravimetro"]),

                        # p_i_ocupacao_nivel
                        nvl_str(row["is_ocup_mira"]),

                        # p_inscricao_chapa
                        nvl_str(row["inscr_chapa"]),

                        # p_sinal_lat
                        nvl_sinal_coord(row["lat_sinal"]),

                        # p_grau_lat
                        nvl_int(row["lat_grau"]),

                        # p_min_lat
                        nvl_int(row["lat_min"]),

                        # p_seg_lat
                        nvl_float(row["lat_seg"]),

                        # p_grau_lon
                        nvl_int(row["lon_grau"]),

                        # p_min_lon
                        nvl_int(row["lon_min"]),

                        # p_seg_lon
                        nvl_float(row["lon_seg"]),

                        # p_datum
                        '06',

                        # p_irregularidades
                        None,

                        # p_nomenclat_conex
                        nvl_str(row["conexao"]),

                        # p_tipo_conexao
                        nvl_str(row["tipo_conexao"]),

                        # p_projeto
                        nvl_str(row["projeto"]),

                        # p_caderneta
                        nvl_str(row["caderneta"]),

                        # p_rn_anterior
                        nvl_str(row["rn_anterior"]),

                        # p_linha
                        nvl_str(row["linha"]),

                        # p_disp_ggc
                        "S",

                        # p_disp_proj
                        "S",

                        # p_critico
                        nvl_str(row["informante"]),

                        # p_fonte
                        nvl_str(row["tipo_fonte_coord"]),

                        # p_ok_coord
                        nvl_ok_coord(row["is_atualizar_coord"]),

                        # p_protocolo_homolog
                        None
                    ]
                )

            self.connection.commit()

            print(
                f"\nSUCESSO: {total} registros processados."
            )

        except oracledb.DatabaseError as e:

            self.connection.rollback()
            error_obj, = e.args
            print("Oracle Code:", error_obj.code)
            print("Oracle Message:", error_obj.message)
            raise

        finally:
            if cursor:
                cursor.close()
            
            
def identificar_fotos(df, pasta_base):

    arquivos = {
    f.stem.upper()
        for f in Path(pasta_base).iterdir()
        if f.is_file()
    }

    df["tem_foto"] = df["cod_estacao"].apply(
        lambda x: "S" if str(x).upper() in arquivos else "N"
    )

    df["tem_foto_chapa"] = df["cod_estacao"].apply(
        lambda x: "S" if f"{str(x).upper()}C" in arquivos else "N"
    )

    return df


#//-------

if __name__ == "__main__":
        
    
    arquivo = input("Informe path/arquivo SIDGEO para atualização da critica:")
    
      
    conn = oracledb.connect(
        user="paulo_gimenez",
        password="u1792847S261",
        dsn="oraprdent2.ibge.gov.br:1521/pent2"
        )

    # ========================================
    # EXECUÇÃO
    # ========================================
    df = pd.read_csv(
        arquivo,
        sep=";",
        quotechar='"',
        encoding="utf-8",
        engine="python"
    )
    
    pasta_carga = Path(arquivo).parent
    
    df = identificar_fotos(df, pasta_carga)
    
    executor = BdgCargaExecutor(conn)
    
    executor.atualizar_critica(df)
    
    executor.atualizar_complemento(df)
    