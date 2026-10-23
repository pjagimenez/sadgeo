from dataclasses import asdict
from datetime import datetime
from unittest.mock import Mock

import pytest

from sidgeo.application.bdg_servico import BdgServico
from sidgeo.domain.registro_fabrica import RegistroFabrica
from sidgeo.domain.registro_mapeador import RegistroMapeador
from sidgeo.domain.coordenadas import diferenca_horizontal_m
from sidgeo.domain.erros import ValidacaoErro
from sidgeo.infra.erros_integracao import IntegracaoErro
from sidgeo.util.geofuncoes import parse_gms


@pytest.mark.parametrize('texto', ['07° 41\' 07" S', '07º41\'07,0"S', 'S 07 41 07', '07° 41′ 07″ S'])
def test_gms_formatos_legados(texto):
    assert parse_gms(texto) == dict(sinal='-', grau=7, min=41, seg=7.0)


@pytest.mark.parametrize('texto', ['coordenada inválida', '07° 61\' 07" S', '07° 41\' 99" S', 'N 07 41 07 S'])
def test_gms_invalido_nao_vira_zero(texto):
    with pytest.raises(ValueError):
        parse_gms(texto)


def test_bdg_mapeamento_data_fonte_e_diferenca():
    client = Mock()
    client.filtrar_por_estacao.return_value = dict(codigoEstacao='422V', latitudeGMS='07° 41\' 07" S',
        longitudeGMS='39° 00\' 21" W', fonteCoordenada='GPS Navegação', dataCoordenada='04/12/2009')
    registro = BdgServico(client, RegistroMapeador()).buscar_registro_por_estacao('422V')
    assert registro.lat_sinal == registro.lon_sinal == '-'
    assert registro.tipo_fonte_coord == '26'
    assert registro.data_coordenada == datetime(2009, 12, 4)
    assert diferenca_horizontal_m(registro, registro) == 0
    novo = RegistroFabrica.criar(dict(cod_estacao='422V', lat_sinal='S', lat_grau=8, lon_sinal='W', lon_grau=39))
    assert diferenca_horizontal_m(registro, novo) > 30_000


def test_bdg_recusa_coordenadas_ausentes():
    client = Mock()
    client.filtrar_por_estacao.return_value = {'codigoEstacao': '422V'}
    with pytest.raises(IntegracaoErro, match='Coordenadas'):
        BdgServico(client, RegistroMapeador()).buscar_registro_por_estacao('422V')
    client.filtrar_por_estacao.return_value = {}
    assert BdgServico(client, RegistroMapeador()).buscar_registro_por_estacao('422V') is None


@pytest.mark.parametrize('login', ['nome.sobrenome', 'nome_sobrenome', 'login123', 'nome-sobrenome'])
def test_login_valido_persistido(controller, login):
    reg = RegistroFabrica.criar(dict(cod_estacao='422V', informante=login, unidade_informante='CGED/GSD'))
    controller.salvar_registro(reg)
    assert asdict(controller.buscar_registro('422V')) == asdict(reg)


@pytest.mark.parametrize('login', ['Nome Completo', 'nome@ibge.gov.br', 'dominio\\usuario', '.nome', 'nome..sobrenome'])
def test_login_invalido_barrado_no_servico(controller, login):
    with pytest.raises(ValidacaoErro, match='login de rede'):
        controller.salvar_registro(RegistroFabrica.criar(dict(cod_estacao='422V', informante=login)))
    assert controller.listar_registros() == []


def test_unidade_fora_da_lista(controller):
    with pytest.raises(ValidacaoErro, match='Unidade'):
        controller.salvar_registro(RegistroFabrica.criar(dict(cod_estacao='422V', unidade_informante='Outra')))


def test_primeira_data_coordenada_em_base_legada(controller, tmp_path, logger):
    import pandas as pd
    from sidgeo.application.controller_fabrica import ControllerFactory
    # Reproduz o HDF5 anterior, sem as novas colunas de unidade/data/fotos.
    pd.DataFrame([{'cod_estacao': '422V', 'descricao': 'Preservar'}]).to_hdf(tmp_path / 'sidgeo.h5', key='dados')
    reaberto = ControllerFactory.criar(logger, data_dir=tmp_path)
    registro = reaberto.buscar_registro('422V')
    registro.unidade_informante = 'CGED/GSD'
    registro.data_coordenada = datetime(2009, 12, 4)
    reaberto.salvar_registro(registro)
    salvo = ControllerFactory.criar(logger, data_dir=tmp_path).buscar_registro('422V')
    assert salvo.data_coordenada == datetime(2009, 12, 4)
    assert salvo.unidade_informante == 'CGED/GSD'
    assert salvo.descricao == 'Preservar'
    assert salvo.fotos == []
