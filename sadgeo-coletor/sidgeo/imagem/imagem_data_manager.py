# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 17:18:24 2026

@author: paulo.gimenez
"""

import os
import json
from pathlib import Path
import pandas as pd

from imagem_model import TImagem, TImagemConteudo, TImagemEstacao, TImagemRepositorio

def carregar_dataframe(arquivo: str) -> pd.DataFrame:
    ext = Path(arquivo).suffix.lower()
    if ext in [".xlsx", ".xls"]:
        return pd.read_excel(arquivo)
    if ext == ".json":
        return pd.read_json(arquivo)
    if ext == ".parquet":
        return pd.read_parquet(arquivo)

    raise ValueError(
        f"Formato não suportado: {ext}"
)


def carregar_dataframe(arquivo: str) -> pd.DataFrame:

    ext = Path(arquivo).suffix.lower()

    if ext in [".xlsx", ".xls"]:
        return pd.read_excel(arquivo)

    if ext == ".json":
        return pd.read_json(arquivo)

    if ext == ".parquet":
        return pd.read_parquet(arquivo)

    raise ValueError(
        f"Formato não suportado: {ext}"
    )

def row_para_timagem(row) -> TImagem:

    dt_hash = row["DT_HASH"]

    if pd.notnull(dt_hash):
        dt_hash = pd.to_datetime(dt_hash)

    dt_captura = row["DT_CAPTURA_IMAGEM_ORIGINAL"]

    if pd.notnull(dt_captura):
        dt_captura = pd.to_datetime(dt_captura)

    return TImagem(
        uuid_imagem=None,

        tx_hash=row["TX_HASH"],
        dt_hash=dt_hash,

        nr_tamanho_arquivo=row["NR_TAMANHO_ARQUIVO"],

        nr_largura_imagem=row["NR_LARGURA_IMAGEM"],
        nr_altura_imagem=row["NR_ALTURA_IMAGEM"],

        tx_fabricante_dispositivo=row["TX_FABRICANTE_DISPOSITIVO"],
        tx_modelo_dispositivo=row["TX_MODELO_DISPOSITIVO"],

        dt_captura_imagem_original=dt_captura,

        tx_iso_imagem=row["TX_ISO_IMAGEM"],
        tx_abertura_imagem=row["TX_ABERTURA_IMAGEM"],
        tx_tempo_exposicao=row["TX_TEMPO_EXPOSICAO"],

        nr_resolucao_horizontal=row["NR_RESOLUCAO_HORIZONTAL"],
        nr_resolucao_vertical=row["NR_RESOLUCAO_VERTICAL"],

        gps_latitude=row["GPS_LATITUDE"],
        gps_longitude=row["GPS_LONGITUDE"],
        gps_altitude=row["GPS_ALTITUDE"]
    )