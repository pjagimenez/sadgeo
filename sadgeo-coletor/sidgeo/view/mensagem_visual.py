# -*- coding: utf-8 -*-
"""
file: /sidgeo/ui/mensagem_visual.py
@created: 25-02-2025 pjag
@updated: 03-07-2026 pjag Refatoração MVC, GRASP, PEP8 pythonic
"""
from typing import Protocol

from sidgeo.infra.notificacao_evento_log import NotificadorEventoLog


class JanelaMensagens(Protocol):
    def show_confirm_modal(self, pergunta: str, cor: str = "black") -> bool: ...
    def show_modal(self, mensagem: str, cor: str = "black") -> None: ...


class MensagemVisual:
    """Centraliza logs e UI feedback (modais)."""

    def __init__(self, logger: NotificadorEventoLog) -> None:
        self._logger = logger
        self._app: JanelaMensagens | None = None

    def attach(self, app: JanelaMensagens) -> None:
        """Associa a raiz Tk para modais."""
        self._app = app

    # Conveniências
    def info(self, msg: str, modal: bool = False) -> None:
        self._logger.info(msg)
        if modal:
            self._show_modal(msg, "black")

    def warn(self, msg: str, modal: bool = False) -> None:
        self._logger.warn(msg)
        if modal:
            self._show_modal(msg, "orange")

    def error(self, msg: str, modal: bool = True) -> None:
        self._logger.error(msg)
        if modal:
            self._show_modal(msg, "red")

    def confirm(self, pergunta: str, cor: str = "black") -> bool:
        """Mostra um modal de confirmação."""
        if self._app and hasattr(self._app, "show_confirm_modal"):
            return self._app.show_confirm_modal(pergunta, cor=cor)
        # fallback sem UI (útil para testes headless)
        self._logger.info(f"[CONFIRM_MODAL] {pergunta}")
        return False

    # Internos
    def _show_modal(self, mensagem: str, cor: str) -> None:
        if self._app and hasattr(self._app, "show_modal"):
            self._app.show_modal(mensagem, cor)
        else:
            # fallback: sem UI (teste/headless)
            self._logger.info(f"[MODAL {cor}] {mensagem}")
