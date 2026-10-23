# -*- coding: utf-8 -*-
"""
file: /sidgeo/domain/registro_metadados.py
@created: 02-07-2026 pjag
@updated: 02-07-2026 pjag Refatoração MVC, GRASP, PEP8 pythonic
"""

from dataclasses import fields
from typing import Final

from sidgeo.domain.registro import Registro

# Campos obrigatórios (para UI/validação)
CAMPOS_OBRIGATORIOS: Final[dict[str, str]] = {
    "cod_estacao": "Estação",
    "monumentacao": "Monumentação",
    "tipo_local": "Tipo Local",
    "situacao": "Situação",
    "projeto": "Projeto",
    "nue": "NUE",
    "lat_sinal": "Sinal Latitude",
    "lat_grau": "Grau Latitude",
    "lat_min": "Minuto Latitude",
    "lat_seg": "Segundo Latitude",
    "lon_sinal": "Sinal Longitude",
    "lon_grau": "Grau Longitude",
    "lon_min": "Minuto Longitude",
    "lon_seg": "Segundo Longitude",
    "informante": "Informante Nome",
    "siape": "Informante Siape",
    "descricao": "Descrição",
    "localizacao": "Localização",
    "campanha": "Campanha",
    "data_levantamento": "Data de Levantamento",
    "data_critica": "Data de Crítica",
    "municipio":"Município",
    "uf":"UF",
}

COLUNAS_BOOLEANAS: Final[list[str]]  = [
    "is_ocup_gps", 
    "is_ocup_mira", 
    "is_ocup_gravimetro", 
    "is_atualizar_coord"
]

COLUNA_CHAVE_LOGICA: Final[str]  = "cod_estacao"

COLUNA_VERSAO: Final[str]  = "versao_app"

STATUS_MAP = {
     None: "Não Criticado GGC/GLGC",
      "": "(_) Não Criticado GGC/GLGC",
     "1": "(1) Liberado GGC/GLGC",
     "2": "(2) Análise Projeto (Retido/Criticado)",
     "3": "(3) Liberado Projeto",
     "4": "(4) Atualizado BDG",
     "5": "(5) Pendente/Reservado"
}

COLUNAS_NOMES: Final[list[str]] = [
    campo.name for campo in fields(Registro)
]
