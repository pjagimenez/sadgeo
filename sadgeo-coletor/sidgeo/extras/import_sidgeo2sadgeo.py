# -*- coding: utf-8 -*-
import pandas as pd
import oracledb
import numpy as np

arquivo = input("Informe path/arquivo SIDGEO para carga:")
s_idchamado = input("Informe o ID do Chamado GLPI:")

idchamado = int(s_idchamado)

df = pd.read_csv(
    arquivo,
    sep=";",
    quotechar='"',
    encoding="utf-8",
    engine="python"
)

# Datas
for col in ["data_levantamento", "data_critica"]:
    df[col] = pd.to_datetime(df[col], errors="coerce")

# Numéricos
for col in [
    "lat_grau",
    "lat_min",
    "lat_seg",
    "lon_grau",
    "lon_min",
    "lon_seg",
    "status_vrf"
    ]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Renomeia para os nomes Oracle
df = df.rename(columns={
"versao_app": "VERSAO_APP",
"cod_estacao": "COD_ESTACAO",
"monumentacao": "TIPO_MONUMENTACAO",
"tipo_local": "TIPO_LOCAL",
"inscr_chapa": "INSCRICAO_CHAPA",
"situacao": "COD_SITUACAO_MARCO_PRINCIPAL",
"conexao": "NOMENCLAT_CONEX",
"tipo_conexao": "TIPO_CONEXAO",
"rn_anterior": "RN_ANTERIOR",
"campanha": "CAMPANHA",
"data_levantamento": "DAT_FIM_LEVANTAMENTO",
"data_critica": "DAT_CRITICA",
"projeto": "PROJETO",
"nue": "NUE",
"linha": "LINHA",
"caderneta": "CADERNETA",
"informante": "ANOTADOR",
"siape": "SIAPE_ANOTADOR",
"tipo_fonte_coord": "COD_FONTE_COORD",
"lat_sinal": "SINAL_LAT",
"lat_grau": "GRAU_LAT",
"lat_min": "MIN_LAT",
"lat_seg": "SEG_LAT",
"lon_sinal": "SINAL_LON",
"lon_grau": "GRAU_LON",
"lon_min": "MIN_LON",
"lon_seg": "SEG_LON",
"is_atualizar_coord": "OK_COORD",
"is_ocup_gps": "I_OCUPACAO_GPS",
"is_ocup_mira": "I_OCUPACAO_NIVEL",
"is_ocup_gravimetro": "I_OCUPACAO_GRAVIMETRO",
"descricao": "DSC_ESTACAO",
"localizacao": "DSC_LOCALIZACAO",
"itinerario": "DSC_ITINERARIO",
"observacao": "DSC_OBSERVACAO",
"seq": "SEQ",
"status_vrf": "STATUS_VRF",
"municipio": "MUNICIPIO",
"uf": "UF"
})

for c in [
"COD_SITUACAO_MARCO_PRINCIPAL",
"NUE",
"SIAPE_ANOTADOR",
"COD_FONTE_COORD"
]:
    df[c] = df[c].astype(str)


# Metadados da carga
df["ID_CHAMADO_GLPI"] = idchamado
df["ST_PROCESSAMENTO"] = "C"
df["DT_PROCESSAMENTO"] = None
df["TX_MSG_PROCESSAMENTO"] = None
df["TX_ERRO"] = None



df = df.astype(object)
df = df.where(pd.notnull(df), None)
df = df.replace({np.nan: None})



print(df.head())


conn = oracledb.connect(
    user="paulo_gimenez",
    password="u1792847S261",
    dsn="oraprdent2.ibge.gov.br:1521/pent2"
)

cur = conn.cursor()

sql_del = """
delete from BDG_VALIDA.T_ARQUIVO_SIDGEO_IMPORTACAO 
where ID_CHAMADO_GLPI= :ID_CHAMADO_GLPI
"""

cur.execute(
sql_del,
{"ID_CHAMADO_GLPI": int(idchamado)}
)

conn.commit()

print(df.dtypes)


sql_ins = """
INSERT INTO BDG_VALIDA.T_ARQUIVO_SIDGEO_IMPORTACAO (
            ID_CHAMADO_GLPI,
            DT_PROCESSAMENTO,
            TX_MSG_PROCESSAMENTO,
            ST_PROCESSAMENTO,
            TX_ERRO,
            VERSAO_APP,
            COD_ESTACAO,
            TIPO_MONUMENTACAO,
            TIPO_LOCAL,
            INSCRICAO_CHAPA,
            COD_SITUACAO_MARCO_PRINCIPAL,
            NOMENCLAT_CONEX,
            TIPO_CONEXAO,
            RN_ANTERIOR,
            CAMPANHA,
            DAT_FIM_LEVANTAMENTO,
            DAT_CRITICA,
            PROJETO,
            NUE,
            LINHA,
            CADERNETA,
            ANOTADOR,
            SIAPE_ANOTADOR,
            COD_FONTE_COORD,
            SINAL_LAT,
            GRAU_LAT,
            MIN_LAT,
            SEG_LAT,
            SINAL_LON,
            GRAU_LON,
            MIN_LON,
            SEG_LON,
            OK_COORD,
            I_OCUPACAO_GPS,
            I_OCUPACAO_NIVEL,
            I_OCUPACAO_GRAVIMETRO,
            DSC_ESTACAO,
            DSC_LOCALIZACAO,
            DSC_ITINERARIO,
            DSC_OBSERVACAO,
            SEQ,
            STATUS_VRF,
            MUNICIPIO,
            UF
        )
        VALUES (
            :ID_CHAMADO_GLPI,
            :DT_PROCESSAMENTO,
            :TX_MSG_PROCESSAMENTO,
            :ST_PROCESSAMENTO,
            :TX_ERRO,
            :VERSAO_APP,
            :COD_ESTACAO,
            :TIPO_MONUMENTACAO,
            :TIPO_LOCAL,
            :INSCRICAO_CHAPA,
            :COD_SITUACAO_MARCO_PRINCIPAL,
            :NOMENCLAT_CONEX,
            :TIPO_CONEXAO,
            :RN_ANTERIOR,
            :CAMPANHA,
            :DAT_FIM_LEVANTAMENTO,
            :DAT_CRITICA,
            :PROJETO,
            :NUE,
            :LINHA,
            :CADERNETA,
            :ANOTADOR,
            :SIAPE_ANOTADOR,
            :COD_FONTE_COORD,
            :SINAL_LAT,
            :GRAU_LAT,
            :MIN_LAT,
            :SEG_LAT,
            :SINAL_LON,
            :GRAU_LON,
            :MIN_LON,
            :SEG_LON,
            :OK_COORD,
            :I_OCUPACAO_GPS,
            :I_OCUPACAO_NIVEL,
            :I_OCUPACAO_GRAVIMETRO,
            :DSC_ESTACAO,
            :DSC_LOCALIZACAO,
            :DSC_ITINERARIO,
            :DSC_OBSERVACAO,
            :SEQ,
            :STATUS_VRF,
            :MUNICIPIO,
            :UF
        )
    
    """

    
#cur.executemany(
#    sql_ins,
#    df.to_dict("records")
#)

for i, row in enumerate(df.to_dict("records")):
    try:
        cur.execute(sql_ins, row)
    except Exception as e:
        print(f"Erro na linha {i+1}")
        print(row)
        raise


conn.commit()

print(f"{len(df)} registros carregados para o chamado {idchamado}")

cur.close()
conn.close()