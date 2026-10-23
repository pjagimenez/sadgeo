# -*- coding: utf-8 -*-
"""
file: /sidgeo/infra/dataframe_schema.py
@created: 03-07-2026 pjag
@updated: 03-07-2026 pjag Refatoração MVC, GRASP, PEP8 pythonic
"""

from __future__ import annotations

import pandas as pd

from sidgeo.domain.registro_metadados import COLUNAS_NOMES


def normalizar_dataset(df_origem: pd.DataFrame) -> pd.DataFrame:
    if df_origem is None:
        df_origem = pd.DataFrame(columns=COLUNAS_NOMES)
    
    
    df = df_origem.copy()

    df.columns = [
        str(coluna).strip().replace("\\", "").replace(" ", "_").lower()
        for coluna in df.columns
    ]

    colunas_validas = [
        coluna for coluna in df.columns
        if coluna in COLUNAS_NOMES
    ]

    df = df[colunas_validas].copy()

    for coluna in COLUNAS_NOMES:
        if coluna not in df.columns:
            df[coluna] = pd.NA

    df = df[COLUNAS_NOMES].copy()

    for coluna in df.columns:
        if (
            df[coluna].dtype == "object"
            or pd.api.types.is_string_dtype(df[coluna].dtype)
        ):
            df[coluna] = df[coluna].astype("string").str.strip()

    df.reset_index(drop=True, inplace=True)
    return df