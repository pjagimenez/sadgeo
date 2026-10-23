# -*- coding: utf-8 -*-
"""
file: /sidgeo/domain/registro_validador.py
@created: 12-09-2025 pjag
@updated: 03-07-2026 pjag Refatoração MVC, GRASP, PEP8 pythonic
"""

from __future__ import annotations
import re

from sidgeo.domain.erros import ValidacaoErro
from sidgeo.domain.registro import Registro
from sidgeo.domain.informante import UNIDADES_INFORMANTE


class RegistroValidador:
    """Validador das regras de negócio de Registro."""

    @classmethod
    def validar(cls, registro: Registro) -> None:
        """Validar a linha completa de registro."""
        cls._validar_codigo(registro.cod_estacao)
        cls._validar_conexao(registro)
        cls.validar_informante(registro.informante)
        if registro.unidade_informante and registro.unidade_informante not in UNIDADES_INFORMANTE:
            raise ValidacaoErro("Unidade do informante inválida. Selecione uma unidade da lista.")

    @staticmethod
    def validar_informante(login: str) -> None:
        if login and not re.fullmatch(r"[A-Za-z0-9]+(?:[._-][A-Za-z0-9]+)*", login):
            raise ValidacaoErro(
                "Informante: use o login de rede, sem espaços. "
                "Exemplos: nome.sobrenome ou nome_sobrenome (letras, números, ponto, '_' ou '-')."
            )

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
