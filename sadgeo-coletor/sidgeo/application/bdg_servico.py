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
from sidgeo.domain.coordenadas import coordenadas_decimais
from sidgeo.infra.erros_integracao import IntegracaoErro


class BdgServico:
    """Serviço de aplicação para consulta e conversão de dados do BDG."""

    def __init__(
        self,
        bdg_client: BdgClient,
        registro_mapeador: RegistroMapeador,
    ) -> None:
        self.bdg_client = bdg_client
        self.registro_mapeador = registro_mapeador

    def buscar_registro_por_estacao(self, codigo: str) -> Registro | None:
        json_bdg = self.bdg_client.filtrar_por_estacao(codigo)
        if not json_bdg:
            return None
        try:
            registro = self.registro_mapeador.dict_bdg_para_registro(json_bdg)
            coordenadas_decimais(registro)
            if registro.cod_estacao and registro.cod_estacao != codigo.strip().upper():
                raise ValueError("O serviço retornou outra estação.")
            return registro
        except (ValueError, TypeError) as erro:
            raise IntegracaoErro(f"Coordenadas do BDG para {codigo} não puderam ser utilizadas: {erro}") from erro
