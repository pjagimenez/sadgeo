# -*- coding: utf-8 -*-
"""
file: /sidgeo/util/settings.py
@created: 24-03-2025 pjag
@updated: 16-10-2025 pjag
"""

from __future__ import annotations

APP_VERSAO = "v1.1.1.261023"
APP_SIGLA = "SIDGEO"
APP_ALTURA = 680
APP_LARGURA = 1280

APP_URL_SADGEO = "https://w3.api-sadgeo.ibge.gov.br/api"

APP_URL_BDG = "http://w3.servicoscged.ibge.gov.br/api/v1/bdg"

# URLs-base: não acrescente código de estação nem query string aqui.
# SADGEO: {APP_URL_SADGEO}/itemsadgeo/filtrar/estacao/{codigo}
# BDG: {APP_URL_BDG}/estacoes?codigoEstacao={codigo}

PLACEHOLDER = "Selecione..."

APP_HDFSTORE_KEY = "dados"
