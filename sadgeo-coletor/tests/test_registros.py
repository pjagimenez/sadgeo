from dataclasses import asdict
from decimal import Decimal
import warnings

import pandas as pd
import pytest

from sidgeo.application.controller_fabrica import ControllerFactory
from sidgeo.domain.erros import ValidacaoErro
from sidgeo.domain.registro_fabrica import RegistroFabrica
from sidgeo.infra.persistencia_hdf import HdfDataStore
from sidgeo.util.parsing import parse_coordinate


def exemplo(**alteracoes):
    dados = dict(cod_estacao='1234A', campanha='medA', tipo_fonte_coord='01',
                 monumentacao='01', data_levantamento='23/10/2026', lat_sinal='-',
                 lat_grau=22, lat_min=10, lat_seg='12,345678', lon_sinal='-',
                 lon_grau=43, lon_min=15, lon_seg='25,678', is_ocup_gps=True,
                 descricao='Marco de teste; descrição com acentos', uf='RJ')
    dados.update(alteracoes)
    return RegistroFabrica.criar(dados)


@pytest.mark.parametrize('formato', ['csv', 'json'])
def test_edicao_reabertura_e_exportacao(controller, logger, tmp_path, formato):
    registro = exemplo()
    controller.salvar_registro(registro)
    reaberto = ControllerFactory.criar(logger, data_dir=tmp_path)
    registro.descricao = 'Descrição revista'
    reaberto.salvar_registro(registro)
    assert asdict(reaberto.buscar_registro('1234A')) == asdict(registro)
    assert len(reaberto.listar_registros()) == 1
    arquivo = tmp_path / f'exportado.{formato}'
    reaberto.exportar(str(arquivo), formato)
    reaberto.zerar_base_registro()
    assert reaberto.listar_registros() == []
    assert reaberto.importar(str(arquivo), formato) == 1
    importado = reaberto.buscar_registro('1234A')
    assert asdict(importado) == asdict(registro)
    assert reaberto.excluir_registro('1234A')
    assert not reaberto.excluir_registro('1234A')
    assert ControllerFactory.criar(logger, data_dir=tmp_path).listar_registros() == []


def test_csv_esparso_preserva_codigos_e_campos_vazios(controller, tmp_path):
    arquivo = tmp_path / 'esparso.csv'
    arquivo.write_text('cod_estacao;tipo_fonte_coord;monumentacao\n1234A;01;02\n', encoding='utf-8')
    assert controller.importar(str(arquivo), 'csv') == 1
    registro = controller.buscar_registro('1234A')
    assert registro.tipo_fonte_coord == '01'
    assert registro.monumentacao == '02'
    assert registro.descricao == registro.conexao == registro.seq == ''
    assert registro.data_critica is None
    assert registro.lat_grau == 0


def test_importacao_conta_atualizacao(controller, tmp_path):
    controller.salvar_registro(exemplo())
    arquivo = tmp_path / 'atualizado.csv'
    arquivo.write_text('cod_estacao;descricao\n1234A;Atualizado\n2345B;Novo\n', encoding='utf-8')
    assert controller.importar(str(arquivo), 'csv') == 2
    assert len(controller.listar_registros()) == 2
    assert controller.buscar_registro('1234A').descricao == 'Atualizado'


def test_importacao_parcial_informa_erros(controller, tmp_path):
    arquivo = tmp_path / 'parcial.csv'
    arquivo.write_text('cod_estacao;descricao\n1234A;Correto\n;Sem código\n', encoding='utf-8')
    with pytest.raises(ValidacaoErro, match='Processados 1'):
        controller.importar(str(arquivo), 'csv')
    assert controller.buscar_registro('1234A') is not None
    assert len(controller.listar_registros()) == 1


def test_falha_de_gravacao_preserva_arquivo_e_memoria(controller, tmp_path, monkeypatch):
    controller.salvar_registro(exemplo())
    original = (tmp_path / 'sidgeo.h5').read_bytes()
    def falhar(*args, **kwargs):
        raise OSError('Disco indisponível')
    monkeypatch.setattr(pd.DataFrame, 'to_hdf', falhar)
    with pytest.raises(RuntimeError, match='Disco indisponível'):
        controller.salvar_registro(exemplo(descricao='Não deve substituir a versão salva'))
    assert (tmp_path / 'sidgeo.h5').read_bytes() == original
    assert controller.buscar_registro('1234A').descricao == exemplo().descricao
    assert list(tmp_path.glob('sidgeo-*.h5')) == []


def test_hdf_invalido_nao_e_substituido(tmp_path):
    arquivo = tmp_path / 'invalido.h5'
    arquivo.write_bytes(b'Arquivo original a preservar')
    with pytest.raises(RuntimeError, match='preservado'):
        HdfDataStore(arquivo).carregar()
    assert arquivo.read_bytes() == b'Arquivo original a preservar'


def test_hdf_vazio_da_versao_anterior(tmp_path):
    arquivo = tmp_path / 'legado.h5'
    with warnings.catch_warnings():
        # O teste reproduz deliberadamente a gravação vazia da versão antiga.
        warnings.filterwarnings('ignore', message='Writing an empty DataFrame', category=UserWarning)
        pd.DataFrame().to_hdf(arquivo, key='dados', format='table')
    assert HdfDataStore(arquivo).carregar().empty


@pytest.mark.parametrize('conexao,tipo', [('1234A', ''), ('', 'RN')])
def test_conexao_exige_os_dois_campos(controller, conexao, tipo):
    with pytest.raises(ValidacaoErro, match='em conjunto'):
        controller.salvar_registro(exemplo(conexao=conexao, tipo_conexao=tipo))


def test_decimal_com_virgula():
    assert parse_coordinate('12,345678901') == Decimal('12.345678901')
    assert parse_coordinate('inválido') == Decimal('0')


@pytest.mark.parametrize('acao', ['excluir_registro', 'zerar_base_registro'])
def test_falha_ao_apagar_preserva_memoria_e_arquivo(controller, tmp_path, monkeypatch, acao):
    controller.salvar_registro(exemplo())
    original = (tmp_path / 'sidgeo.h5').read_bytes()
    def falhar(*args, **kwargs):
        raise OSError('Falha de gravação')
    monkeypatch.setattr(pd.DataFrame, 'to_hdf', falhar)
    argumentos = ['1234A'] if acao == 'excluir_registro' else []
    with pytest.raises(RuntimeError, match='Falha de gravação'):
        getattr(controller, acao)(*argumentos)
    assert controller.buscar_registro('1234A') is not None
    assert (tmp_path / 'sidgeo.h5').read_bytes() == original
