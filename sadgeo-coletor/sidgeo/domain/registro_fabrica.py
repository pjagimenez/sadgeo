# -*- coding: utf-8 -*-
"""
file: /sidgeo/registro_fabrica.py
@created: 26-02-2025 pjag
@updated: 03-07-2026 pjag Refatoração MVC, GRASP, PEP8 pythonic
"""
from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from sidgeo.domain.registro import Registro

from sidgeo.util.settings import APP_VERSAO
from sidgeo.util.parsing import  (parse_data, str_para_bool, safe_int, safe_float)


class RegistroFabrica:
    """Fábrica responsável por criar objetos Registro a partir de dicionários."""

    @staticmethod
    def _normalizar_texto(valor: Any) -> str:
        if valor is None:
            return ""
        return str(valor).strip()

    @staticmethod
    def _normalizar_codigo(valor: Any) -> str:
        if valor is None:
            return ""
        return str(valor).strip().upper()

    @staticmethod
    def criar(dados: Mapping[str, Any]) -> Registro:
        """Metodo para criar uma registro a partir de um conjunto/array de valores"""
        
        texto = RegistroFabrica._normalizar_texto
        codigo = RegistroFabrica._normalizar_codigo

        return Registro(
            versao_app=texto(dados.get("versao_app", APP_VERSAO)),
            cod_estacao=codigo(dados.get("cod_estacao", "")),
            monumentacao=codigo(dados.get("monumentacao", "")),
            tipo_local=codigo(dados.get("tipo_local", "")),
            inscr_chapa=texto(dados.get("inscr_chapa", "")),
            situacao=codigo(dados.get("situacao", "")),
            conexao=codigo(dados.get("conexao", "")),
            tipo_conexao=codigo(dados.get("tipo_conexao", "")),
            rn_anterior=texto(dados.get("rn_anterior", "")),
            campanha=texto(dados.get("campanha", "")),
            data_levantamento=parse_data(dados.get("data_levantamento")),
            data_critica=parse_data(dados.get("data_critica")),
            projeto=texto(dados.get("projeto", "")),
            nue=texto(dados.get("nue", "")),
            linha=texto(dados.get("linha", "")),
            caderneta=texto(dados.get("caderneta", "")),
            informante=texto(dados.get("informante", "")),
            siape=texto(dados.get("siape", "")),
            tipo_fonte_coord=codigo(dados.get("tipo_fonte_coord", "")),
            lat_sinal=codigo(dados.get("lat_sinal", "")),
            lat_grau=safe_int(dados.get("lat_grau", 0)),
            lat_min=safe_int(dados.get("lat_min", 0)),
            lat_seg=safe_float(dados.get("lat_seg", 0)),
            lon_sinal=codigo(dados.get("lon_sinal", "")),
            lon_grau=safe_int(dados.get("lon_grau", 0)),
            lon_min=safe_int(dados.get("lon_min", 0)),
            lon_seg=safe_float(dados.get("lon_seg", 0)),
            is_atualizar_coord=str_para_bool(
                dados.get("is_atualizar_coord", "")
            ),
            is_ocup_gps=str_para_bool(dados.get("is_ocup_gps", "")),
            is_ocup_mira=str_para_bool(dados.get("is_ocup_mira", "")),
            is_ocup_gravimetro=str_para_bool(
                dados.get("is_ocup_gravimetro", "")
            ),
            descricao=texto(dados.get("descricao", "")),
            localizacao=texto(dados.get("localizacao", "")),
            itinerario=texto(dados.get("itinerario", "")),
            observacao=texto(dados.get("observacao", "")),
            seq=texto(dados.get("seq", "")),
            status_vrf=codigo(dados.get("status_vrf", "")),
            municipio=texto(dados.get("municipio", "")),
            uf=codigo(dados.get("uf", "")),
        )

    @staticmethod
    def codigo_por_descricao(
        dicionario: Mapping[str, str],
        descricao: str | None,
    ) -> str:
        """
        Retorna o código correspondente a uma descrição.

        Exemplo:
            {"1": "Ativo"} + "Ativo" -> "1"
        """
        if not descricao:
            return ""

        descricao_normalizada = descricao.strip().lower()

        for codigo, texto in dicionario.items():
            if texto.strip().lower() == descricao_normalizada:
                return str(codigo)

        return ""
