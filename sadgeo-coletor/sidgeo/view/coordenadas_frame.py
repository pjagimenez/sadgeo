# -*- coding: utf-8 -*-
"""
file: /sidgeo/ui/coordenadas_frame.py
Created on Wed Feb 26 10:35:12 2025
@author: pjag
"""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from sidgeo.domain.dominios import opcoes_tipo_fonte

from sidgeo.util.strings import values_with_placeholder, labels_from_opcoes
from sidgeo.view.mensagem_visual import MensagemVisual


# Classe para o quadro de Coordenadas
class CoordenadasFrame(tk.LabelFrame):
    def __init__(self, 
                 master: tk.Tk | tk.Toplevel,
                 msg: MensagemVisual, 
                 titulo:str = "Coordenadas", 
                 com_def_coord: bool = True, 
                 **kwargs
    ) -> None:
        super().__init__(master, text=titulo, padx=10, pady=2, **kwargs)
        self.com_def_coord = com_def_coord     
        self.msg = msg
        self.create_widgets()
   
    def validate_min(self, proposed: str):
        if proposed == "":
            return True
        try:
            v = int(proposed)
        except ValueError:
            return False
        return 0 <= v <= 59

    def _to_float(self, s: str) -> float:
        if "," in s and "." not in s:
            s = s.replace(",", ".")
        return float(s)

    def validate_sec(self, proposed: str):
        if proposed == "":
            return True
        try:
            v = self._to_float(proposed)
        except ValueError:
            return False
        # 0 ≤ seg < 60
        return (v >= 0) and (v < 60)

    def validate_brazil_lat_deg(self, proposed: str):
        if proposed == "":
            return True
        try:
            v = int(proposed)
        except ValueError:
            return False
        # latitude em graus absolutos no Brasil: 0..34
        return 0 <= v <= 35

    def validate_brazil_lon_deg(self, proposed: str):
        if proposed == "":
            return True
        try:
            # Só dígitos
            if not proposed.isdigit():
                return False

            # Se só tem 1 dígito, verifique se ele pode ser o primeiro dígito de 34..74
            if len(proposed) == 1:
                # longitudes 34..74 → primeiro dígito pode ser 3, 4, 5, 6 ou 7
                return proposed in "34567"

            # A partir de 2 dígitos, valide o número completo
            v = int(proposed)
        except ValueError:
            return False
        # longitudes Oeste do Brasil: 34..74
        return 30 <= v <= 80

    def _obter_key_combo(self, combo):
        conteudo = combo.get()
        if conteudo == "Selecione..." or not conteudo.strip():
            return ""
        return conteudo.split(" - ")[0]

    def create_widgets(self):
        # Latitude
        tk.Label(self, text="Latitude").grid(row=0, column=0, columnspan=2, padx=5, pady=(10, 2), sticky="w")

        tk.Label(self, text="Sinal:").grid(row=1, column=0, sticky="e", padx=5, pady=2)
        self.combo_lat_sinal = ttk.Combobox(self, values=["+", "-"], width=3, state="readonly")
        self.combo_lat_sinal.current(1)  # Brasil: -
        self.combo_lat_sinal.grid(row=1, column=1, padx=5, pady=2)

        tk.Label(self, text="Grau:").grid(row=2, column=0, sticky="e", padx=5, pady=2)
        vcmd_lat_grau = (self.register(self.validate_brazil_lat_deg), "%P")
        self.txt_lat_grau = tk.Entry(self, width=5, validate="focusout", validatecommand=vcmd_lat_grau)
        self.txt_lat_grau.grid(row=2, column=1, padx=5, pady=2)

        tk.Label(self, text="Min:").grid(row=3, column=0, sticky="e", padx=5, pady=2)
        vcmd_lat_min = (self.register(self.validate_min), "%P")
        self.txt_lat_min = tk.Entry(self, width=5, validate="focusout", validatecommand=vcmd_lat_min)
        self.txt_lat_min.grid(row=3, column=1, padx=5, pady=2)

        tk.Label(self, text="Seg:").grid(row=4, column=0, sticky="e", padx=5, pady=2)
        vcmd_lat_seg = (self.register(self.validate_sec), "%P")
        self.txt_lat_seg = tk.Entry(self, validate="focusout", width=10, validatecommand=vcmd_lat_seg)
        self.txt_lat_seg.grid(row=4, column=1, padx=5, pady=2)

        # Longitude
        tk.Label(self, text="Longitude").grid(row=0, column=2, columnspan=2, padx=5, pady=(10, 2), sticky="w")

        tk.Label(self, text="Sinal:").grid(row=1, column=2, sticky="e", padx=5, pady=2)
        self.combo_lon_sinal = ttk.Combobox(self, values=["+", "-"], width=3, state="readonly")
        self.combo_lon_sinal.current(0)  # Brasil: -
        self.combo_lon_sinal.grid(row=1, column=3, padx=5, pady=2)

        tk.Label(self, text="Grau:").grid(row=2, column=2, sticky="e", padx=5, pady=2)
        vcmd_lon_grau = (self.register(self.validate_brazil_lon_deg), "%P")
        self.txt_lon_grau = tk.Entry(self, width=5, validate="focusout", validatecommand=vcmd_lon_grau)
        self.txt_lon_grau.grid(row=2, column=3, padx=5, pady=2)

        tk.Label(self, text="Min:").grid(row=3, column=2, sticky="e", padx=5, pady=2)
        vcmd_lon_min = (self.register(self.validate_min), "%P")
        self.txt_lon_min = tk.Entry(self, width=5, validate="focusout", validatecommand=vcmd_lon_min)
        self.txt_lon_min.grid(row=3, column=3, padx=5, pady=2)

        tk.Label(self, text="Seg:").grid(row=4, column=2, sticky="e", padx=5, pady=2)
        vcmd_lon_seg = (self.register(self.validate_sec), "%P")
        self.txt_lon_seg = tk.Entry(self, validate="focusout", width=10, validatecommand=vcmd_lon_seg)
        self.txt_lon_seg.grid(row=4, column=3, padx=5, pady=2)

        # Tipo Fonte   lin=5 / Col=0..3
        tk.Label(self, text="Tipo Fonte:").grid(row=5, column=0, padx=5, pady=2, sticky="e")
        self.combo_tipo_fonte = ttk.Combobox(
            self,
            values=values_with_placeholder(labels_from_opcoes(opcoes_tipo_fonte())),
            state="readonly",
            width=30,
        )
        self.combo_tipo_fonte.grid(row=5, column=1, columnspan=3, padx=5, pady=2, sticky="w")

        qrow = 6
        self.var_atualizar_coord = tk.BooleanVar(value=True)  # True = Atualizar (default)        
        if self.com_def_coord:
            # Definição de Coordenadas (Atualizar/Manter)
            tk.Label(self, text="Definição de Coordenadas:").grid(row=qrow, column=0, padx=5, pady=(10, 2), sticky="e")
            self.rb_frame = tk.Frame(self)
            self.rb_frame.grid(row=qrow, column=1, columnspan=3, sticky="w", padx=5, pady=(10, 2))
            tk.Radiobutton(self.rb_frame, text="Atualizar", variable=self.var_atualizar_coord, value=True).pack(side="left")
            tk.Radiobutton(self.rb_frame, text="Manter", variable=self.var_atualizar_coord, value=False).pack(side="left")
            qrow = qrow +1
            
        # --- Grupo de Checkboxes: Possibilidade de Ocupação ---
        self.var_ocup_gps = tk.BooleanVar()
        self.var_ocup_mira = tk.BooleanVar()
        self.var_ocup_gravimetro = tk.BooleanVar()
        tk.Label(self, text="Possibilidade de Ocupação:").grid(
            row=qrow, column=0, columnspan=4, pady=(10, 2), sticky="w"
        )
        qrow= qrow+1

        self.chk_gps = tk.Checkbutton(self, text="GPS", variable=self.var_ocup_gps)
        self.chk_gps.grid(row=qrow, column=0, padx=5, pady=2, sticky="w")
        
        self.chk_mira = tk.Checkbutton(self, text="Mira", variable=self.var_ocup_mira)
        self.chk_mira.grid(row=qrow, column=1, padx=5, pady=2, sticky="w")
        
        self.chk_grav = tk.Checkbutton(self, text="Gravímetro", variable=self.var_ocup_gravimetro)
        self.chk_grav.grid(row=qrow, column=2, columnspan=2, padx=5, pady=2, sticky="w" )

        # Flag para excluir registro (se precisar em outro fluxo)
        self.var_excl_reg = tk.BooleanVar()

    def disable_all(self) -> None:
        # Latitude
        self.combo_lat_sinal.config(state="disabled")
        self.txt_lat_grau.config(state="disabled")
        self.txt_lat_min.config(state="disabled")
        self.txt_lat_seg.config(state="disabled")
        
        # Longitude
        self.combo_lon_sinal.config(state="disabled")
        self.txt_lon_grau.config(state="disabled")
        self.txt_lon_min.config(state="disabled")
        self.txt_lon_seg.config(state="disabled")
        
        # Tipo Fonte   lin=5 / Col=0..3
        self.combo_tipo_fonte.config(state="disabled")

        if self.com_def_coord:
            # Definição de Coordenadas (Atualizar/Manter)
            self.rb_frame.config(state="disabled")
            
        # --- Grupo de Checkboxes: Possibilidade de Ocupação ---
        self.chk_gps.config(state="disabled")
        self.chk_mira.config(state="disabled")       
        self.chk_grav.config(state="disabled")
  

    def enable_all(self) -> None:
        # Latitude
        self.combo_lat_sinal.config(state="normal")
        self.txt_lat_grau.config(state="normal")
        self.txt_lat_min.config(state="normal")
        self.txt_lat_seg.config(state="normal")
        
        # Longitude
        self.combo_lon_sinal.config(state="normal")
        self.txt_lon_grau.config(state="normal")
        self.txt_lon_min.config(state="normal")
        self.txt_lon_seg.config(state="normal")
        
        # Tipo Fonte   lin=5 / Col=0..3
        self.combo_tipo_fonte.config(state="normal")

        if self.com_def_coord:
            # Definição de Coordenadas (Atualizar/Manter)
            self.rb_frame.config(state="normal")
            
        # --- Grupo de Checkboxes: Possibilidade de Ocupação ---
        self.chk_gps.config(state="normal")
        self.chk_mira.config(state="normal")       
        self.chk_grav.config(state="normal")        

    def get_data(self):
        return {
            "lat_sinal": self.combo_lat_sinal.get(),
            "lat_grau": self.txt_lat_grau.get(),
            "lat_min": self.txt_lat_min.get(),
            "lat_seg": self.txt_lat_seg.get(),
            "lon_sinal": self.combo_lon_sinal.get(),
            "lon_grau": self.txt_lon_grau.get(),
            "lon_min": self.txt_lon_min.get(),
            "lon_seg": self.txt_lon_seg.get(),
            "tipo_fonte_coord": self._obter_key_combo(self.combo_tipo_fonte),
            "is_atualizar_coord": self.var_atualizar_coord.get(),
            "is_ocup_gps": self.var_ocup_gps.get(),
            "is_ocup_mira": self.var_ocup_mira.get(),
            "is_ocup_gravimetro": self.var_ocup_gravimetro.get(),
        }

    def limpar(self):
        self.combo_lat_sinal.current(1)  # -
        self.txt_lat_grau.delete(0, tk.END)
        self.txt_lat_min.delete(0, tk.END)
        self.txt_lat_seg.delete(0, tk.END)

        self.combo_lon_sinal.current(1)  # -
        self.txt_lon_grau.delete(0, tk.END)
        self.txt_lon_min.delete(0, tk.END)
        self.txt_lon_seg.delete(0, tk.END)

        self.combo_tipo_fonte.current(0)
        self.var_atualizar_coord.set(True)  # default: Atualizar
        self.var_ocup_gps.set(False)
        self.var_ocup_mira.set(False)
        self.var_ocup_gravimetro.set(False)

