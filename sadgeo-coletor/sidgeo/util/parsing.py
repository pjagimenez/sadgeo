# -*- coding: utf-8 -*-
"""
file: /sidgeo/util/parsing.py
@created: 24-03-2025 pjag
@updated: 16-10-2025 pjag
"""

from __future__ import annotations

from collections.abc import Iterable
from datetime import datetime
from decimal import Decimal, InvalidOperation

# conjuntos de verdade/mentira (pt/en)
_TRUE_SET = {"true", "t", "1", "y", "yes", "sim", "s"}
_FALSE_SET = {"false", "f", "0", "n", "no", "nao", "não"}


def reversa_codigo_dic(dicionario: dict[str, str], valor_descr: str | None ) -> str | None:
    """Resolve o código a partir da descrição (case-insensitive)."""

    if not valor_descr:
        return None

    descr_para_cod = {
        str(valor).upper(): str(chave)
        for chave, valor in dicionario.items()
    }
    return descr_para_cod.get(str(valor_descr).upper())



def parse_data(valor: object, formatos: Iterable[str] | None = None) -> datetime | None:
    """Converte str -> datetime considerando formatos comuns; aceita datetime/None."""
    if isinstance(valor, datetime):
        return valor
    if not isinstance(valor, str) or not valor.strip():
        return None

    s = valor.strip()
    formatos_padrao = [
        "%d/%m/%Y %H:%M:%S",
        "%d/%m/%Y %H:%M",
        "%d/%m/%Y",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d",
        "%d-%m-%Y",
        "%Y%m%d",
        "%d%m%Y",
    ]
    formatos = list(formatos) if formatos else formatos_padrao

    for fmt in formatos:
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue
    try:
        return datetime.fromisoformat(s)
    except ValueError:
        return None


def bool_to_str(val: object) -> str:
        """ Converte logico em String  S ou N """
        return 'S' if str(val).strip().lower() in ['true', '1', 's'] else 'N'


def str_para_bool(valor: object, default: bool = False) -> bool:
    """Converte bool/int/str (pt/en) para bool; fallback em `default`."""
    if isinstance(valor, bool):
        return valor
    if isinstance(valor, (int, float)):
        return bool(valor)
    if isinstance(valor, str):
        s = valor.strip().lower()
        if s in _TRUE_SET:
            return True
        if s in _FALSE_SET:
            return False
    return default

def parse_coordinate(value: object) -> Decimal:
        """
        Converte uma string numérica (com vírgula ou ponto) em Decimal,
        preservando todas as casas decimais originais.
        Em caso de erro, retorna Decimal('0').
        """
        s = str(value).replace(',', '.').strip()
        try:
            return Decimal(s)
        except InvalidOperation:
            return Decimal('0')


def _normalize_number_string(value: str) -> str:
    """
    Normaliza string numérica com vírgula/ponto:
      - remove espaços
      - vírgula única vira ponto
      - se tiver ponto e vírgula, último separador é decimal
    """
    s = value.strip().replace(" ", "")
    if "," in s and "." not in s:
        return s.replace(",", ".")
    if "." in s and "," not in s:
        return s
    if "," in s and "." in s:
        last_comma = s.rfind(",")
        last_dot = s.rfind(".")
        if last_comma > last_dot:
            return s.replace(".", "").replace(",", ".")
        else:
            return s.replace(",", "")
    return s


def safe_int(value: object, default: int = 0) -> int:
    """Converte para int de forma robusta; aceita '', None, vírgula decimal e milhares."""
    if value is None:
        return default
    try:
        s = _normalize_number_string(str(value))
        return int(float(s)) if s else default   # truncamento int()
    except ValueError:
        return default


def safe_float(value: object, default: float = 0.0) -> float:
    """Converte para float de forma robusta; aceita '', None, vírgula decimal e milhares."""
    if value is None:
        return default
    try:
        s = _normalize_number_string(str(value))
        return float(s) if s else default
    except ValueError:
        return default
