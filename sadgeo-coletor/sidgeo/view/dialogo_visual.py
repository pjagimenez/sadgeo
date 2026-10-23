# -*- coding: utf-8 -*-
"""
file: /sidgeo/ui/dialogo_visual.py
@created: 03-07-2026 pjag
@updated: 03-07-2026 pjag Refatoração MVC, GRASP, PEP8 pythonic
"""
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog 
from typing import Optional, Tuple


class DialogoVisual:
    """Centraliza diálogos visuais de seleção de arquivos."""
    
    def __init__(self) -> None:
         self._app: tk.Tk | None = None  # será plugado depois

   
    def attach(self, app: tk.Tk) -> None:
        self._app = app
        
        
    def escolher_arquivo_importacao(self) -> Optional[Tuple[str, str]]:
        """Abre janela para escolher formato (CSV/JSON) e depois arquivo."""
        
        if not self._app:
            raise RuntimeError("DialogoVisual sem app. Chame attach().")
    
        modal = tk.Toplevel(self._app)
        modal.title("Importar registros")
        modal.resizable(False, False)
        modal.transient(self._app)       
        modal.grab_set()               
        modal.focus_set()
        
        modal.geometry("+%d+%d" 
                       % (
                           self._app.winfo_rootx()+40, 
                           self._app.winfo_rooty()+40
                         )
        )

        tk.Label(modal, 
                 text="Formato do arquivo:"
        ).pack(pady=10)

        formato = tk.StringVar(value="csv")
        
        ttk.Combobox(modal, 
                     textvariable=formato, 
                     values=("csv", "json"), 
                     state="readonly"
        ).pack(padx=10)

        resultado: tuple[str, str] | None = None

        def _confirmar():
            nonlocal  resultado
            
            fmt = formato.get()
            
            tipos = (
                [("CSV", "*.csv")] 
                if fmt == "csv" 
                else [("JSON", "*.json")]
            )
            
            path = filedialog.askopenfilename(        
                parent=modal, 
                title="Selecionar arquivo", 
                filetypes=tipos
            )
            
            if path:
                resultado = (path, fmt)
                
            modal.destroy()

        btns = tk.Frame(modal)
        btns.pack(fill="x", padx=10, pady=10)
        
        tk.Button(btns, 
                  text="Cancelar", 
                  command=modal.destroy
        ).pack(side="right", padx=5)
        
        tk.Button(btns, 
                  text="Escolher arquivo", 
                  command=_confirmar
        ).pack(side="right", padx=5)

        self._app.wait_window(modal)
        
        return resultado
    
    
    def escolher_arquivo_exportacao(self) -> Optional[Tuple[str, str]]:
        """Abre janela para escolher formato (CSV/JSON) e depois local para salvar."""
        
        if not self._app:
            raise RuntimeError("MensagemService sem app. Chame attach().")
    
        modal = tk.Toplevel(self._app)
        modal.title("Exportar registros")
        modal.resizable(False, False)
        modal.transient(self._app)          # ✅ associa ao app
        modal.grab_set()
        modal.focus_set()
        
        modal.geometry("+%d+%d" % (self._app.winfo_rootx()+40, self._app.winfo_rooty()+40))

        tk.Label(modal, text="Formato do arquivo:").pack(pady=10)

        formato = tk.StringVar(value="csv")
        
        ttk.Combobox(modal, 
                     textvariable=formato, 
                     values=("csv", "json"), 
                     state="readonly"
        ).pack(padx=10)

        resultado: tuple[str, str] | None = None

        def _confirmar():
            nonlocal resultado
        
            fmt = formato.get()
        
            ext = ".csv" if fmt == "csv" else ".json"
        
            tipos = (
                [("CSV", "*.csv")]
                if fmt == "csv"
                else [("JSON", "*.json")]
            )
        
            path = filedialog.asksaveasfilename(
                parent=modal,
                title="Salvar como...",
                defaultextension=ext,
                filetypes=tipos,
            )
        
            if path:
                resultado = (path, fmt)
        
            modal.destroy()

        btns = tk.Frame(modal)
        btns.pack(fill="x", padx=10, pady=10)
        
        tk.Button(btns, 
                  text="Cancelar", 
                  command=modal.destroy
        ).pack(side="right", padx=5)
        
        tk.Button(btns, 
                  text="Salvar", 
                  command=_confirmar
        ).pack(side="right", padx=5)

        self._app.wait_window(modal)
        
        return resultado
