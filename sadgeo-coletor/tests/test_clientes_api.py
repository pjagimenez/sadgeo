"""Contrato HTTP das consultas: rotas reais informadas pela área usuária e erros de integração."""
from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import logging
from threading import Thread
from unittest.mock import Mock

import pytest
import requests

from sidgeo.application.bdg_servico import BdgServico
from sidgeo.domain.registro_mapeador import RegistroMapeador
from sidgeo.infra.bdg_client import BdgClient
from sidgeo.infra.sadgeo_client import SadgeoClient
from sidgeo.infra.erros_integracao import IntegracaoErro
from sidgeo.util.settings import APP_URL_BDG, APP_URL_SADGEO

BDG_ESTACAO = {
    'codigoEstacao': '3677J', 'latitudeGMS': '07° 41\' 07" S',
    'longitudeGMS': '39° 00\' 21" W', 'fonteCoordenada': 'GPS Navegação',
}


@contextmanager
def api_local(caminho_esperado, dados, status=200):
    acessos = []
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            acessos.append(self.path)
            self.send_response(status if self.path == caminho_esperado else 404)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(dados).encode())
        def log_message(self, *args):
            pass
    servidor = HTTPServer(('127.0.0.1', 0), Handler)
    thread = Thread(target=servidor.serve_forever, daemon=True)
    thread.start()
    try:
        yield f'http://127.0.0.1:{servidor.server_port}', acessos
    finally:
        servidor.shutdown()
        thread.join(timeout=2)
        servidor.server_close()


@pytest.mark.parametrize('resposta', [[BDG_ESTACAO], {'content': [BDG_ESTACAO]}, BDG_ESTACAO])
def test_bdg_rota_query_e_conversao_real_http(resposta):
    with api_local('/api/v1/bdg/estacoes?codigoEstacao=3677J', resposta) as (host, acessos):
        cliente = BdgClient(host + '/api/v1/bdg/')
        cliente._session.trust_env = False
        registro = BdgServico(cliente, RegistroMapeador()).buscar_registro_por_estacao(' 3677j ')
    assert acessos == ['/api/v1/bdg/estacoes?codigoEstacao=3677J']
    assert registro.cod_estacao == '3677J'
    assert registro.lat_grau == 7 and registro.lat_sinal == '-'
    assert registro.tipo_fonte_coord == '26'


def test_sadgeo_rota_real_http_preservada():
    resposta = {'resultado': 'sucesso', 'dados': [{'codEstacao': '3677J'}]}
    with api_local('/api/itemsadgeo/filtrar/estacao/3677J', resposta) as (host, acessos):
        cliente = SadgeoClient(host + '/api/')
        cliente._session.trust_env = False
        assert cliente.filtrar_por_estacao(' 3677j ') == resposta
    assert acessos == ['/api/itemsadgeo/filtrar/estacao/3677J']


def test_bases_institucionais_geram_as_urls_informadas():
    bdg = requests.Request('GET', APP_URL_BDG + '/estacoes', params={'codigoEstacao': '3677J'}).prepare()
    assert bdg.url == 'http://w3.servicoscged.ibge.gov.br/api/v1/bdg/estacoes?codigoEstacao=3677J'
    assert APP_URL_SADGEO + '/itemsadgeo/filtrar/estacao/3677J' == 'https://w3.api-sadgeo.ibge.gov.br/api/itemsadgeo/filtrar/estacao/3677J'


def test_bdg_colecao_vazia_e_selecao_da_estacao_correta():
    cliente = BdgClient(APP_URL_BDG)
    resposta = Mock(status_code=200, url='http://exemplo/estacoes')
    cliente._session.get = Mock(return_value=resposta)
    resposta.json.return_value = []
    assert cliente.filtrar_por_estacao('3677J') == {}
    resposta.json.return_value = [{'codigoEstacao': 'OUTRA'}, BDG_ESTACAO]
    assert cliente.filtrar_por_estacao('3677J') == BDG_ESTACAO
    resposta.json.return_value = [BDG_ESTACAO, BDG_ESTACAO]
    with pytest.raises(IntegracaoErro, match='ambígua'):
        cliente.filtrar_por_estacao('3677J')


