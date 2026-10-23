# -*- coding: utf-8 -*-
"""
file: /sidgeo/ui/registro_frame.py
Created on Wed Feb 26 10:35:12 2025
@author: pjag
"""
from __future__ import annotations

from collections.abc import Callable
import tkinter as tk
from sidgeo.view.mensagem_visual import MensagemVisual

# ──────────────────────────────
# 1. Controles de REGISTRO
# ──────────────────────────────
class RegistroFrame(tk.Frame):
    """Botões que afetam apenas o registro em edição + list-box."""

    def __init__(self, 
                 master: tk.Tk | tk.Toplevel,
                 msg: MensagemVisual,
                 salvar: Callable[[], None] | None = None, 
                 excluir: Callable[[], None] | None = None, 
                 limpar: Callable[[], None] | None = None, 
                 buscar: Callable[[], None] | None = None, 
                 comparar: Callable[[], None] | None = None, 
                 **kwargs,
    ) -> None:
        super().__init__(master, **kwargs)
        self._cb = {"salvar": salvar, "excluir": excluir, "limpar": limpar, "buscar": buscar, "comparar": comparar}
        self.config(width=210)
        self._build()
        

    def _build(self) -> None:
        col = 0
        for text, key in (("💾 Salvar", "salvar"), ("🗑️ Excluir", "excluir"), ("🧹 Limpar", "limpar") , ("Coord.BDG", "comparar")):
            tk.Button(self, text=text, width=10, command=self._cb[key] or (lambda: None)).grid(
                row=0, column=col, pady=2, padx=1
            )
            col += 1

        
        # --- Quadro de listagem e busca de registro para edição
        lb_frame = tk.LabelFrame(self, text="Registros (Cod.Est|Camp.|Dt.Levant.|seq.SADGEO)")
        lb_frame.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=5, pady=2)              
            
        # Listbox e Scrollbar com grid -- Dentro do Quadro
        self.lb = tk.Listbox(lb_frame, height=8, width=40)
        self.lb.config(font=("Courier New", 9))
        self.lb.grid(row=0, column=0, sticky="nsew", padx=5, pady=2)
    
        sb = tk.Scrollbar(lb_frame, orient="vertical", command=self.lb.yview)
        sb.grid(row=0, column=1, sticky="ns")
        self.lb.config(yscrollcommand=sb.set)
    
        # Botão "Editar selecionado" abaixo da listbox
        btn_buscar = tk.Button(lb_frame, width=35, text="🔍 Selecionar p/Edição", command=self._cb["buscar"] or (lambda: None))
        btn_buscar.grid(row=1, column=0,  sticky="ew", padx=5, pady=(0, 2))
    
        # Configura expansão
        #lb_frame.rowconfigure(0, weight=1)
        #lb_frame.columnconfigure(, weight=1)
                        
        self.rowconfigure(1, weight=1)
        self.grid_propagate(False)
        
        
