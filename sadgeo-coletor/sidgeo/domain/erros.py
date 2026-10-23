# -*- coding: utf-8 -*-
"""
file: /sidgeo/domain/erros.py
@created: 09-09-2025 pjag
@updated: 03-07-2026 pjag Refatoração MVC, GRASP, PEP8 pythonic
"""
from __future__ import annotations

from typing import Iterable


class ValidacaoErro(Exception):
    """
    Erro de validação agregando uma.erros = [str(e) for e in erros]    
    Erro de validação agregando uma ou mais mensagens.
        super().__init__("\n".join(self.erros))
    """

    def __init__(self, erros: str | Iterable[str]) -> None:
        if isinstance(erros, str):
            self.erros = [erros]
        else:
            self.erros = [str(erro) for erro in erros]

        super().__init__("\n".join(self.erros))