@pytest.mark.parametrize('resposta', [None, 'html', {'erro': 'falha'}, {'content': None}, [None]])
def test_bdg_resposta_invalida_nao_vira_estacao_zerada(resposta):
    cliente = BdgClient(APP_URL_BDG)
    retorno = Mock(status_code=200, url='http://exemplo/estacoes')
    retorno.json.return_value = resposta
    cliente._session.get = Mock(return_value=retorno)
    with pytest.raises(IntegracaoErro, match='Resposta inválida'):
        cliente.filtrar_por_estacao('3677J')


@pytest.mark.parametrize('tipo', [BdgClient, SadgeoClient])
@pytest.mark.parametrize('status', [403, 404, 500])
def test_status_http_nao_e_ocultado(tipo, status):
    cliente = tipo('https://exemplo/api')
    retorno = requests.Response()
    retorno.status_code = status
    retorno.url = 'https://exemplo/api/consulta'
    cliente._session.get = Mock(return_value=retorno)
    with pytest.raises(IntegracaoErro, match=f'HTTP {status}'):
        cliente.filtrar_por_estacao('3677J')


@pytest.mark.parametrize('tipo', [BdgClient, SadgeoClient])
def test_tls_diferenciado_de_falha_generica(tipo, caplog):
    caplog.set_level(logging.INFO, logger='SIDGEO')
    cliente = tipo('https://exemplo/api')
    cliente._session.get = Mock(side_effect=requests.exceptions.SSLError('certificado de teste'))
    with pytest.raises(IntegracaoErro, match='certificado HTTPS'):
        cliente.filtrar_por_estacao('3677J')
    assert 'GET https://exemplo/api/' in caplog.text
    assert 'TLS/certificado' in caplog.text


def test_payload_bdg_informado_pelo_usuario():
    # Campos e formatos do retorno real de 3677J; sem textos descritivos/localização.
    dados = [{
        'codigoEstacao': '3677J', 'tipoEstacao': 'R', 'tema': 'RN', 'nomeEstacao': '3677J',
        'dataVisita': '03/12/2018', 'situacao': 'BOM', 'tipoLocal': 'PT',
        'latitude': -8.7003722222, 'longitude': -35.155475,
        'latitudeGMS': ' 08º 42\' 01,34"  S', 'longitudeGMS': ' 35º 09\' 19,71" W',
        'fonteCoordenada': 'GPS Navegação', 'dataMedicaoCoordenada': '03/12/2018',
        'dataCalculoCoordenada': '', 'sistemaReferenciaCoordenada': 'SIRGAS2000',
        'municipio': {'nomeMunicipio': 'Rio Formoso', 'geocodigo': '2611903',
                      'uf': {'sigla': 'PE', 'nomeUF': 'Pernambuco'}},
    }]
    with api_local('/api/v1/bdg/estacoes?codigoEstacao=3677J', dados) as (host, _):
        from datetime import datetime
        from sidgeo.domain.coordenadas import coordenadas_decimais
        cliente = BdgClient(host + '/api/v1/bdg')
        cliente._session.trust_env = False
        registro = BdgServico(cliente, RegistroMapeador()).buscar_registro_por_estacao('3677J')
    assert coordenadas_decimais(registro) == pytest.approx((-8.7003722222, -35.155475), abs=1e-9)
    assert registro.data_coordenada == datetime(2018, 12, 3)
    assert registro.tipo_fonte_coord == '26'
    assert registro.uf == 'PE' and registro.municipio == 'Rio Formoso'


def test_data_medicao_coordenada_independe_da_visita_e_do_calculo():
    from datetime import datetime
    registro = RegistroMapeador().dict_bdg_para_registro({
        **BDG_ESTACAO, 'dataVisita': '01/01/2020', 'dataCalculoCoordenada': '01/02/2020',
        'dataMedicaoCoordenada': '03/12/2018', 'dataCoordenada': '01/03/2020',
    })
    assert registro.data_coordenada == datetime(2018, 12, 3)
    assert registro.data_levantamento == datetime(2020, 1, 1)
