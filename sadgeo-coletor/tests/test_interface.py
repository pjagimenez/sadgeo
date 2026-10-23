import tkinter as tk
from tkinter import ttk
from unittest.mock import Mock

import pytest

from sidgeo.domain.registro_fabrica import RegistroFabrica
from sidgeo.view.bdg_formulario_busca import JanelaCoordenadasBDG
from sidgeo.view.sadgeo_formulario_busca import JanelaBuscaSadgeo
from sidgeo.view.mensagem_visual import MensagemVisual

pytestmark = pytest.mark.gui


def descendentes(widget):
    for filho in widget.winfo_children():
        yield filho
        yield from descendentes(filho)


def test_layout_cabe_em_1366x768(app):
    assert app.winfo_width() <= 1326
    assert app.winfo_height() <= 668
    assert len(app.abas.tabs()) == 4
    for aba_id in app.abas.tabs():
        app.abas.select(aba_id)
        app.update()
        aba = app.nametowidget(aba_id)
        assert aba.canvas.xview() == (0.0, 1.0)
        assert aba.canvas.yview() == (0.0, 1.0)
        for widget in descendentes(app):
            if widget.winfo_ismapped() and isinstance(widget, (tk.Entry, ttk.Entry, ttk.Button)):
                x = widget.winfo_rootx() - app.winfo_rootx()
                y = widget.winfo_rooty() - app.winfo_rooty()
                assert x >= 0 and x + widget.winfo_width() <= app.winfo_width()
                assert y >= 0 and y + widget.winfo_height() <= app.winfo_height()


def test_redimensionar_mantem_acoes_e_rolagem(app):
    app.geometry('1000x560')
    app.update()
    for aba_id in app.abas.tabs():
        app.abas.select(aba_id)
        app.update()
        aba = app.nametowidget(aba_id)
        aba.canvas.xview_moveto(1)
        aba.canvas.yview_moveto(1)
        assert aba.canvas.winfo_width() > 100
        assert app.ds_frame.winfo_y() + app.ds_frame.winfo_height() <= app.winfo_height()
        for widget in app.reg_frame.winfo_children():
            if isinstance(widget, ttk.Button):
                assert widget.winfo_ismapped()


def test_salvar_editar_ver_dados_e_excluir(app, controller):
    app.info_basicas.entry_estacao.insert(0, '1234A')
    app.observacoes.txt_descricao.insert('1.0', 'Teste da interface')
    app.acao_salvar()
    app.show_modal.assert_not_called()
    assert app.reg_frame.lb.size() == 1
    app.reg_frame.lb.selection_set(0)
    app.acao_buscar()
    assert app.info_basicas.entry_estacao.get() == '1234A'
    assert app.observacoes.txt_descricao.get('1.0', 'end').strip() == 'Teste da interface'
    app.exibir_dados()
    tabela = next(w for w in descendentes(app) if isinstance(w, ttk.Treeview) and w is not app.fotos_frame.lista)
    assert len(tabela.get_children()) == 1
    app.show_confirm_modal = Mock(return_value=False)
    app.acao_excluir()
    assert controller.buscar_registro('1234A') is not None
    app.show_confirm_modal.return_value = True
    app.acao_excluir()
    assert controller.listar_registros() == []
    assert app.reg_frame.lb.size() == 0


def test_confirmacao_real_pode_cancelar(app):
    def responder():
        botao = next(w for w in descendentes(app) if isinstance(w, tk.Button) and w.cget('text') == 'Não')
        botao.invoke()
    app.after(30, responder)
    assert app.msg.confirm('Confirmação de teste') is False


def test_sem_janela_nao_confirma_exclusao(logger):
    assert MensagemVisual(logger).confirm('Apagar tudo?') is False


@pytest.mark.parametrize('acao,atualiza', [('usar_bdg', True), ('manter_local', False), ('fechar', None)])
def test_comparacao_bdg_retorna_escolha(app, acao, atualiza):
    local = RegistroFabrica.criar({'cod_estacao': '1234A', 'lat_sinal': '-', 'lat_grau': 22, 'lon_sinal': '-', 'lon_grau': 43})
    bdg = RegistroFabrica.criar({'cod_estacao': '1234A', 'lat_sinal': '-', 'lat_grau': 23, 'lon_sinal': '-', 'lon_grau': 43})
    dialogo = JanelaCoordenadasBDG(app, app.msg, app.mapper_view, local, bdg)
    dialogo.update()
    for frame in (dialogo.frm_coord_local, dialogo.frm_coord_bdg):
        assert frame.txt_lat_grau.cget('state') == 'disabled'
        assert frame.winfo_rootx() + frame.winfo_reqwidth() <= dialogo.winfo_rootx() + dialogo.winfo_width()
    dialogo.after(10, getattr(dialogo, acao))
    resultado = dialogo.obter_resultado()
    if atualiza is None:
        assert resultado is None
    else:
        assert resultado == (atualiza, bdg if atualiza else local)


