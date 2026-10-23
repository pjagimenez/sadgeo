# -*- coding: utf-8 -*-
"""
file: /sidgeo/imagem/imagem_parser_nome.py
@created: 29-09-2026 pjag
@updated: 29-09-2026 pjag
"""
import os
import re

from imagem_model import (
    IdentificacaoImagem,
    TipoImagem
)


class NomeArquivoParser:

    REGEX_SADGEO = re.compile(
        r'^(?P<seq>\d+)-(?P<ano>\d{2})_(?P<restante>.+)$'
    )

    VALIDACAO_ESTACAO = re.compile(
        r'^\d[A-Z0-9]*$'
    )

    @classmethod
    def identificar(
        cls,
        nome_arquivo: str
    ) -> IdentificacaoImagem:

        nome = os.path.basename(nome_arquivo)

        sem_ext = re.sub(
            r'\.[^.]+$',
            '',
            nome
        )

        origem_sadgeo = False

        m = cls.REGEX_SADGEO.match(sem_ext)

        if m:
            origem_sadgeo = True
            sem_ext = m.group("restante")

        if sem_ext.startswith("I"):

            codigo = sem_ext[1:]

            cls._validar(codigo)

            return IdentificacaoImagem(
                nome_arquivo_original=nome,
                codigo_estacao=codigo,
                tipo_imagem=TipoImagem.CROQUI,
                origem_sadgeo=origem_sadgeo
            )

        if sem_ext.endswith("c"):

            codigo = sem_ext[:-1]

            cls._validar(codigo)

            return IdentificacaoImagem(
                nome_arquivo_original=nome,
                codigo_estacao=codigo,
                tipo_imagem=TipoImagem.CHAPA,
                origem_sadgeo=origem_sadgeo
            )

        if sem_ext.endswith("s"):

            codigo = sem_ext[:-1]

            cls._validar(codigo)

            return IdentificacaoImagem(
                nome_arquivo_original=nome,
                codigo_estacao=codigo,
                tipo_imagem=TipoImagem.SITUACAO,
                origem_sadgeo=origem_sadgeo
            )

        codigo = sem_ext

        cls._validar(codigo)

        return IdentificacaoImagem(
            nome_arquivo_original=nome,
            codigo_estacao=codigo,
            tipo_imagem=TipoImagem.PANORAMICA,
            origem_sadgeo=origem_sadgeo
        )

    @classmethod
    def _validar(cls, codigo: str):

        if not cls.VALIDACAO_ESTACAO.match(codigo):
            raise ValueError(
                f"Código da estação inválido: {codigo}"
            )