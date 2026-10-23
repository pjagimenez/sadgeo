# -*- coding: utf-8 -*-
"""
file: /sidgeo/infra/repositorio_registro.py
@created: 26-08-2025 pjag
@updated: 03-07-2026 pjag Refatoração MVC, GRASP, PEP8 pythonic
"""

from __future__ import annotations

from pathlib import Path
from typing import Any
from sidgeo.domain.registro_mapeador import RegistroMapeador
from sidgeo.infra.notificacao_evento_log import NotificadorEventoLog

import pandas as pd
import platformdirs

from sidgeo.domain.registro import Registro
from sidgeo.domain.registro_metadados import (
    COLUNA_CHAVE_LOGICA,
    COLUNAS_NOMES,
)
from sidgeo.infra.persistencia_hdf import HdfDataStore
from sidgeo.infra.csv_serializer import CsvSerializer
from sidgeo.infra.json_serializer import JsonSerializer
from sidgeo.util.settings import APP_SIGLA

class RepositorioRegistro:
    """Repositório local de registros SIDGeo."""

    def __init__(self, log_servico: NotificadorEventoLog, mapeador: RegistroMapeador,
                 data_dir: Path | None = None) -> None:
        self.mapeador = mapeador
        self.notificador = log_servico

        data_dir = data_dir or Path(
            platformdirs.user_data_dir(
                appname=APP_SIGLA,
                appauthor=False,
                roaming=False,
            )
        )
        data_dir.mkdir(parents=True, exist_ok=True)

        self.filename = data_dir / "sidgeo.h5"
        self.hdf_store = HdfDataStore(self.filename)
        self.csv_serializer = CsvSerializer()
        self.json_serializer = JsonSerializer()

        self.dataset = self.hdf_store.carregar()

    def encerrar(self) -> None:
        self.hdf_store.salvar(self.dataset)

    def salvar(self, registro: Registro) -> None:
        registro_dict = self.mapeador.registro_para_dict(registro)
        anterior = self.dataset.copy(deep=True)
        try:
            self._persistir_registro_memoria(registro_dict)
            self.hdf_store.salvar(self.dataset)
        except Exception:
            self.dataset = anterior
            raise

    def inserir(self, registro: Registro) -> bool:
        total_antes = len(self.dataset)
        self.salvar(registro)
        return len(self.dataset) > total_antes

    def excluir(self, codigo: str) -> bool:
        if COLUNA_CHAVE_LOGICA not in self.dataset.columns:
            return False

        total_antes = len(self.dataset)

        novo_dataset = self.dataset[
            self.dataset[COLUNA_CHAVE_LOGICA].astype("string").str.strip()
            != codigo.strip()
        ].copy()

        excluiu = len(novo_dataset) < total_antes

        if excluiu:
            self.hdf_store.salvar(novo_dataset)
            self.dataset = novo_dataset

        return excluiu

    def buscar_por_codigo(self, codigo: str) -> Registro | None:
        if COLUNA_CHAVE_LOGICA not in self.dataset.columns:
            return None

        filtro = (
            self.dataset[COLUNA_CHAVE_LOGICA].astype("string").str.strip()
            == codigo.strip()
        )

        registros = self.mapeador.df_para_registros(self.dataset[filtro])
        return registros[0] if registros else None

    def listar_todos(self) -> list[Registro]:
        return self.mapeador.df_para_registros(self.dataset.copy())

    def importar(self, caminho: str, formato: str = "csv") -> list[Registro]:
        path = Path(caminho)

        if formato.lower() == "csv":
            df_importado = self.csv_serializer.importar(path)
        elif formato.lower() == "json":
            df_importado = self.json_serializer.importar(path)
        else:
            raise ValueError(f"Formato não suportado: {formato}")

        return self.mapeador.df_para_registros(df_importado)

    def exportar(self, caminho: str, formato: str = "csv") -> None:
        path = Path(caminho)

        if formato.lower() == "csv":
            self.csv_serializer.exportar(self.dataset, path)
        elif formato.lower() == "json":
            self.json_serializer.exportar(self.dataset, path)
        else:
            raise ValueError(f"Formato não suportado: {formato}")

    def zerar_base(self) -> None:
        vazio = pd.DataFrame(columns=COLUNAS_NOMES)
        self.hdf_store.salvar(vazio)
        self.dataset = vazio

    def _persistir_registro_memoria(self, registro: dict[str, Any]) -> None:
        codigo = str(registro.get(COLUNA_CHAVE_LOGICA, "") or "").strip()

        if not codigo:
            self.notificador.warn("Código da estação ausente no registro.")
            return

        self._garantir_schema()

        filtro = (
            self.dataset[COLUNA_CHAVE_LOGICA].astype("string").str.strip()
            == codigo
        )
        indices = self.dataset.index[filtro].tolist()

        if indices:
            indice = indices[0]
            for campo, valor in registro.items():
                if campo in self.dataset.columns:
                    self.dataset.at[indice, campo] = valor
            self.notificador.info(f"Registro da estação '{codigo}' atualizado.")
        else:
            novo = pd.DataFrame([registro])
            self.dataset = novo if self.dataset.empty else pd.concat(
                [self.dataset, novo], ignore_index=True)
            self.notificador.info(f"Registro da estação '{codigo}' incluído.")

        self._ordenar_por_codigo()

    def _garantir_schema(self) -> None:
        for coluna in COLUNAS_NOMES:
            if coluna not in self.dataset.columns:
                self.dataset[coluna] = pd.NA

        self.dataset = self.dataset[COLUNAS_NOMES].copy()

    def _ordenar_por_codigo(self) -> None:
        if COLUNA_CHAVE_LOGICA in self.dataset.columns:
            self.dataset = self.dataset.sort_values(
                by=COLUNA_CHAVE_LOGICA, kind="mergesort",
            ).reset_index(drop=True)
