# -*- coding: utf-8 -*-
"""
file: /sidgeo/util/strings.py
@created: 24-03-2025 pjag
@updated: 03-07-2026 pjag Refatoração MVC, GRASP, PEP8 pythonic
"""

from __future__ import annotations


def tratar_texto_sql(texto):
    """Prepara um campo de texto para ser usado com segurança em comandos SQL."""
    if texto is None or str(texto).strip() == '':
        return "' '" # Retorna uma string com espaço entre aspas simples
    texto = str(texto).replace("'", "").replace('"', '') # Escapa aspas simples e remove aspas duplas
    return f"'{texto}'" if texto.strip() else "null"
