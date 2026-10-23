# -*- coding: utf-8 -*-
"""
file: /sidgeo/ui/widgets.py
@created: 24-03-2025 pjag
@updated: 03-07-2026 pjag Refatoração MVC, GRASP, PEP8 pythonic
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

import pandas as pd

from sidgeo.util.settings import PLACEHOLDER


def valor_para_widget(
    valor: Any,
    tipo: str = "str",
    padrao: str = "",
) -> Any:
    """Prepara valores para widgets Tkinter."""
    if valor is None or pd.isna(valor):
        return False if tipo == "bool" else padrao

    if tipo == "str":
        return str(valor)

    if tipo == "int":
        try:
            return str(int(valor))
        except (TypeError, ValueError):
            return padrao

    if tipo == "float":
        try:
            return str(float(valor))
        except (TypeError, ValueError):
            return padrao

    if tipo == "bool":
        if isinstance(valor, bool):
            return valor

        texto = str(valor).strip().lower()
        return texto in {"1", "true", "t", "sim", "yes", "y", "s"}

    if tipo == "date":
        if isinstance(valor, datetime):
            return valor

        try:
            return pd.Timestamp(valor)
        except (TypeError, ValueError):
            return None

    return str(valor)


def obter_valor_completo(
    combo_valor: object,
    combo_dict: dict[str, str],
    placeholder: str = PLACEHOLDER,
) -> str:
    """Retorna 'COD - Descrição' se a chave existir no dict."""
    chave = str(combo_valor).strip() if combo_valor is not None else ""

    if chave and chave in combo_dict:
        return f"{chave} - {combo_dict[chave]}"

    return placeholder
