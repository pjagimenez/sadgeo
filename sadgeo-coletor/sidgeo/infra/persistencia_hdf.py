# -*- coding: utf-8 -*-
"""
file: /sidgeo/infra/persistencia_hdf.py
@created: 26-08-2025 pjag
@updated: 03-07-2026 pjag Refatoração MVC, GRASP, PEP8 pythonic
"""

from __future__ import annotations

import os
import tempfile
from pathlib import Path

import pandas as pd

from sidgeo.domain.registro_metadados import (
    COLUNA_VERSAO,
    COLUNAS_NOMES,
)
from sidgeo.infra.dataframe_schema import normalizar_dataset
from sidgeo.util.settings import APP_HDFSTORE_KEY, APP_VERSAO


class HdfDataStore:
    """Persistência local em arquivo HDF5."""

    def __init__(self, filename: str | Path) -> None:
        self.filename = Path(filename)

    def carregar(self) -> pd.DataFrame:
        if not self.filename.exists():
            df_vazio = pd.DataFrame(columns=COLUNAS_NOMES)
            self.salvar(df_vazio)
            return df_vazio
        try:
            # Versões anteriores gravavam o DataFrame vazio sem criar a chave 'dados'.
            with pd.HDFStore(self.filename, mode="r") as store:
                if not store.keys():
                    return pd.DataFrame(columns=COLUNAS_NOMES)
            df = pd.read_hdf(self.filename, key=APP_HDFSTORE_KEY)
            if not isinstance(df, pd.DataFrame):
                raise ValueError("A chave de dados não contém uma tabela de registros.")
            return normalizar_dataset(df)
        except Exception as erro:
            raise RuntimeError(
                f"Erro ao carregar HDF5 '{self.filename}': {erro}. "
                "O arquivo original foi preservado; nenhuma base vazia o substituiu."
            ) from erro

    def salvar(self, df: pd.DataFrame) -> None:
        df_local = normalizar_dataset(df)

        if COLUNA_VERSAO in df_local.columns:
            df_local[COLUNA_VERSAO] = APP_VERSAO

        df_hdf = self._preparar_para_hdf(df_local)

        temporario: Path | None = None
        try:
            # O arquivo anterior só é substituído depois da gravação completa.
            fd, nome = tempfile.mkstemp(prefix="sidgeo-", suffix=".h5", dir=self.filename.parent)
            os.close(fd)
            temporario = Path(nome)
            df_hdf.to_hdf(
                temporario,
                key=APP_HDFSTORE_KEY,
                mode="w",
                format="fixed" if df_hdf.empty else "table",
            )
            os.replace(temporario, self.filename)
        except Exception as erro:
            raise RuntimeError(
                f"Erro ao salvar HDF5 '{self.filename}': {erro}"
            ) from erro
        finally:
            if temporario is not None:
                temporario.unlink(missing_ok=True)

    @staticmethod
    def _preparar_para_hdf(df: pd.DataFrame) -> pd.DataFrame:
        df_local = df.copy()

        for coluna in df_local.columns:
            if pd.api.types.is_string_dtype(df_local[coluna].dtype):
                serie = df_local[coluna].astype("string")
                df_local[coluna] = serie.where(~serie.isna(), "").astype(object)

            elif (
                str(df_local[coluna].dtype) == "boolean"
                or pd.api.types.is_bool_dtype(df_local[coluna].dtype)
            ):
                df_local[coluna] = (
                    pd.Series(df_local[coluna], dtype="boolean")
                    .fillna(False)
                    .astype(bool)
                )

            elif str(df_local[coluna].dtype) == "Int64":
                df_local[coluna] = df_local[coluna].astype("float64")

            elif str(df_local[coluna].dtype) == "Float64":
                df_local[coluna] = df_local[coluna].astype("float64")

        return df_local
