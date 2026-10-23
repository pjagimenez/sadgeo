# -*- coding: utf-8 -*-
"""
file: /sidgeo/ui/dataset_frame.py
Created on Wed Feb 26 10:35:12 2025
@author: pjag
"""
from __future__ import annotations

from collections.abc import Callable

import tkinter as tk
from tkinter import ttk
from typing import Any
from sidgeo.view.mensagem_visual import MensagemVisual


# ──────────────────────────────
# 2. Controles de DATASET
# ──────────────────────────────
class DatasetFrame(tk.Frame):
    """Botões que agem sobre o DataFrame inteiro."""

    def __init__(self,
        master: tk.Misc,
        msg: MensagemVisual,
        importar: Callable[[], None] | None = None,
        exportar: Callable[[], None] | None = None,
        zerar: Callable[[], None] | None = None,
        ver: Callable[[], None] | None = None,
        consultar_sadgeo: Callable[[], None] | None = None,
        empacotar: Callable[[], None] | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(master, **kwargs)

        self._callbacks  = {"importar": importar,
                            "exportar": exportar,
                            "zerar": zerar,
                            "ver": ver,
                            "consultar_sadgeo" : consultar_sadgeo,
                            "empacotar": empacotar,
        }
        self._build()


    def _callback(self, nome: str) -> Callable[[], None]:
        callback = self._callbacks.get(nome)
        return callback if callback is not None else lambda: None


    def _build(self) -> None:
        # ── 6 colunas: [esp½] [btn] [btn] [btn] [btn] [esp½] ──
        for col in range(8):
            # colunas 0 e 5 recebem peso 1 → centralizam o bloco
            self.columnconfigure(col, weight=1 if col in (0, 7) else 0)

        # Botão Importar
        ttk.Button(self,
                  text="Importar arquivo",
                  command=self._callback("importar")
        ).grid(row=0, column=1, padx=(5, 5), pady=2 )

        # Botão Exportar
        ttk.Button(self,
                  text="Exportar arquivo",
                  command=self._callback("exportar")
        ).grid(row=0, column=2, padx=(5, 5), pady=2 )

        # Botão Zerar
        ttk.Button(self,
                  text="Zerar base local",
                  style="Perigo.TButton",
                  command=self._callback("zerar")
        ).grid(row=0, column=3, padx=(5,5), pady=2 )

        # Botão Ver
        ttk.Button(self,
                  text="Ver dados locais",
                  command=self._callback("ver")
        ).grid(row=0, column=4, padx=(5, 5), pady=2 )

        # Botão Consulta SADGEO
        ttk.Button(self,
                  text="Consultar SADGEO",
                  style="Primario.TButton",
                  command=self._callback("consultar_sadgeo")
        ).grid(row=0, column=5, padx=(5, 5), pady=2 )

        ttk.Button(self, text="Empacotar ZIP", command=self._callback("empacotar"),
                   style="Primario.TButton").grid(row=0, column=6, padx=5, pady=2)
