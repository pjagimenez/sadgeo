# -*- coding: utf-8 -*-
"""
file: /sidgeo/infra/bdg_client.py
@created: 16-10-2025 pjag
@updated: 03-07-2026 pjag Refatoração MVC, GRASP, PEP8 pythonic
"""
from __future__ import annotations

from typing import Any
import requests

from sidgeo.infra.erros_integracao import IntegracaoErro

# pylint: disable=too-few-public-methods

class BdgClient:
    """Cliente fino para a API do BDG."""

    def __init__(
        self,
        base_url: str,
        verificar_tls: bool = True,
        timeout_s: int = 15,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.verificar_tls = verificar_tls
        self.timeout_s = timeout_s
        self._session = requests.Session()

    def filtrar_por_estacao(self, cod_estacao: str) -> dict[str, Any]:
        """Filtra os registros na API do BDG pelo código da estação."""
        codigo = cod_estacao.strip().upper()
        url = f"{self.base_url}/estacao/{codigo}"

        try:
            response = self._session.get(
                url,
                timeout=self.timeout_s,
                verify=self.verificar_tls,
            )
            response.raise_for_status()
            return response.json()

        except requests.Timeout as erro:
            raise IntegracaoErro(
                f"Tempo esgotado ao consultar BDG para estação {codigo}."
            ) from erro

        except requests.ConnectionError as erro:
            raise IntegracaoErro(
                "Não foi possível conectar ao serviço BDG."
            ) from erro

        except requests.HTTPError as erro:
            status = erro.response.status_code if erro.response is not None else "desconhecido"
            raise IntegracaoErro(
                f"Erro HTTP {status} ao consultar BDG para estação {codigo}."
            ) from erro

        except requests.JSONDecodeError as erro:
            raise IntegracaoErro(
                "Resposta inválida do BDG: JSON malformado."
            ) from erro

        except requests.RequestException as erro:
            raise IntegracaoErro(
                f"Falha inesperada ao consultar BDG: {erro}"
            ) from erro
