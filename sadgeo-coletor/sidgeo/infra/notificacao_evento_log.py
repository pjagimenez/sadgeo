# -*- coding: utf-8 -*-
"""
file: /sidgeo/application/notificacao.py
@created: 03-07-2026 pjag
@updated: 03-07-2026 pjag Refatoração MVC, GRASP, PEP8 pythonic
"""

from __future__ import annotations

import sys
from pathlib import Path

import logging
from logging.handlers import RotatingFileHandler

import platformdirs

from sidgeo.util.settings import APP_SIGLA


class NotificadorEventoLog:
    """Notificador simples para logs da aplicação."""
       
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
        return cls._instancia

    def __init__(self) -> None:

        if hasattr(self, "_inicializado"):
            return

        self._inicializado = True

        log_path = Path(
            platformdirs.user_log_dir(
                APP_SIGLA,
                appauthor=False,
            )
        )

        log_path.mkdir(
            parents=True,
            exist_ok=True,
        )

        handler = RotatingFileHandler(
            log_path / "sidgeo.log",
            maxBytes=500_000,
            backupCount=3,
            encoding="utf-8",
        )

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(message)s"
        )

        self.logger = logging.getLogger(APP_SIGLA)

        self.logger.setLevel(logging.INFO)
        self.logger.handlers.clear()

        handler.setFormatter(formatter)

        self.logger.addHandler(handler)
        self.logger.propagate = False



    def instalar_excepthook(self):
    
        def _excepthook(exc_type, exc, tb):
            self.logger.exception(
                "Uncaught exception",
                exc_info=(exc_type, exc, tb),
            )
    
            sys.__excepthook__(
                exc_type,
                exc,
                tb,
            )
    
        sys.excepthook = _excepthook 

    def info(self, mensagem: str) -> None:
        self.logger.info(mensagem)

    def warn(self, mensagem: str) -> None:
        self.logger.warning(mensagem)

    def error(self, mensagem: str) -> None:
        self.logger.error(mensagem)   
        
    def exception(self, mensagem: str) -> None:
        self.logger.exception(mensagem)
