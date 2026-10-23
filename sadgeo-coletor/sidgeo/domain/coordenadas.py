"""Validação e comparação horizontal das coordenadas de uma estação."""
from __future__ import annotations

import math

from sidgeo.domain.registro import Registro
from sidgeo.util.geofuncoes import gms_para_decimal, distancia_haversine, normalizar_hemisferio


def coordenadas_decimais(registro: Registro) -> tuple[float, float]:
    for sinal, grau, minuto, segundo, limite in (
        (registro.lat_sinal, registro.lat_grau, registro.lat_min, registro.lat_seg, 90),
        (registro.lon_sinal, registro.lon_grau, registro.lon_min, registro.lon_seg, 180),
    ):
        if (not normalizar_hemisferio(sinal)
                or not all(math.isfinite(v) for v in (grau, minuto, segundo))
                or not 0 <= grau <= limite or not 0 <= minuto < 60 or not 0 <= segundo < 60
                or (grau == limite and (minuto != 0 or segundo != 0))):
            raise ValueError("Coordenadas incompletas ou inválidas; confira sinal, graus, minutos e segundos.")
    return (
        gms_para_decimal(registro.lat_sinal, registro.lat_grau, registro.lat_min, registro.lat_seg),
        gms_para_decimal(registro.lon_sinal, registro.lon_grau, registro.lon_min, registro.lon_seg),
    )


def diferenca_horizontal_m(local: Registro, bdg: Registro) -> float:
    lat1, lon1 = coordenadas_decimais(local)
    lat2, lon2 = coordenadas_decimais(bdg)
    return distancia_haversine(lat1, lon1, lat2, lon2) * 1000.0
