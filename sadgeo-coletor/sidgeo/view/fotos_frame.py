"""Fotos da estação, com prévia reduzida e arquivos originais mantidos no perfil do usuário."""
from __future__ import annotations

import tkinter as tk
from collections.abc import Callable
from tkinter import ttk, filedialog

from PIL import Image, ImageOps, ImageTk

from sidgeo.application.aplicacao_controller import AplicacaoController
from sidgeo.domain.foto import Foto, TIPOS_FOTO
from sidgeo.view.mensagem_visual import MensagemVisual
from sidgeo.view.editar_foto import EditarFoto


class FotosFrame(ttk.Frame):
    def __init__(self, master: tk.Misc, msg: MensagemVisual, controller: AplicacaoController, obter_codigo: Callable[[], str]) -> None:
        super().__init__(master, padding=10)
        self.msg = msg
        self.controller = controller
        self.obter_codigo = obter_codigo
        self.fotos: list[Foto] = []
        self._previa: ImageTk.PhotoImage | None = None
        self.resumo = ttk.Label(self, text="")
        self.resumo.pack(anchor="w", pady=(0, 8))
        botoes = ttk.Frame(self)
        botoes.pack(fill="x")
        for tipo, titulo in TIPOS_FOTO.items():
            ttk.Button(botoes, text=f"Adicionar {titulo.lower()}",
                       command=lambda t=tipo: self.adicionar(t)).pack(side="left", padx=(0, 6))
        ttk.Label(self, text="JPEG/PNG · até 5 MB por foto · salve o registro para confirmar os vínculos.",
                  wraplength=620).pack(anchor="w", pady=8)
        lista = ttk.Frame(self)
        lista.pack(fill="x")
        self.lista = ttk.Treeview(lista, columns=("tipo", "nome", "tamanho"), show="headings", height=5)
        for coluna, titulo, largura in (("tipo", "Tipo", 90), ("nome", "Arquivo original", 290), ("tamanho", "Tamanho", 85)):
            self.lista.heading(coluna, text=titulo)
            self.lista.column(coluna, width=largura, minwidth=60, stretch=coluna == "nome")
        self.lista.pack(side="left", fill="x", expand=True)
        barra = ttk.Scrollbar(lista, orient="vertical", command=self.lista.yview)  # pyright: ignore[reportUnknownMemberType, reportUnknownArgumentType]
        barra.pack(side="right", fill="y")
        self.lista.configure(yscrollcommand=barra.set)
        self.lista.bind("<<TreeviewSelect>>", self.mostrar_previa)
        ttk.Button(self, text="Remover vínculo da foto selecionada", command=self.remover).pack(anchor="w", pady=8)
        ttk.Button(self, text="Redimensionar foto / Ajustar etiqueta", command=self.editar).pack(anchor="w", pady=4)
        self.previa = ttk.Label(self, text="Selecione uma foto para visualizar.", anchor="center")
        self.previa.pack(fill="both", expand=True)
        self.atualizar()

    def adicionar(self, tipo: str) -> None:
        caminho = filedialog.askopenfilename(parent=self, title=f"Foto — {TIPOS_FOTO[tipo]}",
                                            filetypes=[("Imagens JPEG/PNG", "*.jpg *.jpeg *.png")])
        if not caminho:
            return
        try:
            foto = self.controller.adicionar_foto(caminho, tipo)
            if foto not in self.fotos:
                self.fotos.append(foto)
            self.atualizar()
            self.lista.selection_set(str(self.fotos.index(foto)))
        except Exception as erro:
            self.msg.error(f"Não foi possível adicionar a foto: {erro}")

    def atualizar(self) -> None:
        self.lista.delete(*self.lista.get_children())
        for indice, foto in enumerate(self.fotos):
            self.lista.insert("", "end", iid=str(indice), values=(TIPOS_FOTO[foto.tipo], foto.nome, f"{foto.tamanho / 1024:.0f} KB"))
        panorama = sum(foto.tipo == "panoramica" for foto in self.fotos)
        chapa = sum(foto.tipo == "chapa" for foto in self.fotos)
        self.resumo.configure(text=f"Panorâmica: {panorama}   |   Chapa: {chapa}   |   Total: {len(self.fotos)}")
        faltantes = [nome for quantidade, nome in ((panorama, "panorâmica"), (chapa, "chapa")) if not quantidade]
        if faltantes:
            self.resumo.configure(text=self.resumo.cget("text") + "   |   Faltam: " + ", ".join(faltantes))
        self._previa = None
        self.previa.configure(image="", text="Selecione uma foto para visualizar.")

    def mostrar_previa(self, _evento: tk.Event | None = None) -> None:
        selecao = self.lista.selection()
        if not selecao:
            return
        try:
            foto = self.fotos[int(selecao[0])]
            with Image.open(self.controller.caminho_foto(foto)) as original:
                imagem = ImageOps.exif_transpose(original)
                imagem.thumbnail((560, 180))
                self._previa = ImageTk.PhotoImage(imagem, master=self)
            self.previa.configure(image=self._previa, text="")
        except Exception as erro:
            self.previa.configure(image="", text=f"Prévia indisponível: {erro}")

    def remover(self) -> None:
        selecao = self.lista.selection()
        if not selecao:
            return
        if self.msg.confirm("Remover o vínculo desta foto com o registro? O arquivo original será preservado."):
            self.fotos.pop(int(selecao[0]))
            self.atualizar()

    def editar(self) -> None:
        selecao = self.lista.selection()
        if not selecao:
            self.msg.warn("Selecione uma foto para tratar.", modal=True)
            return
        indice = int(selecao[0])
        def aplicar(foto: Foto) -> None:
            self.fotos[indice] = foto
            self.atualizar()
            self.lista.selection_set(str(indice))
        try:
            EditarFoto(self, self.fotos[indice], self.controller, self.msg, self.obter_codigo(), aplicar)
        except Exception as erro:
            self.msg.error(f"Não foi possível abrir a foto: {erro}")

    def definir_fotos(self, fotos: list[Foto]) -> None:
        self.fotos = list(fotos)
        self.atualizar()

    def get_data(self) -> dict[str, object]:
        return {"fotos": list(self.fotos)}

    def limpar(self) -> None:
        self.definir_fotos([])
