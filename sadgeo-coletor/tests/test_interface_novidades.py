from pathlib import Path
from unittest.mock import Mock

from PIL import Image
import pytest

from sidgeo.domain.registro_fabrica import RegistroFabrica
from sidgeo.view.ajuda_descritivo import AjudaDescritivo
from sidgeo.view.editar_foto import EditarFoto

pytestmark = pytest.mark.gui


def test_informante_unidade_e_link_reg(app, controller, monkeypatch):
    app.info_basicas.entry_estacao.insert(0, '422V')
    app.info_basicas.entry_informante.insert(0, 'Nome Completo')
    app.acao_salvar()
    assert controller.listar_registros() == []
    assert app.info_basicas.entry_informante.get() == 'Nome Completo'
    app.info_basicas.entry_informante.delete(0, 'end')
    app.info_basicas.entry_informante.insert(0, 'nome.sobrenome')
    app.info_basicas.combo_unidade_informante.set('SES-GO/GGC')
    app.acao_salvar()
    app.reg_frame.lb.selection_set(0)
    app.acao_buscar()
    assert app.info_basicas.combo_unidade_informante.get() == 'SES-GO/GGC'
    navegador = Mock(return_value=True)
    monkeypatch.setattr('sidgeo.view.aplicativo_tela.webbrowser.open_new_tab', navegador)
    app.acao_ver_reg()
    navegador.assert_called_once_with('https://bdg.ibge.gov.br/bdg/pdf/relatorio.asp?L1=422V')


def test_ajuda_descritivo_acrescenta_sem_apagar(app):
    app.observacoes.txt_descricao.insert('1.0', 'Observação existente.')
    app.observacoes.btn_ajuda_descritivo.invoke()
    janela = next(w for w in app.observacoes.winfo_children() if isinstance(w, AjudaDescritivo))
    janela.modelo.current(2)
    janela.atualizar()
    janela.inserir()
    texto = app.observacoes.txt_descricao.get('1.0', 'end')
    assert texto.startswith('Observação existente.\nTronco de pirâmide')
    assert '# cm' in texto


def test_bdg_preserva_ocupacao_e_aplica_opcao(app, monkeypatch):
    app.info_basicas.entry_estacao.insert(0, '422V')
    app.coordenadas.var_ocup_gps.set(True)
    reg = RegistroFabrica.criar(dict(cod_estacao='422V', lat_sinal='S', lat_grau=7,
                                   lon_sinal='W', lon_grau=39, data_coordenada='04/12/2009'))
    monkeypatch.setattr(app, 'janela_importar_coordenadas_bdg', lambda cod: (True, reg))
    app.acao_comparar_coord_bdg()
    assert app.coordenadas.var_atualizar_coord.get()
    assert app.coordenadas.var_ocup_gps.get()
    assert app.info_basicas.data_coordenada.year == 2009
    monkeypatch.setattr(app, 'janela_importar_coordenadas_bdg', lambda cod: (False, reg))
    app.acao_comparar_coord_bdg()
    assert not app.coordenadas.var_atualizar_coord.get()


def test_foto_editor_e_empacotamento_real(app, controller, tmp_path, monkeypatch):
    origem = tmp_path / 'foto.png'
    Image.new('RGB', (1600, 1200), (10, 80, 100)).save(origem)
    app.info_basicas.entry_estacao.insert(0, '422V')
    monkeypatch.setattr('sidgeo.view.fotos_frame.filedialog.askopenfilename', lambda **kw: str(origem))
    app.fotos_frame.adicionar('panoramica')
    app.fotos_frame.lista.selection_set('0')
    app.fotos_frame.editar()
    janela = next(w for w in app.fotos_frame.winfo_children() if isinstance(w, EditarFoto))
    janela.campos['horizontal'].set('100')
    janela.campos['vertical'].set('100')
    janela.atualizar()
    assert '640 × 480' in janela.tamanho.cget('text')
    janela.aplicar()
    assert app.fotos_frame.fotos[0].arquivo_original
    app.acao_salvar()
    assert len(controller.buscar_registro('422V').fotos) == 1
    destino = tmp_path / 'projeto_completo.zip'
    monkeypatch.setattr('tkinter.filedialog.asksaveasfilename', lambda **kw: str(destino))
    app.empacotar_zip()
    assert destino.is_file()
    app.reg_frame.lb.selection_set(0)
    app.acao_buscar()
    assert app.fotos_frame.fotos[0].arquivo_original
    assert origem.read_bytes() == controller.original_foto(app.fotos_frame.fotos[0])
