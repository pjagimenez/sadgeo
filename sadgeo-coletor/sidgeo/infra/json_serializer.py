# -*- coding: utf-8 -*-
"""
file: /sidgeo/infra/json_serializer.py
@created: 26-08-2025 pjag
@updated: 03-07-2026 pjag Refatoração MVC, GRASP, PEP8 pythonic
"""

from __future__ import annotations

from pathlib import Path
import json

import pandas as pd

from sidgeo.infra.dataframe_schema import normalizar_dataset


class JsonSerializer:
    """Importa e exporta registros em formato JSON."""

    def importar(self, caminho: str | Path) -> pd.DataFrame:
        path = Path(caminho)

        try:
            df = pd.read_json(path, orient="records", dtype=False)
        except Exception as erro:
            raise RuntimeError(f"Erro ao importar JSON: {erro}") from erro

        if "fotos" in df.columns:
            df["fotos"] = df["fotos"].map(lambda valor: json.dumps(valor, ensure_ascii=False) if isinstance(valor, list) else valor)
        return normalizar_dataset(df)

    def exportar(self, df: pd.DataFrame, caminho: str | Path) -> None:
        path = Path(caminho)
        df_exportacao = normalizar_dataset(df)
        if "fotos" in df_exportacao.columns:
            df_exportacao["fotos"] = df_exportacao["fotos"].map(
                lambda valor: json.loads(valor) if isinstance(valor, str) and valor.strip() else [])

        df_exportacao.to_json(
            path,
            orient="records",
            force_ascii=False,
            indent=2,
            date_format="iso",
        )
