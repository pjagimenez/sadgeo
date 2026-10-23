"""Transferência de registros e fotos com referências relativas e verificação de integridade."""
from __future__ import annotations

import hashlib
import os
from pathlib import Path
import tempfile
from zipfile import ZipFile, ZIP_DEFLATED

import pandas as pd

from sidgeo.domain.erros import ValidacaoErro
from sidgeo.domain.foto import ler_fotos, LIMITE_FOTO
from sidgeo.infra.csv_serializer import CsvSerializer
from sidgeo.infra.json_serializer import JsonSerializer
from sidgeo.infra.imagens_store import ImagensStore
from sidgeo.infra.persistencia_hdf import HdfDataStore


class PacoteZip:
    def __init__(self, imagens: ImagensStore) -> None:
        self.imagens = imagens

    def exportar(self, dataset: pd.DataFrame, caminho: Path) -> None:
        with tempfile.TemporaryDirectory(prefix="sidgeo-export-", dir=caminho.parent) as pasta:
            tmp = Path(pasta)
            JsonSerializer().exportar(dataset, tmp / "registros.json")
            CsvSerializer().exportar(dataset, tmp / "registros.csv")
            HdfDataStore(tmp / "sidgeo.h5").salvar(dataset)
            pacote = tmp / "pacote.zip"
            with ZipFile(pacote, "w", compression=ZIP_DEFLATED) as arquivo:
                arquivo.write(tmp / "registros.json", "registros.json")
                arquivo.write(tmp / "registros.csv", "registros.csv")
                arquivo.write(tmp / "sidgeo.h5", "sidgeo.h5")
                incluidos: set[str] = set()
                for valor in dataset.get("fotos", pd.Series(dtype=str)).dropna():
                    for foto in ler_fotos(valor):
                        if foto.arquivo not in incluidos:
                            arquivo.writestr(f"imagens/{foto.arquivo}", self.imagens.ler(foto))
                            incluidos.add(foto.arquivo)
                        if foto.arquivo_original and foto.arquivo_original not in incluidos:
                            arquivo.writestr(f"imagens/{foto.arquivo_original}", self.imagens.ler_original(foto.arquivo_original))
                            incluidos.add(foto.arquivo_original)
            os.replace(pacote, caminho)

    def importar(self, caminho: Path) -> pd.DataFrame:
        with ZipFile(caminho) as arquivo, tempfile.TemporaryDirectory(prefix="sidgeo-import-") as pasta:
            nomes = arquivo.namelist()
            if len(nomes) != len(set(nomes)) or "registros.json" not in nomes:
                raise ValidacaoErro("ZIP inválido: registros.json ausente ou nomes de arquivo duplicados.")
            if arquivo.getinfo("registros.json").file_size > 50 * 1024 * 1024:
                raise ValidacaoErro("O JSON de dados do pacote excede 50 MB.")
            dados = Path(pasta) / "registros.json"
            dados.write_bytes(arquivo.read("registros.json"))
            dataset = JsonSerializer().importar(dados)
            fotos = [foto for valor in dataset["fotos"].dropna() for foto in ler_fotos(valor)]
            # Lê apenas os nomes derivados de hashes validados, nunca extrai caminhos do ZIP.
            for foto in fotos:
                membro = f"imagens/{foto.arquivo}"
                if membro not in nomes or arquivo.getinfo(membro).file_size > LIMITE_FOTO:
                    raise ValidacaoErro(f"Foto ausente ou maior que 5 MB no pacote: {foto.nome}")
                conteudo = arquivo.read(membro)
                if len(conteudo) != foto.tamanho or hashlib.sha256(conteudo).hexdigest() != foto.sha256:
                    raise ValidacaoErro(f"Integridade da foto inválida: {foto.nome}")
                if foto.arquivo_original:
                    original = f"imagens/{foto.arquivo_original}"
                    if original not in nomes or arquivo.getinfo(original).file_size > LIMITE_FOTO:
                        raise ValidacaoErro(f"Foto original ausente ou maior que 5 MB: {foto.nome}")
                    if hashlib.sha256(arquivo.read(original)).hexdigest() != foto.arquivo_original.split(".")[0]:
                        raise ValidacaoErro(f"Integridade da foto original inválida: {foto.nome}")
            for foto in fotos:
                gravada = self.imagens.gravar(arquivo.read(f"imagens/{foto.arquivo}"), foto.tipo, foto.nome)
                if gravada.arquivo != foto.arquivo:
                    raise ValidacaoErro("Extensão da foto incompatível com o conteúdo do pacote.")
                if foto.arquivo_original:
                    gravada_original = self.imagens.gravar(arquivo.read(f"imagens/{foto.arquivo_original}"), foto.tipo, foto.nome)
                    if gravada_original.arquivo != foto.arquivo_original:
                        raise ValidacaoErro("Extensão da foto original incompatível com o conteúdo do pacote.")
            return dataset
