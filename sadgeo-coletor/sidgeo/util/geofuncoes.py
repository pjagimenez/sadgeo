# -*- coding: utf-8 -*-
"""
file: /sidgeo/util/geofuncoes.py
"""

from __future__ import annotations

import math
import re


def normalizar_hemisferio(valor: str | None) -> str:
    """Normaliza hemisfério para sinal + ou -."""
    if not valor:
        return ""

    texto = str(valor).strip().upper()

    if texto in ("S", "W", "O", "-"):
        return "-"

    if texto in ("N", "E", "+"):
        return "+"

    return ""


def gms_para_decimal(
    sinal: str,
    grau: int | float | str,
    minuto: int | float | str,
    segundo: int | float | str,
) -> float:
    """Converte coordenada GMS para decimal."""
    sinal_norm = normalizar_hemisferio(sinal)

    decimal = (
        abs(float(grau))
        + (float(minuto) / 60.0)
        + (float(str(segundo).replace(",", ".")) / 3600.0)
    )

    return -decimal if sinal_norm == "-" else decimal


def decimal_para_gms(valor: float) -> dict[str, str | int | float]:
    """Converte coordenada decimal para GMS com sinal + ou -."""
    sinal = "-" if valor < 0 else "+"
    absoluto = abs(float(valor))

    grau = int(absoluto)
    resto_minutos = (absoluto - grau) * 60.0
    minuto = int(resto_minutos)
    segundo = (resto_minutos - minuto) * 60.0

    return {
        "sinal": sinal,
        "grau": grau,
        "min": minuto,
        "seg": round(segundo, 6),
    }


def distancia_haversine(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float,
    raio_terra_km: float = 6371.0088,
) -> float:
    """Calcula distância geodésica aproximada entre dois pontos em quilômetros."""
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    delta_lat = lat2_rad - lat1_rad
    delta_lon = lon2_rad - lon1_rad

    a = (
        math.sin(delta_lat / 2.0) ** 2
        + math.cos(lat1_rad)
        * math.cos(lat2_rad)
        * math.sin(delta_lon / 2.0) ** 2
    )

    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return raio_terra_km * c


def parse_gms(texto: str | None) -> dict[str, str | int | float]:
    """Converte texto GMS em sinal +/-, grau, minuto e segundo."""
    if not texto:
        return {"sinal": "", "grau": 0, "min": 0, "seg": 0.0}

    padrao = re.compile(
        r"""^\s*
            (\d+)\s*[ºo]\s*
            (\d+)\s*'\s*
            ([\d.,]+)\s*"\s*
            ([NnSsEeWwOo+-])\s*
        $""",
        re.VERBOSE,
    )

    match = padrao.match(texto.strip())
    if not match:
        return {"sinal": "", "grau": 0, "min": 0, "seg": 0.0}

    grau, minuto, segundo, direcao = match.groups()

    try:
        return {
            "sinal": normalizar_hemisferio(direcao),
            "grau": int(grau),
            "min": int(minuto),
            "seg": float(segundo.replace(",", ".")),
        }
    except ValueError:
        return {"sinal": "", "grau": 0, "min": 0, "seg": 0.0}


def validar_latitude(latitude: float, margem: float = 1.0) -> bool:
    """Valida latitude dentro do Brasil com margem em graus."""
    limite_sul = -34.0 - margem
    limite_norte = 6.0 + margem

    return limite_sul <= latitude <= limite_norte


def validar_longitude(longitude: float, margem: float = 1.0) -> bool:
    """Valida longitude dentro do Brasil com margem em graus."""
    limite_oeste = -74.0 - margem
    limite_leste = -34.0 + margem

    return limite_oeste <= longitude <= limite_leste