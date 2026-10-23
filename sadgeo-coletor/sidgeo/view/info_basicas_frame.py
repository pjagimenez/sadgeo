# -*- coding: utf-8 -*-
"""
file: /sidgeo/ui/info_basicas_frame.py
Created on Wed Feb 26 10:35:12 2025
@author: pjag
"""
from __future__ import annotations

import re
import tkinter as tk
from typing import Any
from datetime import datetime
from tkinter import ttk
from tkcalendar import DateEntry
from sidgeo.domain.informante import UNIDADES_INFORMANTE
from sidgeo.domain.registro_validador import RegistroValidador
from sidgeo.domain.erros import ValidacaoErro

from sidgeo.domain.dominios import (TIPO_CONEXAO_LIST,
                                    TIPO_MONUMENTACAO_DICT,
                                    opcoes_tipo_local,
                                    opcoes_situacao,
                                    opcoes_campanha,
                                    opcoes_uf)

from sidgeo.domain.registro_metadados import STATUS_MAP
from sidgeo.view.mensagem_visual import MensagemVisual
from sidgeo.util.strings import trim_all, values_with_placeholder, labels_from_opcoes, list_from_dict_cod_desc


# ---------------------------
# Classes de Interface
# ---------------------------

# Classe para o quadro de Informações Básicas
class InfoBasicasFrame(tk.LabelFrame):


    def __init__(self,
                 master: tk.Misc,
                 msg: MensagemVisual,
                 **kwargs: Any
    ) -> None:
        super().__init__(master, text="Informações Básicas", padx=10, pady=2, **kwargs)
        self.msg = msg
        self.create_widgets()


    def validar_informante(self, event: tk.Event | None = None):
        valor = self.entry_informante.get().strip()

        try:
            RegistroValidador.validar_informante(valor)
        except ValidacaoErro as erro:
            # Preserva o texto digitado para permitir a correção.
            self.msg.warn(str(erro), modal=True)
            self.entry_informante.focus_set()


    def validar_siape(self,event: tk.Event | None = None):
        valor = self.entry_siape.get().strip()

        if valor and not re.fullmatch(r"\d{6,7}", valor):
            self.msg.warn(
                "SIAPE inválido. Informe um número com 6 ou 7 dígitos.",
                modal=True
            )

            self.entry_siape.delete(0, tk.END)
            self.entry_siape.focus_set()


    def validar_codigo_estacao(self, entry: tk.Entry, nome_campo: str, obrigatorio: bool = True):
        valor = entry.get().strip().upper()

        # Atualiza para maiúsculas
        entry.delete(0, tk.END)
        entry.insert(0, valor)

        # Campo opcional e vazio
        if not valor:
            if obrigatorio:
                self.msg.warn(
                    f"{nome_campo} deve ser informado.",
                    modal=True
                )
                entry.focus_set()
            return

        padrao_curto = r"^[1-9][A-Z0-9]{0,4}$"
        padrao_longo = r"^8\d{6}$"

        if not (
            re.fullmatch(padrao_curto, valor)
            or re.fullmatch(padrao_longo, valor)
        ):
            self.msg.warn(
                f"{nome_campo} inválido.\n"
                "Informe de 1 a 5 caracteres alfanuméricos "
                "(iniciando por 1 a 9) ou 7 dígitos numéricos "
                "iniciando por 8.",
                modal=True
            )

            entry.delete(0, tk.END)
            entry.focus_set()


    def create_widgets(self):
        # Primeira coluna 0-1

        # Estação   lin=0 / Col=0+1
        tk.Label(self, text="Estação:").grid(row=0, column=0, padx=5, pady=2, sticky="e")
        self.entry_estacao = tk.Entry(self, width=20)
        self.entry_estacao.grid(row=0, column=1, padx=5, pady=2, sticky="w")
        self.entry_estacao.bind("<FocusOut>", lambda _e: self.validar_codigo_estacao(self.entry_estacao, "Código Estação"))

        # Monumentação    lin=1 / Col=0+1
        tk.Label(self, text="Monumentação:").grid(row=1, column=0, padx=5, pady=2, sticky="e")
        self.combo_monumentacao = ttk.Combobox(
            self,
            values=values_with_placeholder(list_from_dict_cod_desc(TIPO_MONUMENTACAO_DICT)),
            state="readonly",
            width=30,
        )
        self.combo_monumentacao.grid(row=1, column=1, padx=5, pady=2, sticky="w")

        # Tipo Local   lin=2 / Col=0+1
        tk.Label(self, text="Tipo Local:").grid(row=2, column=0, padx=5, pady=2, sticky="e")
        self.combo_tipo_local = ttk.Combobox(
            self,
            values=values_with_placeholder(labels_from_opcoes(opcoes_tipo_local())),
            state="readonly",
            width=30,
        )
        self.combo_tipo_local.grid(row=2, column=1, padx=5, pady=2, sticky="w")

        # Inscrição na Chapa   lin=3 / Col=0+1
        tk.Label(self, text="Inscr.Chapa:").grid(row=3, column=0, padx=5, pady=2, sticky="e")
        self.entry_inscr_chapa = tk.Entry(self, width=20)
        self.entry_inscr_chapa.grid(row=3, column=1, padx=5, pady=2, sticky="w")

        # Situação (domínio)   lin=4 / Col=0+1
        tk.Label(self, text="Situação:").grid(row=4, column=0, padx=5, pady=2, sticky="e")
        self.combo_situacao = ttk.Combobox(
            self,
            values=values_with_placeholder(labels_from_opcoes(opcoes_situacao())),
            state="readonly",
            width=30,
        )
        self.combo_situacao.grid(row=4, column=1, padx=5, pady=2, sticky="w")

        # Conexão   lin=5 / Col=0+1
        tk.Label(self, text="Conexão:").grid(row=5, column=0, padx=5, pady=2, sticky="e")
        self.entry_conexao = tk.Entry(self, width=20)
        self.entry_conexao.grid(row=5, column=1, padx=5, pady=2, sticky="w")
        self.entry_conexao.bind("<FocusOut>", lambda _e: self.validar_codigo_estacao(
            self.entry_conexao, "Estação Conexão", obrigatorio=False))

        # Tipo de Conexão   lin=6 / Col=0+1
        tk.Label(self, text="Tipo Conexão:").grid(row=6, column=0, padx=5, pady=2, sticky="e")
        self.combo_tipo_conexao = ttk.Combobox(
            self,
            values=values_with_placeholder(TIPO_CONEXAO_LIST),
            state="readonly",
            width=20,
        )
        self.combo_tipo_conexao.grid(row=6, column=1, padx=5, pady=2, sticky="w")

        # RN Anterior   lin=7 / Col=0+1
        tk.Label(self, text="RN Anterior:").grid(row=7, column=0, padx=5, pady=2, sticky="e")
        self.entry_rn_anterior = tk.Entry(self, width=20)
        self.entry_rn_anterior.grid(row=7, column=1, padx=5, pady=2, sticky="w")

        # Informante    lin=8 / Col 0-1
        tk.Label(self, text="Informante (login):").grid(row=8, column=0, padx=5, pady=2, sticky="e")
        self.entry_informante = tk.Entry(self, width=20)
        self.entry_informante.grid(row=8, column=1, padx=5, pady=2, sticky="w")
        self.entry_informante.bind("<FocusOut>",self.validar_informante)

        # SIAPE    lin=9 / Col 0-1
        tk.Label(self, text="Informante (SIAPE):").grid(row=9, column=0, padx=5, pady=2, sticky="e")
        self.entry_siape = tk.Entry(self, width=20)
        self.entry_siape.grid(row=9, column=1, padx=5, pady=2, sticky="w")
        self.entry_siape.bind("<FocusOut>", self.validar_siape)

        # --------------------------------------
        # Segunda coluna 2-3

        # Campanha     lin=0 / Col 2-3
        tk.Label(self, text="Campanha:").grid(row=0, column=2, padx=5, pady=2, sticky="e")
        self.combo_campanha = ttk.Combobox(
            self,
            values=values_with_placeholder(labels_from_opcoes(opcoes_campanha())),
            state="readonly",
            width=20,
        )
        self.combo_campanha.grid(row=0, column=3, padx=5, pady=2, sticky="w")

        # Data de Levantamento     lin=1 / Col 2-3
        tk.Label(self, text="Dt.Levantamento:").grid(row=1, column=2, padx=10, pady=2, sticky="e")
        self.entry_data_levantamento = DateEntry(
            self, width=12, background="darkblue", foreground="white", borderwidth=2, date_pattern="dd/mm/yyyy"
        )
        self.entry_data_levantamento.grid(row=1, column=3, padx=10, pady=2, sticky="w")

        # Data de Crítica     lin=2 / Col 2-3
        tk.Label(self, text="Dt.Crítica:").grid(row=2, column=2, padx=10, pady=2, sticky="e")
        self.entry_data_critica = DateEntry(
            self, width=12, background="darkblue", foreground="white", borderwidth=2, date_pattern="dd/mm/yyyy"
        )
        self.entry_data_critica.grid(row=2, column=3, padx=10, pady=2, sticky="w")

        # Projeto    lin=3 / Col 2-3
        tk.Label(self, text="Projeto:").grid(row=3, column=2, padx=5, pady=2, sticky="e")
        self.entry_projeto = tk.Entry(self, width=20)
        self.entry_projeto.grid(row=3, column=3, padx=5, pady=2, sticky="w")

        # NUE  lin=4 / Col 2-3
        tk.Label(self, text="NUE:").grid(row=4, column=2, padx=5, pady=2, sticky="e")
        self.entry_nue = tk.Entry(self, width=20)
        self.entry_nue.grid(row=4, column=3, padx=5, pady=2, sticky="w")

        # Linha    lin=5 / Col 2-3
        tk.Label(self, text="Linha:").grid(row=5, column=2, padx=5, pady=2, sticky="e")
        self.entry_linha = tk.Entry(self, width=20)
        self.entry_linha.grid(row=5, column=3, padx=5, pady=2, sticky="w")

        # Caderneta    lin=6 / Col 2-3
        tk.Label(self, text="Caderneta:").grid(row=6, column=2, padx=5, pady=2, sticky="e")
        self.entry_caderneta = tk.Entry(self, width=20)
        self.entry_caderneta.grid(row=6, column=3, padx=5, pady=2, sticky="w")

        # Local Cidade    lin=7 / Col 2-3
        tk.Label(self, text="Município:").grid(row=7, column=2, padx=5, pady=2, sticky="e")
        self.entry_municipio = tk.Entry(self, width=20)
        self.entry_municipio.grid(row=7, column=3, padx=5, pady=2, sticky="w")

        # Local UF    lin=7 / Col 2-3
        tk.Label(self, text="UF:").grid(row=8, column=2, padx=5, pady=2, sticky="e")
        self.combo_uf = ttk.Combobox(
             self,
             values=values_with_placeholder(labels_from_opcoes(opcoes_uf())),
             state="readonly",
             width=20,
        )
        self.combo_uf.grid(row=8, column=3, padx=5, pady=2, sticky="w")

        tk.Label(self, text="Unidade informante:").grid(row=9, column=2, padx=5, pady=2, sticky="e")
        self.combo_unidade_informante = ttk.Combobox(
            self, values=values_with_placeholder(UNIDADES_INFORMANTE), state="readonly", width=20,
        )
        self.combo_unidade_informante.grid(row=9, column=3, padx=5, pady=2, sticky="w")
        self.data_coordenada: datetime | None = None

        # --------------------------------------
        # Campos ocultos (seq/status)  -- Parte inferior desse quadro col 0-1, 2-3
        self.seq_var = tk.StringVar(self)
        self.status_vrf_var = tk.StringVar(self)  # valor codificado: '', '1', '2', '3', '4'

        # Label de Seq
        tk.Label(self, text="Seq/Id:").grid(row=10, column=0, padx=5, pady=2, sticky="e")
        self.lbl_seqid = tk.Label(self, textvariable=self.seq_var, anchor="w")
        self.lbl_seqid.grid(row=10, column=1, padx=5, pady=2, sticky="w")

        # Label de Status VRF (somente exibição)
        tk.Label(self, text="Situação:").grid(row=10, column=2, padx=5, pady=2, sticky="e")
        self.status_vrf_text = tk.StringVar(self, value=STATUS_MAP[""])
        self.lbl_status_vrf = tk.Label(self, textvariable=self.status_vrf_text, anchor="w")
        self.lbl_status_vrf.grid(row=10, column=3, padx=5, pady=2, sticky="w")

        # Atualiza label quando status_vrf_var mudar
        self.status_vrf_var.trace_add("write", self._update_status_vrf)

        self.set_default_value()

    def _update_status_vrf(self, *_args: str) -> None:
        val = self.status_vrf_var.get()
        self.status_vrf_text.set(STATUS_MAP.get(val, "Início"))

    def obter_key_combo(self, combo: ttk.Combobox) -> str:
        conteudo = combo.get()
        if conteudo == "Selecione..." or not conteudo.strip():
            return ""
        return conteudo.split(" - ")[0]  # retorna "COD"

    def get_data(self) -> dict[str, Any]:
        data: dict[str, Any] = {
            "cod_estacao": self.entry_estacao.get(),
            "monumentacao": self.obter_key_combo(self.combo_monumentacao),
            "tipo_local": self.obter_key_combo(self.combo_tipo_local),
            "inscr_chapa": self.entry_inscr_chapa.get(),
            "situacao": self.obter_key_combo(self.combo_situacao),
            "conexao": self.entry_conexao.get(),
            "tipo_conexao": self.combo_tipo_conexao.get() if self.combo_tipo_conexao.current() > 0 else "",
            "rn_anterior": self.entry_rn_anterior.get(),
            "campanha": self.obter_key_combo(self.combo_campanha),
            "data_levantamento": self.entry_data_levantamento.get(),
            "data_critica": self.entry_data_critica.get(),
            "projeto": self.entry_projeto.get(),
            "nue": self.entry_nue.get(),
            "linha": self.entry_linha.get(),
            "caderneta": self.entry_caderneta.get(),
            "informante": self.entry_informante.get(),
            "unidade_informante": self.combo_unidade_informante.get() if self.combo_unidade_informante.current() > 0 else "",
            "data_coordenada": self.data_coordenada,
            "siape": self.entry_siape.get(),
            "seq": self.seq_var.get(),
            "status_vrf": self.status_vrf_var.get(),
            "municipio": self.entry_municipio.get(),
            "uf": self.obter_key_combo(self.combo_uf),
        }
        return trim_all(data)

    def limpar(self):
        # Textos
        for entry in (
            self.entry_estacao,
            self.entry_inscr_chapa,
            self.entry_conexao,
            self.entry_rn_anterior,
            self.entry_projeto,
            self.entry_nue,
            self.entry_linha,
            self.entry_caderneta,
            self.entry_informante,
            self.entry_siape,
            self.entry_municipio,
        ):
            entry.delete(0, tk.END)

        # Datas
        self.entry_data_levantamento.delete(0, tk.END)
        self.entry_data_critica.delete(0, tk.END)

        # Vars ocultas
        self.seq_var.set("")
        self.status_vrf_var.set("")

        self.data_coordenada = None
        self.set_default_value()

    def set_default_value(self):
        for combo in (
            self.combo_monumentacao,
            self.combo_tipo_local,
            self.combo_situacao,
            self.combo_tipo_conexao,
            self.combo_campanha,
            self.combo_uf,
            self.combo_unidade_informante
        ):
            combo.current(0)  # "Selecione..."
        # status label
        self._update_status_vrf()
