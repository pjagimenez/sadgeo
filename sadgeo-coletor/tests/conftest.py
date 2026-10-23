from unittest.mock import Mock
import tkinter as tk

import pytest

from sidgeo.application.controller_fabrica import ControllerFactory
from sidgeo.infra.notificacao_evento_log import NotificadorEventoLog
from sidgeo.view.aplicativo_tela import AplicativoVisual


def pytest_addoption(parser):
    parser.addoption('--require-gui', action='store_true', help='Falha se a interface não puder ser testada')


@pytest.fixture
def logger():
    return Mock(spec=NotificadorEventoLog)


@pytest.fixture
def controller(tmp_path, logger):
    return ControllerFactory.criar(logger, data_dir=tmp_path)


@pytest.fixture
def app(controller, logger, monkeypatch, request):
    # Reproduz a resolução do notebook mesmo quando executado em outro monitor.
    monkeypatch.setattr(tk.Misc, 'winfo_screenwidth', lambda self: 1366)
    monkeypatch.setattr(tk.Misc, 'winfo_screenheight', lambda self: 768)
    try:
        janela = AplicativoVisual(controller, logger)
    except tk.TclError as erro:
        sem_display = any(texto in str(erro) for texto in ('no display name', "couldn't connect to display"))
        if request.config.getoption('--require-gui') or not sem_display:
            pytest.fail(f'Sessão gráfica obrigatória indisponível: {erro}')
        pytest.skip(f'Sem sessão gráfica: {erro}')
    janela.show_modal = Mock()
    janela.update()
    yield janela
    logger.registrar_excecao.assert_not_called()
    if janela.winfo_exists():
        for callback in janela.tk.splitlist(janela.tk.call('after', 'info')):
            # Cada widget continua responsável por remover seus próprios comandos Tcl.
            janela.tk.call('after', 'cancel', callback)
        janela.destroy()