def test_coordenadas_bdg_aplicadas_sem_salvar_automaticamente(app, controller, monkeypatch):
    app.info_basicas.entry_estacao.insert(0, '1234A')
    bdg = RegistroFabrica.criar({'cod_estacao': '1234A', 'lat_sinal': '-', 'lat_grau': 23, 'lon_sinal': '-', 'lon_grau': 43})
    monkeypatch.setattr(app, 'janela_importar_coordenadas_bdg', lambda cod: (True, bdg))
    app.acao_comparar_coord_bdg()
    assert app.coordenadas.txt_lat_grau.get() == '23'
    assert controller.buscar_registro('1234A') is None


def test_zerar_base_e_cancelar_saida(app, controller):
    controller.salvar_registro(RegistroFabrica.criar({'cod_estacao': '1234A'}))
    app.atualiza_listbox()
    app.show_confirm_modal = Mock(return_value=False)
    app.zerar_base()
    assert len(controller.listar_registros()) == 1
    app.on_close()
    assert app.winfo_exists()
    app.show_confirm_modal.return_value = True
    app.zerar_base()
    assert controller.listar_registros() == []
    assert app.reg_frame.lb.size() == 0


def test_consulta_sadgeo_seleciona_linha_com_seq_vazio(app):
    dialogo = JanelaBuscaSadgeo(app, app.msg, app.controle_app)
    registros = [RegistroFabrica.criar({'cod_estacao': '1234A', 'campanha': campanha}) for campanha in ('medA', 'medP')]
    dialogo.registros = registros
    dialogo._popular_tabela_visual(registros)
    dialogo.tree.selection_set(dialogo.tree.get_children()[1])
    dialogo.on_select()
    assert dialogo.registro_selecionado is registros[1]
    dialogo.destroy()


@pytest.mark.parametrize('acao', ['importacao', 'exportacao'])
@pytest.mark.parametrize('cancelar', [False, True])
def test_dialogo_arquivo_retorna_caminho_ou_cancelamento(app, monkeypatch, acao, cancelar):
    from sidgeo.view import dialogo_visual
    monkeypatch.setattr(dialogo_visual.filedialog, 'askopenfilename', lambda **kwargs: 'exemplo.csv')
    monkeypatch.setattr(dialogo_visual.filedialog, 'asksaveasfilename', lambda **kwargs: 'exemplo.csv')
    def responder():
        rotulo = 'Cancelar' if cancelar else 'Escolher arquivo' if acao == 'importacao' else 'Salvar'
        botao = next(w for w in descendentes(app) if isinstance(w, tk.Button) and w.cget('text') == rotulo)
        botao.invoke()
    app.after(30, responder)
    resultado = getattr(app.dialogo, f'escolher_arquivo_{acao}')()
    assert resultado == (None if cancelar else ('exemplo.csv', 'csv'))


def test_saida_finaliza_persistencia(app, controller, monkeypatch):
    app.show_confirm_modal = Mock(return_value=True)
    persistir = Mock(wraps=controller.finalizar_persistencia)
    monkeypatch.setattr(controller, 'finalizar_persistencia', persistir)
    # Observa o fechamento e deixa a fixture destruir a raiz Tk ao terminar.
    with monkeypatch.context() as patch:
        fechar = Mock()
        patch.setattr(app, 'destroy', fechar)
        app.on_close()
        fechar.assert_called_once()
    persistir.assert_called_once()


def test_fontes_maiores_mantem_campos_acessiveis(app):
    from tkinter import font
    for nome in ('TkDefaultFont', 'TkTextFont', 'TkMenuFont'):
        font.nametofont(nome).configure(size=12)
    for aba_id in app.abas.tabs():
        app.abas.select(aba_id)
        app.update()
        aba = app.nametowidget(aba_id)
        if aba.conteudo.winfo_reqwidth() > aba.canvas.winfo_width():
            assert aba.horizontal.winfo_ismapped()
        if aba.conteudo.winfo_reqheight() > aba.canvas.winfo_height():
            assert aba.vertical.winfo_ismapped()
        aba.canvas.xview_moveto(1)
        aba.canvas.yview_moveto(1)
        assert aba.canvas.xview()[1] == 1.0
        assert aba.canvas.yview()[1] == 1.0
    assert app.ds_frame.winfo_y() + app.ds_frame.winfo_height() <= app.winfo_height()
