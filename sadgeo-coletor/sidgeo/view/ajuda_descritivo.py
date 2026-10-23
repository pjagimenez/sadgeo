"""Consulta e inserção dos modelos de descritivo sem apagar o texto já digitado."""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk, scrolledtext

from sidgeo.domain.descritivos import MODELOS_DESCRITIVO
from sidgeo.view.tema import ajustar_janela


class AjudaDescritivo(tk.Toplevel):
    def __init__(self, master: tk.Misc, destino: tk.Text) -> None:
        super().__init__(master)
        self.destino = destino
        self.title("Ajuda — modelos de descritivo")
        ajustar_janela(self, 850, 390)
        self.transient(master.winfo_toplevel())
        self.grab_set()
        botoes = ttk.Frame(self, padding=10)
        botoes.pack(side="bottom", fill="x")
        ttk.Button(botoes, text="Copiar modelo", command=self.copiar).pack(side="left")
        ttk.Button(botoes, text="Inserir no descritivo", command=self.inserir,
                   style="Primario.TButton").pack(side="left", padx=8)
        ttk.Button(botoes, text="Fechar", command=self.destroy).pack(side="right")
        corpo = ttk.Frame(self, padding=12)
        corpo.pack(fill="both", expand=True)
        ttk.Label(corpo, text="Escolha o tipo de monumentação:").pack(anchor="w")
        self.modelo = ttk.Combobox(corpo, values=[nome for nome, _ in MODELOS_DESCRITIVO], state="readonly")
        self.modelo.pack(fill="x", pady=(6, 10))
        self.modelo.current(0)
        self.modelo.bind("<<ComboboxSelected>>", self.atualizar)
        self.texto = scrolledtext.ScrolledText(corpo, wrap="word", height=6)
        self.texto.pack(fill="both", expand=True)
        ttk.Label(corpo, text="Preencha cada # com a informação de campo. A inserção acrescenta o modelo ao texto atual.",
                  wraplength=780).pack(anchor="w", pady=(8, 0))
        self.atualizar()

    def atualizar(self, _evento: tk.Event | None = None) -> None:
        self.texto.configure(state="normal")
        self.texto.delete("1.0", "end")
        self.texto.insert("1.0", MODELOS_DESCRITIVO[self.modelo.current()][1])
        self.texto.configure(state="disabled")

    def copiar(self) -> None:
        self.clipboard_clear()
        self.clipboard_append(MODELOS_DESCRITIVO[self.modelo.current()][1])

    def inserir(self) -> None:
        if self.destino.get("1.0", "end-1c").strip():
            self.destino.insert("end-1c", "\n")
        self.destino.insert("end-1c", MODELOS_DESCRITIVO[self.modelo.current()][1])
        self.destino.see("end")
        self.destroy()
