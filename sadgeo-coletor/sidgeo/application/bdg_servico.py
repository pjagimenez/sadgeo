# -*- coding: utf-8 -*-
"""
file: /sidgeo/application/bdg_servico.py
@created: 03-07-2026 pjag
@updated: 03-07-2026 pjag Refatoração MVC, GRASP, PEP8 pythonic
"""

from __future__ import annotations

from sidgeo.domain.registro import Registro
from sidgeo.domain.registro_mapeador import RegistroMapeador
from sidgeo.infra.bdg_client import BdgClient


class BdgServico:
    """Serviço de aplicação para consulta e conversão de dados do BDG."""

    def __init__(
        self,
        bdg_client: BdgClient,
        registro_mapeador: RegistroMapeador,
    ) -> None:
        self.bdg_client = bdg_client
        self.registro_mapeador = registro_mapeador

    def buscar_registro_por_estacao(self, codigo: str) -> Registro:
        json_bdg = self.bdg_client.filtrar_por_estacao(codigo)
        return self.registro_mapeador.dict_bdg_para_registro(json_bdg)