"""Editor com prévia e controles da etiqueta nas coordenadas da foto final."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import asdict
from io import BytesIO
import json
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog

from PIL import Image, ImageTk, ImageOps

from sidgeo.application.aplicacao_controller import AplicacaoController
from sidgeo.domain.foto import Foto
from sidgeo.domain.tratamento_foto import AjusteFoto, renderizar_foto, jpeg_tratado
from sidgeo.view.mensagem_visual import MensagemVisual
from sidgeo.view.tema import ajustar_janela, AbaRolavel


class EditarFoto(tk.Toplevel):
    def __init__(self, master: tk.Misc, foto: Foto, controller: AplicacaoController,
                 mensagens: MensagemVisual, codigo: str, ao_aplicar: Callable[[Foto], None]) -> None:
        original = controller.original_foto(foto)
        super().__init__(master)
        self.foto = foto
        self.controller = controller
        self.mensagens = mensagens
        self.ao_aplicar = ao_aplicar
        self.original = original
        self.title("Tratamento da foto — redimensionamento e etiqueta")
        ajustar_janela(self, 1000, 640)
        self.transient(master.winfo_toplevel())
        self.grab_set()
        self._previa: ImageTk.PhotoImage | None = None
        botoes = ttk.Frame(self, padding=8)
        botoes.pack(side="bottom", fill="x")
        ttk.Button(botoes, text="Redimensionar foto / Atualizar prévia", command=self.atualizar).pack(side="left")
        ttk.Button(botoes, text="Aplicar ao registro", command=self.aplicar, style="Primario.TButton").pack(side="left", padx=8)
        ttk.Button(botoes, text="Salvar cópia...", command=self.salvar_copia).pack(side="left")
        ttk.Button(botoes, text="Cancelar", command=self.destroy).pack(side="right")
        corpo = AbaRolavel(self)
        corpo.pack(fill="both", expand=True, padx=8, pady=8)
        painel = corpo.conteudo
        valores = asdict(AjusteFoto(codigo=codigo.strip().upper()))
        if foto.ajustes:
            valores.update(json.loads(foto.ajustes))
        else:
            with Image.open(BytesIO(self.original)) as imagem:
                imagem = ImageOps.exif_transpose(imagem)
                imagem.thumbnail((640, 480))
                valores['horizontal'] = max(0, min(370, imagem.width - 70))
                valores['vertical'] = max(0, min(280, imagem.height - 15))
        self.campos: dict[str, tk.StringVar] = {}
        controles = ttk.Frame(painel, padding=6)
        controles.pack(fill="x")
        for indice, (chave, titulo) in enumerate((
            ('tipo_estacao', 'Tipo da estação'), ('codigo', 'Código da estação'),
            ('largura_maxima', 'Largura máxima'), ('altura_maxima', 'Altura máxima'),
            ('horizontal', 'Horizontal (X)'), ('vertical', 'Vertical (Y)'),
            ('comprimento', 'Comprimento'), ('altura', 'Altura da etiqueta'),
        )):
            coluna = (indice % 4) * 2
            linha = indice // 4
            ttk.Label(controles, text=titulo).grid(row=linha, column=coluna, padx=4, pady=4, sticky='e')
            variavel = tk.StringVar(self, str(valores[chave]))
            self.campos[chave] = variavel
            if chave == 'tipo_estacao':
                widget = ttk.Combobox(controles, textvariable=variavel, values=('SAT', 'RN', 'EG', 'EP', 'VT', 'GPS'), width=8)
            elif chave != 'codigo':
                widget = ttk.Spinbox(controles, textvariable=variavel, width=9, from_=0, to=8192,
                                     increment=1, command=self.atualizar)
            else:
                widget = ttk.Entry(controles, textvariable=variavel, width=9)
            widget.grid(row=linha, column=coluna + 1, padx=4, pady=4)
        self.redimensionar = tk.BooleanVar(self, value=valores['redimensionar'])
        ttk.Checkbutton(painel, text="Redimensionar preservando a proporção (sem ampliar fotos menores)",
                        variable=self.redimensionar).pack(anchor='w', padx=10)
        ttk.Label(painel, text="Posição e tamanho da etiqueta em pixels da foto final. A prévia parte sempre do original.",
                  wraplength=900).pack(anchor='w', padx=10, pady=8)
        self.tamanho = ttk.Label(painel, text="")
        self.tamanho.pack()
        self.previa = ttk.Label(painel, text="Clique em Atualizar prévia.", anchor='center')
        self.previa.pack(fill='both', expand=True, padx=8, pady=8)
        corpo.ativar_rolagem()
        if codigo or foto.ajustes:
            self.atualizar()

    def ajuste(self) -> AjusteFoto:
        valores = {chave: int(var.get()) for chave, var in self.campos.items() if chave not in ('tipo_estacao', 'codigo')}
        return AjusteFoto(tipo_estacao=self.campos['tipo_estacao'].get().strip().upper(),
                          codigo=self.campos['codigo'].get().strip().upper(),
                          redimensionar=self.redimensionar.get(), **valores)

    def atualizar(self) -> None:
        try:
            imagem = renderizar_foto(self.original, self.ajuste())
            self.tamanho.configure(text=f"Foto final: {imagem.width} × {imagem.height} pixels")
            imagem.thumbnail((800, 360))
            self._previa = ImageTk.PhotoImage(imagem, master=self)
            self.previa.configure(image=self._previa, text='')
        except Exception as erro:
            self.mensagens.warn(f"Confira os ajustes: {erro}", modal=True)
            self.grab_set()

    def aplicar(self) -> None:
        try:
            tratada = self.controller.tratar_foto(self.foto, self.ajuste())
            self.ao_aplicar(tratada)
            self.destroy()
        except Exception as erro:
            self.mensagens.error(f"Não foi possível tratar a foto: {erro}")
            self.grab_set()

    def salvar_copia(self) -> None:
        try:
            dados = jpeg_tratado(self.original, self.ajuste())
            caminho = filedialog.asksaveasfilename(parent=self, title="Salvar cópia tratada", defaultextension='.jpg',
                                                 filetypes=[('JPEG', '*.jpg')])
            if caminho:
                Path(caminho).write_bytes(dados)
        except Exception as erro:
            self.mensagens.error(f"Não foi possível salvar a cópia: {erro}")
            self.grab_set()
