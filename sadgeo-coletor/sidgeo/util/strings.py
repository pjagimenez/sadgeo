# -*- coding: utf-8 -*-
"""
file: /sidgeo/util/strings.py
@created: 24-03-2025 pjag
@updated: 03-07-2026 pjag Refatoração MVC, GRASP, PEP8 pythonic
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from pathlib import Path

from sidgeo.util.settings import PLACEHOLDER

try:
    from charset_normalizer import from_path as _charset_from_path  # pyright: ignore[reportUnknownVariableType]
except ImportError:
    _charset_from_path = None


def detectar_encoding(filepath: str | Path) -> str:
    """Detecta encoding do arquivo; fallback para UTF-8."""
    if _charset_from_path is None:
        return "utf-8"

    try:
        resultado = _charset_from_path(str(filepath)).best()
    except OSError:
        return "utf-8"

    return resultado.encoding if resultado else "utf-8"


def trim_all(dados: Mapping[str, object]) -> dict[str, object]:
    """Aplica strip em strings de um dict e converte string vazia para None."""
    saida: dict[str, object] = {}

    for chave, valor in dados.items():
        if isinstance(valor, str):
            texto = valor.strip()
            saida[chave] = texto if texto else None
        else:
            saida[chave] = valor

    return saida


def bool_para_sn(valor: bool | None, vazio: str = "") -> str:
    """Mapeia True/False/None para S/N/vazio."""
    if valor is True:
        return "S"
    if valor is False:
        return "N"
    return vazio


def labels_from_opcoes(opcoes: Iterable[tuple[str, str]]) -> list[str]:
    """Recebe [(COD, 'COD - Descrição')] e devolve apenas os labels."""
    return [label for _, label in opcoes]


def values_with_placeholder(
    labels: Iterable[str],
    placeholder: str = PLACEHOLDER,
) -> list[str]:
    """Insere placeholder como primeira opção."""
    return [placeholder, *list(labels)]


def list_from_dict_cod_desc(dicionario: dict[str, str]) -> list[str]:
    """Converte dict code->desc em lista ['COD - Descrição', ...]."""
    return [
        f"{codigo} - {descricao}"
        for codigo, descricao in dicionario.items()
    ]


def truncar(valor: object, tamanho: int = 8) -> str:
    """Trunca texto à esquerda até o tamanho informado."""
    texto = str(valor)
    return texto[:tamanho]
