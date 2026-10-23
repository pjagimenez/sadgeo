# -*- coding: utf-8 -*-
"""
file: /sidgeo/ui/sadgeo_formulario_busca.py
@created: 09-09-2025 pjag
@updated: 03-07-2026 pjag Refatoração MVC, GRASP, PEP8 pythonic
"""
from __future__ import annotations

import tkinter as tk
from datetime import datetime, date
from tkinter import ttk
from typing import Literal

from sidgeo.domain.registro import Registro
from sidgeo.view.mensagem_visual import MensagemVisual
from sidgeo.application.aplicacao_controller import AplicacaoController


Anchor = Literal[
    "nw", "n", "ne",
    "w", "center", "e",
    "sw", "s", "se"
]


class JanelaBuscaSadgeo(tk.Toplevel):
    """Janela visual para buscar e selecionar registros SADGEO."""

    def __init__(
        self,
        master: tk.Tk | tk.Toplevel,
        mensagens: MensagemVisual,
        controller: AplicacaoController,
    ) -> None:
        super().__init__(master)

        self.mensagens = mensagens
        self.controller = controller

        self.registros: list[Registro] = []
        self.registro_selecionado: Registro | None = None
        self.resultado: Registro | None = None

        self.title("Importar via SADGEO")
        self.geometry("700x450")
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()

        self._construir_interface()


    def _construir_interface(self) -> None:
        frame_top = tk.Frame(self)
        frame_top.pack(pady=2, padx=10, fill="x")

        tk.Label(frame_top, text="Código da Estação:").pack(
            side="left",
            padx=2,
        )

        self.entry_codigo = tk.Entry(frame_top)
        self.entry_codigo.pack(side="left", padx=2)
        self.entry_codigo.bind("<Return>", lambda _e: self.buscar_estacao())

        tk.Button(
            frame_top,
            text="Buscar",
            command=self.buscar_estacao,
        ).pack(side="left", padx=5)

        colunas = (
            "seq",
            "campanha",
            "data_levantamento",
            "projeto",
            "municipio",
            "uf",
        )

        self.tree = ttk.Treeview(
            self,
            columns=colunas,
            show="headings",
            height=14,
        )

        self._configurar_colunas()
        self.tree.pack(expand=True, fill="both", padx=10, pady=(0, 2))
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        frame_bottom = tk.Frame(self)
        frame_bottom.pack(fill="x", padx=10, pady=2)

        self.label_detalhes = tk.Label(
            frame_bottom,
            text="Selecione um registro para ver detalhes.",
            anchor="w",
            justify="left",
        )
        self.label_detalhes.pack(fill="x")

        self.btn_selecionar = tk.Button(
            frame_bottom,
            text="Selecionar Registro",
            command=self.selecionar_registro,
            state="disabled",
        )
        self.btn_selecionar.pack(pady=2)

    def _configurar_colunas(self) -> None:
        configuracoes: dict[    str,     tuple[str, int, Anchor] ] =    {
            "seq": ("Seq", 50, "center"),
            "campanha": ("Campanha", 90, "center"),
            "data_levantamento": ("Data Lev.", 110, "center"),
            "projeto": ("Projeto", 100, "w"),
            "municipio": ("Município", 160, "w"),
            "uf": ("UF", 50, "center"),
        }

        for coluna, (titulo, largura, alinhamento) in configuracoes.items():
            self.tree.heading(coluna, text=titulo)
            self.tree.column(
                coluna,
                width=largura,
                anchor=alinhamento,
                stretch=True,
            )

    def buscar_estacao(self) -> None:
        codigo = self.entry_codigo.get().strip()

        if not codigo:
            self.mensagens.warn(
                "Digite o código da estação.",
                modal=True,
            )
            return

        self.label_detalhes.config(text="Buscando registros…")
        self._popular_tabela_visual([])
        self._set_busy(True)

        try:
            resultado = self.controller.buscar_sadgeo(codigo)
            self.registros = resultado or []
            self._popular_tabela_visual(self.registros)

            if not self.registros:
                self.mensagens.warn(
                    "Nenhum registro encontrado para esta estação.",
                    modal=True,
                )
                self.label_detalhes.config(
                    text="Nenhum registro encontrado."
                )

        except Exception as erro:
            self.registros = []
            self._popular_tabela_visual([])
            self.label_detalhes.config(text="Falha na consulta.")
            self.mensagens.error(
                f"Falha ao consultar SADGEO: {erro}",
                modal=True,
            )

        finally:
            self._set_busy(False)

    def _set_busy(self, busy: bool) -> None:
        self.configure(cursor="watch" if busy else "")
        self.btn_selecionar.config(state="disabled")
        self.update_idletasks()

    def _popular_tabela_visual(self, registros: list[Registro]) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)

        self.registro_selecionado = None
        self.btn_selecionar.config(state="disabled")
        self.label_detalhes.config(
            text="Selecione um registro para ver detalhes."
        )

        for registro in registros:
            self.tree.insert(
                "",
                "end",
                values=(
                    registro.seq,
                    registro.campanha,
                    self._formatar_data(registro.data_levantamento),
                    registro.projeto,
                    registro.municipio,
                    registro.uf,
                ),
            )

    def on_select(self, _event: tk.Event | None = None) -> None:
        selection = self.tree.selection()

        if not selection:
            return

        values = self.tree.item(selection[0]).get("values", [])

        if not values:
            return

        seq_selecionado = str(values[0])

        self.registro_selecionado = next(
            (
                registro
                for registro in self.registros
                if str(registro.seq) == seq_selecionado
            ),
            None,
        )

        if not self.registro_selecionado:
            self.btn_selecionar.config(state="disabled")
            return

        registro = self.registro_selecionado

        detalhes = (
            f"Seq: {registro.seq or '-'} | "
            f"Campanha: {registro.campanha or '-'} | "
            f"Data: {self._formatar_data(registro.data_levantamento) or '-'} | "
            f"Projeto: {registro.projeto or '-'} | "
            f"Município: {registro.municipio or '-'} | "
            f"UF: {registro.uf or '-'}"
        )

        self.label_detalhes.config(text=detalhes)
        self.btn_selecionar.config(state="normal")

    def selecionar_registro(self) -> None:
        if not self.registro_selecionado:
            self.mensagens.warn(
                "Nenhum registro selecionado.",
                modal=True,
            )
            return

        self.resultado = self.registro_selecionado
        self.destroy()

    def obter_resultado(self) -> Registro | None:
        self.wait_window()
        return self.resultado

    @staticmethod
    def _formatar_data(valor: object) -> str:
        if valor is None:
            return ""

        if isinstance(valor, (date, datetime)):
            return valor.strftime("%d/%m/%Y")
       
        texto = str(valor).strip()
        return texto if texto not in ("None", "NaT", "nan") else ""