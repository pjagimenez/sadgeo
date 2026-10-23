"""Tema e containers redimensionáveis compartilhados pelas telas do coletor."""
from __future__ import annotations

import tkinter as tk
from tkinter import font, ttk

FUNDO = "#f4f6f8"
AZUL = "#112e34"
TEXTO = "#1c3038"


def aplicar_tema(app: tk.Tk) -> None:
    for nome in ("TkDefaultFont", "TkTextFont", "TkMenuFont"):
        font.nametofont(nome).configure(size=9)
    app.configure(background=FUNDO)
    for chave, valor in {
        "*Background": FUNDO, "*Foreground": TEXTO,
        "*Entry.Background": "white", "*Text.Background": "white",
        "*Listbox.Background": "white", "*selectBackground": AZUL,
        "*selectForeground": "white", "*Button.relief": "flat",
        "*Button.padX": 8, "*Button.padY": 4,
    }.items():
        app.option_add(chave, valor)  # pyright: ignore[reportUnknownMemberType]
    estilo = ttk.Style(app)
    estilo.theme_use("clam")
    estilo.configure(".", background=FUNDO, foreground=TEXTO)
    estilo.configure("TButton", padding=(10, 6))
    estilo.configure("Primario.TButton", background="#007f70", foreground="white")
    estilo.map("Primario.TButton", background=[("active", "#006457")])
    estilo.configure("Perigo.TButton", foreground="#a52232")
    estilo.configure("TNotebook", borderwidth=0)
    estilo.configure("TNotebook.Tab", padding=(12, 8))
    estilo.map("TNotebook.Tab", background=[("selected", "white")])
    estilo.configure("Treeview", background="white", fieldbackground="white", rowheight=23)
    estilo.configure("Treeview.Heading", font=("TkDefaultFont", 9, "bold"))
    estilo.map("TCombobox", fieldbackground=[("readonly", "white")],
               foreground=[("readonly", TEXTO)])


def estilizar_quadro(widget: tk.Misc) -> None:
    """Painéis brancos e bordas leves, preservando os widgets de entrada existentes."""
    if isinstance(widget, (tk.LabelFrame, tk.Frame, tk.Label, tk.Checkbutton, tk.Radiobutton)):
        widget.configure(background="white")
    if isinstance(widget, tk.LabelFrame):
        widget.configure(relief="flat", borderwidth=0)
    for filho in widget.winfo_children():
        estilizar_quadro(filho)


def ajustar_janela(janela: tk.Tk | tk.Toplevel, largura: int, altura: int) -> None:
    """Reserva espaço para as bordas e a barra de tarefas, inclusive em 1366×768."""
    largura = min(largura, max(320, janela.winfo_screenwidth() - 40))
    altura = min(altura, max(240, janela.winfo_screenheight() - 100))
    x = max(0, (janela.winfo_screenwidth() - largura) // 2)
    y = max(0, (janela.winfo_screenheight() - altura - 50) // 2)
    janela.geometry(f"{largura}x{altura}+{x}+{y}")


class AbaRolavel(ttk.Frame):
    """Mantém campos acessíveis em janelas menores ou com escala de fonte maior."""

    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master)
        self.canvas = tk.Canvas(self, background=FUNDO, highlightthickness=0)
        self.vertical = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)  # pyright: ignore[reportUnknownMemberType, reportUnknownArgumentType]
        self.horizontal = ttk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)  # pyright: ignore[reportUnknownMemberType, reportUnknownArgumentType]
        self.canvas.configure(yscrollcommand=self.vertical.set, xscrollcommand=self.horizontal.set)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.conteudo = ttk.Frame(self.canvas)
        self._item = self.canvas.create_window(0, 0, window=self.conteudo, anchor="nw")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.conteudo.bind("<Configure>", self._redimensionar)
        self.canvas.bind("<Configure>", self._redimensionar)
        # Bindtag local: não intercepta a roda da listagem, dos textos ou de outras janelas.
        self._tag_roda = f"AbaRolavel_{id(self)}"
        self.canvas.bind_class(self._tag_roda, "<MouseWheel>", self._rolar)
        self.canvas.bind_class(self._tag_roda, "<Button-4>", self._rolar)
        self.canvas.bind_class(self._tag_roda, "<Button-5>", self._rolar)

    def ativar_rolagem(self) -> None:
        def visitar(widget: tk.Misc) -> None:
            if widget.winfo_class() not in ("Text", "Listbox", "TCombobox"):
                widget.bindtags((*widget.bindtags(), self._tag_roda))
            for filho in widget.winfo_children():
                visitar(filho)
        visitar(self.canvas)

    def _rolar(self, evento: tk.Event) -> str:
        unidades = -1 if evento.num == 4 else 1 if evento.num == 5 else -int(evento.delta / 120)
        if self.canvas.yview() != (0.0, 1.0):  # pyright: ignore[reportUnknownMemberType]
            self.canvas.yview_scroll(unidades, "units")
        return "break"

    def _redimensionar(self, _evento: tk.Event) -> None:
        largura = max(self.canvas.winfo_width(), self.conteudo.winfo_reqwidth())
        altura = max(self.canvas.winfo_height(), self.conteudo.winfo_reqheight())
        self.canvas.itemconfigure(self._item, width=largura, height=altura)
        self.canvas.configure(scrollregion=(0, 0, largura, altura))
        if self.conteudo.winfo_reqheight() > self.canvas.winfo_height():
            self.vertical.grid(row=0, column=1, sticky="ns")
        else:
            self.vertical.grid_remove()
        if self.conteudo.winfo_reqwidth() > self.canvas.winfo_width():
            self.horizontal.grid(row=1, column=0, sticky="ew")
        else:
            self.horizontal.grid_remove()
