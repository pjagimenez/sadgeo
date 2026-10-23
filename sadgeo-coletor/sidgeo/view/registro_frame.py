"""Ações do registro e listagem que permanecem acessíveis junto ao formulário."""
from __future__ import annotations

from collections.abc import Callable
import tkinter as tk
from tkinter import ttk
from typing import Any
from sidgeo.view.mensagem_visual import MensagemVisual


class RegistroFrame(ttk.LabelFrame):
    def __init__(self, master: tk.Misc, msg: MensagemVisual,
                 salvar: Callable[[], None] | None = None,
                 excluir: Callable[[], None] | None = None,
                 limpar: Callable[[], None] | None = None,
                 buscar: Callable[[], None] | None = None,
                 comparar: Callable[[], None] | None = None,
                 ver_reg: Callable[[], None] | None = None,
                 **kwargs: Any) -> None:
        super().__init__(master, text="Registros locais", padding=8, **kwargs)
        self.columnconfigure((0, 1), weight=1)
        self.rowconfigure(4, weight=1)
        for texto, comando, linha, coluna, estilo in (
            ("Salvar registro", salvar, 0, 0, "Primario.TButton"),
            ("Limpar formulário", limpar, 0, 1, "TButton"),
            ("Coordenadas BDG", comparar, 1, 0, "TButton"),
            ("Excluir registro", excluir, 1, 1, "Perigo.TButton"),
        ):
            ttk.Button(self, text=texto, command=comando or (lambda: None), style=estilo).grid(
                row=linha, column=coluna, padx=2, pady=3, sticky="ew")
        ttk.Button(self, text="Ver REG", command=ver_reg or (lambda: None)).grid(
            row=2, column=0, columnspan=2, sticky="ew", padx=2, pady=3)
        ttk.Label(self, text="Estação · Campanha · Levantamento · Seq",
                  font=("TkDefaultFont", 8)).grid(row=3, column=0, columnspan=2, pady=(12, 4))
        lista = ttk.Frame(self)
        lista.grid(row=4, column=0, columnspan=2, sticky="nsew")
        lista.rowconfigure(0, weight=1)
        lista.columnconfigure(0, weight=1)
        self.lb = tk.Listbox(lista, height=10, width=40, exportselection=False,
                             font=("TkFixedFont", 9), relief="flat", borderwidth=0)
        self.lb.grid(row=0, column=0, sticky="nsew")
        vertical = ttk.Scrollbar(lista, orient="vertical", command=self.lb.yview)  # pyright: ignore[reportUnknownMemberType, reportUnknownArgumentType]
        horizontal = ttk.Scrollbar(lista, orient="horizontal", command=self.lb.xview)  # pyright: ignore[reportUnknownMemberType, reportUnknownArgumentType]
        vertical.grid(row=0, column=1, sticky="ns")
        horizontal.grid(row=1, column=0, sticky="ew")
        self.lb.configure(yscrollcommand=vertical.set, xscrollcommand=horizontal.set)
        ttk.Button(self, text="Editar registro selecionado", command=buscar or (lambda: None)).grid(
            row=5, column=0, columnspan=2, sticky="ew", pady=(8, 0))
        if buscar is not None:
            self.lb.bind("<Double-Button-1>", lambda _e: buscar())
