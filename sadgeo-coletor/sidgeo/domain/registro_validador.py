# -*- coding: utf-8 -*-
"""
file: /sidgeo/domain/registro_validador.py
@created: 12-09-2025 pjag
@updated: 03-07-2026 pjag Refatoração MVC, GRASP, PEP8 pythonic
"""

from __future__ import annotations

from sidgeo.domain.erros import ValidacaoErro
from sidgeo.domain.registro import Registro


class RegistroValidador:
    """Validador das regras de negócio de Registro."""

    @classmethod
    def validar(cls, registro: Registro) -> None:
        """Validar a linha completa de registro."""
        cls._validar_codigo(registro.cod_estacao)
        cls._validar_conexao(registro)

    @staticmethod
    def _validar_codigo(codigo: str) -> None:
        if not codigo:
            raise ValidacaoErro("Identificação da Estação é obrigatória.")

    @staticmethod
    def _validar_conexao(registro: Registro) -> None:
        if bool(registro.conexao) != bool(registro.tipo_conexao):
            raise ValidacaoErro(
                "Conexão e Tipo de Conexão devem ser informados em conjunto."
            )
