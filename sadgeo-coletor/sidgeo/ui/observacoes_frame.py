# -*- coding: utf-8 -*-
"""
file: /sidgeo/ui/observacoes_frame.py
Created on Wed Feb 26 10:35:12 2025
@author: pjag
"""


import tkinter as tk
from tkinter import scrolledtext

from sidgeo.util.strings import trim_all



# ---------------------------
# Classes de Interface
# ---------------------------

# Classe para o quadro de Observações (exemplo para campos de texto)
class ObservacoesFrame(tk.LabelFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, text="Observações", padx=10, pady=10, **kwargs)
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Descrição:").grid(row=0, column=0, sticky="nw", padx=5)
        self.txt_descricao = scrolledtext.ScrolledText(self, width=60, height=2)
        self.txt_descricao.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        tk.Label(self, text="Localização:").grid(row=1, column=0, sticky="nw", padx=5)
        self.txt_localizacao = scrolledtext.ScrolledText(self, width=60, height=2)
        self.txt_localizacao.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        tk.Label(self, text="Itinerário:").grid(row=2, column=0, sticky="nw", padx=5)
        self.txt_itinerario = scrolledtext.ScrolledText(self, width=60, height=2)
        self.txt_itinerario.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")

        tk.Label(self, text="Observação:").grid(row=3, column=0, sticky="nw", padx=5)
        self.txt_observacao = scrolledtext.ScrolledText(self, width=60, height=2)
        self.txt_observacao.grid(row=3, column=1, padx=5, pady=5, sticky="nsew")
        
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)

    def get_data(self):
        data = {
            "descricao": self.txt_descricao.get("1.0", tk.END),
            "localizacao": self.txt_localizacao.get("1.0", tk.END),
            "itinerario": self.txt_itinerario.get("1.0", tk.END),
            "observacao": self.txt_observacao.get("1.0", tk.END),
        }
        return trim_all(data)

    def limpar(self):
        self.txt_descricao.delete("1.0", tk.END)
        self.txt_localizacao.delete("1.0", tk.END)
        self.txt_itinerario.delete("1.0", tk.END)
        self.txt_observacao.delete("1.0", tk.END)

