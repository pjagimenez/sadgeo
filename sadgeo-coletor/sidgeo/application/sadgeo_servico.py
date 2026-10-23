# -*- coding: utf-8 -*-
"""
file: /sidgeo/application/sadgeo_servico.py
@created: 03-07-2026 pjag
@updated: 03-07-2026 pjag Refatoração MVC, GRASP, PEP8 pythonic
"""

from __future__ import annotations

from typing import Any, cast

from sidgeo.domain.registro import Registro
from sidgeo.domain.registro_mapeador import RegistroMapeador
from sidgeo.infra.sadgeo_client import SadgeoClient


class SadgeoServico:
    """Serviço de aplicação para consulta e conversão de dados do SADGEO."""

    def __init__(
        self,
        sadgeo_client: SadgeoClient,
        registro_mapeador: RegistroMapeador,
    ) -> None:
        self.sadgeo_client = sadgeo_client
        self.registro_mapeador = registro_mapeador

    def buscar_por_estacao(self, codigo: str) -> list[Registro]:
        resposta = self.sadgeo_client.filtrar_por_estacao(codigo)

        if resposta.get("resultado") != "sucesso":
            return []
        
        dados =  cast(
            list[dict[str, Any]],
            resposta.get("dados", [])
        )


        return [
            self.registro_mapeador.dict_sadgeo_para_registro(item) 
            for item in dados
        ]

    def converter_para_registro(self, dados_sadgeo: dict[str, Any]) -> Registro:
        return self.registro_mapeador.dict_sadgeo_para_registro(dados_sadgeo)