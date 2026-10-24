# -*- coding: utf-8 -*-
"""
file: /sidgeo/infra/bdg_client.py
@created: 16-10-2025 pjag
@updated: 03-07-2026 pjag Refatoração MVC, GRASP, PEP8 pythonic
"""
from __future__ import annotations

from typing import Any, cast
import logging
import requests

from sidgeo.infra.erros_integracao import IntegracaoErro
from sidgeo.util.settings import APP_SIGLA

_LOG = logging.getLogger(APP_SIGLA)

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
        url = f"{self.base_url}/estacoes"
        parametros = {"codigoEstacao": codigo}
        url_consulta = requests.Request("GET", url, params=parametros).prepare().url
        _LOG.info("BDG GET %s", url_consulta)

        try:
            response = self._session.get(
                url,
                params=parametros,
                timeout=self.timeout_s,
                verify=self.verificar_tls,
            )
            _LOG.info("BDG resposta: HTTP %s | %s", response.status_code, response.url)
            response.raise_for_status()
            dados = response.json()
            return self._selecionar_estacao(dados, codigo)

        except requests.Timeout as erro:
            _LOG.exception("BDG timeout | %s", url_consulta)
            raise IntegracaoErro(
                f"Tempo esgotado ao consultar BDG para estação {codigo}."
            ) from erro

        except requests.exceptions.SSLError as erro:
            _LOG.exception("BDG falha TLS/certificado | %s", url_consulta)
            raise IntegracaoErro("Falha no certificado HTTPS do BDG. Confira a cadeia institucional e REQUESTS_CA_BUNDLE.") from erro

        except requests.ConnectionError as erro:
            _LOG.exception("BDG falha de conexão/DNS/proxy | %s", url_consulta)
            raise IntegracaoErro(
                "Não foi possível conectar ao serviço BDG."
            ) from erro

        except requests.HTTPError as erro:
            status = erro.response.status_code if erro.response is not None else "desconhecido"
            raise IntegracaoErro(
                f"Erro HTTP {status} ao consultar BDG para estação {codigo}. URL: {url_consulta}"
            ) from erro

        except requests.JSONDecodeError as erro:
            _LOG.exception("BDG resposta não é JSON | %s", url_consulta)
            raise IntegracaoErro(
                "Resposta inválida do BDG: JSON malformado."
            ) from erro

        except requests.RequestException as erro:
            _LOG.exception("BDG falha na requisição | %s", url_consulta)
            raise IntegracaoErro(
                f"Falha inesperada ao consultar BDG: {erro}"
            ) from erro

    @staticmethod
    def _selecionar_estacao(dados: Any, codigo: str) -> dict[str, Any]:
        """A consulta de coleção pode retornar uma lista, uma página ou o objeto da estação."""
        if isinstance(dados, dict):
            objeto = cast(dict[str, Any], dados)
            if "content" in objeto:
                dados = objeto["content"]
            elif "codigoEstacao" in objeto:
                return objeto
            else:
                raise IntegracaoErro("Resposta inválida do BDG: objeto sem codigoEstacao ou content.")
        if not isinstance(dados, list):
            raise IntegracaoErro("Resposta inválida do BDG: esperada uma lista de estações.")
        encontrados: list[dict[str, Any]] = []
        for item in cast(list[Any], dados):
            if not isinstance(item, dict):
                raise IntegracaoErro("Resposta inválida do BDG: estação sem codigoEstacao.")
            estacao = cast(dict[str, Any], item)
            if not estacao.get("codigoEstacao"):
                raise IntegracaoErro("Resposta inválida do BDG: estação sem codigoEstacao.")
            if str(estacao["codigoEstacao"]).strip().upper() == codigo:
                encontrados.append(estacao)
        if len(encontrados) > 1:
            raise IntegracaoErro(f"O BDG retornou mais de um registro para a estação {codigo}; a seleção é ambígua.")
        return encontrados[0] if encontrados else {}
