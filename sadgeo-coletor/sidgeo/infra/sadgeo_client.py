# -*- coding: utf-8 -*-
"""
file: /sidgeo/infra/sadgeo_client.py
@created: 09-09-2025 pjag
@updated: 03-07-2026 pjag Refatoração MVC, GRASP, PEP8 pythonic
"""

from __future__ import annotations

from typing import Any
import logging

import requests

from sidgeo.infra.erros_integracao import IntegracaoErro
from sidgeo.util.settings import APP_SIGLA

_LOG = logging.getLogger(APP_SIGLA)


class SadgeoClient:
    """Cliente fino para a API do SADGEO."""

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
        codigo = cod_estacao.strip().upper()
        url = f"{self.base_url}/itemsadgeo/filtrar/estacao/{codigo}"
        _LOG.info("SADGEO GET %s", url)

        try:
            response = self._session.get(
                url,
                timeout=self.timeout_s,
                verify=self.verificar_tls,
            )
            _LOG.info("SADGEO resposta: HTTP %s | %s", response.status_code, response.url)
            response.raise_for_status()
            return response.json()

        except requests.Timeout as erro:
            _LOG.exception("SADGEO timeout | %s", url)
            raise IntegracaoErro(
                f"Tempo esgotado ao consultar SADGEO para estação {codigo}."
            ) from erro

        except requests.exceptions.SSLError as erro:
            _LOG.exception("SADGEO falha TLS/certificado | %s", url)
            raise IntegracaoErro("Falha no certificado HTTPS do SADGEO. Confira a cadeia institucional e REQUESTS_CA_BUNDLE.") from erro

        except requests.ConnectionError as erro:
            _LOG.exception("SADGEO falha de conexão/DNS/proxy | %s", url)
            raise IntegracaoErro(
                "Não foi possível conectar ao serviço SADGEO."
            ) from erro

        except requests.HTTPError as erro:
            status = erro.response.status_code if erro.response is not None else "desconhecido"
            raise IntegracaoErro(
                f"Erro HTTP {status} ao consultar SADGEO para estação {codigo}. URL: {url}"
            ) from erro

        except requests.JSONDecodeError as erro:
            _LOG.exception("SADGEO resposta não é JSON | %s", url)
            raise IntegracaoErro(
                "Resposta inválida do SADGEO: JSON malformado."
            ) from erro

        except requests.RequestException as erro:
            _LOG.exception("SADGEO falha na requisição | %s", url)
            raise IntegracaoErro(
                f"Falha inesperada ao consultar SADGEO: {erro}"
            ) from erro
