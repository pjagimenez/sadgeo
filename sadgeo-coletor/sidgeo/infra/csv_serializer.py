# -*- coding: utf-8 -*-
"""
file: /sidgeo/infra/csv_serializer.py
@created: 26-08-2025 pjag
@updated: 03-07-2026 pjag Refatoração MVC, GRASP, PEP8 pythonic
"""

from __future__ import annotations

import csv
from pathlib import Path

import pandas as pd

from sidgeo.domain.registro_metadados import (
    COLUNA_VERSAO,
    COLUNAS_BOOLEANAS,
)
from sidgeo.infra.dataframe_schema import normalizar_dataset
from sidgeo.util.settings import APP_VERSAO
from sidgeo.util.strings import detectar_encoding


SEPARADOR_CSV = ";"


class CsvSerializer:
    """Importa e exporta registros em formato CSV."""

    def importar(
        self,
        caminho: str | Path,
        separador: str = SEPARADOR_CSV,
    ) -> pd.DataFrame:
        path = Path(caminho)
        encoding = detectar_encoding(str(path)) or "utf-8"

        try:
            df = pd.read_csv(
                path,
                sep=separador,
                quotechar='"',
                encoding=encoding,
                index_col=False,
                on_bad_lines="skip",
                keep_default_na=False,
                na_values=[],
            )
        except Exception as erro:
            raise RuntimeError(f"Erro ao importar CSV: {erro}") from erro

        return normalizar_dataset(df)

    def exportar(self, df: pd.DataFrame, caminho: str | Path) -> None:
        path = Path(caminho)
        df_exportacao = normalizar_dataset(df)

        for coluna in COLUNAS_BOOLEANAS:
            if coluna in df_exportacao.columns:
                valores = df_exportacao[coluna].astype(str).str.lower()
                booleanos = valores.map({
                    "true": True,
                    "false": False,
                    "1": True,
                    "0": False,
                    "s": True,
                    "n": False,
                })
                df_exportacao[coluna] = (
                    booleanos.map({True: "S", False: "N"})
                    .fillna("")
                )

        if COLUNA_VERSAO in df_exportacao.columns:
            df_exportacao[COLUNA_VERSAO] = APP_VERSAO

        df_exportacao.to_csv(
            path,
            index=False,
            sep=SEPARADOR_CSV,
            quoting=csv.QUOTE_ALL,
            quotechar='"',
        )