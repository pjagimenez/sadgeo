"""Arquivos de imagem imutáveis, identificados pelo SHA-256 do conteúdo."""
from __future__ import annotations

import hashlib
from io import BytesIO
import os
from pathlib import Path
import tempfile
import json
from dataclasses import asdict, replace

from PIL import Image, UnidentifiedImageError

from sidgeo.domain.erros import ValidacaoErro
from sidgeo.domain.foto import Foto, LIMITE_FOTO
from sidgeo.domain.tratamento_foto import AjusteFoto, jpeg_tratado


class ImagensStore:
    def __init__(self, data_dir: Path) -> None:
        self.pasta = data_dir / "imagens"

    def adicionar(self, caminho: str, tipo: str) -> Foto:
        origem = Path(caminho)
        if origem.stat().st_size > LIMITE_FOTO:
            raise ValidacaoErro("Cada foto pode ter no máximo 5 MB (5.242.880 bytes).")
        return self.gravar(origem.read_bytes(), tipo, origem.name)

    def gravar(self, dados: bytes, tipo: str, nome: str) -> Foto:
        if not 0 < len(dados) <= LIMITE_FOTO:
            raise ValidacaoErro("Foto vazia ou maior que o limite de 5 MB.")
        try:
            with Image.open(BytesIO(dados)) as imagem:
                formato = imagem.format
                imagem.verify()
            if formato not in ("JPEG", "PNG"):
                raise ValidacaoErro("Use uma foto JPEG ou PNG.")
        except (UnidentifiedImageError, OSError, Image.DecompressionBombError) as erro:
            raise ValidacaoErro(f"Não foi possível ler a imagem: {erro}") from erro
        sha = hashlib.sha256(dados).hexdigest()
        foto = Foto(tipo, nome, f"{sha}.{'jpg' if formato == 'JPEG' else 'png'}", len(dados), sha)
        self.pasta.mkdir(parents=True, exist_ok=True)
        destino = self.pasta / foto.arquivo
        if destino.exists() and hashlib.sha256(destino.read_bytes()).hexdigest() == sha:
            return foto
        fd, nome_temp = tempfile.mkstemp(prefix="foto-", dir=self.pasta)
        temporario = Path(nome_temp)
        try:
            with os.fdopen(fd, "wb") as arquivo:
                arquivo.write(dados)
            os.replace(temporario, destino)
        finally:
            temporario.unlink(missing_ok=True)
        return foto

    def caminho(self, foto: Foto) -> Path:
        destino = self.pasta / foto.arquivo
        if not destino.is_file():
            raise ValidacaoErro(f"Foto '{foto.nome}' não encontrada. Importe o ZIP com as imagens.")
        return destino

    def ler(self, foto: Foto) -> bytes:
        dados = self.caminho(foto).read_bytes()
        if len(dados) != foto.tamanho or hashlib.sha256(dados).hexdigest() != foto.sha256:
            raise ValidacaoErro(f"A foto '{foto.nome}' não corresponde ao tamanho/hash registrado.")
        return dados

    def ler_original(self, arquivo: str) -> bytes:
        # A referência original usa o mesmo formato de nome validado de Foto.
        referencia = Foto("outra", "Original", arquivo, 1, arquivo.split(".")[0])
        caminho = self.caminho(referencia)
        if caminho.stat().st_size > LIMITE_FOTO:
            raise ValidacaoErro("A foto original excede 5 MB.")
        dados = caminho.read_bytes()
        if hashlib.sha256(dados).hexdigest() != referencia.sha256:
            raise ValidacaoErro("Hash da foto original inválido.")
        return dados

    def tratar(self, foto: Foto, ajuste: AjusteFoto) -> Foto:
        original = foto.arquivo_original or foto.arquivo
        dados = jpeg_tratado(self.ler_original(original), ajuste)
        tratada = self.gravar(dados, foto.tipo, foto.nome)
        return replace(tratada, arquivo_original=original, ajustes=json.dumps(asdict(ajuste), ensure_ascii=False))
