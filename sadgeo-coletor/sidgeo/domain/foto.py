"""Referências de fotos; o conteúdo binário fica fora do HDF5, CSV e JSON."""
from __future__ import annotations

from dataclasses import dataclass
import json
import re
from typing import Any, cast

from sidgeo.domain.erros import ValidacaoErro

LIMITE_FOTO = 5 * 1024 * 1024
TIPOS_FOTO = {"panoramica": "Panorâmica", "chapa": "Chapa", "outra": "Outra"}


@dataclass(frozen=True, slots=True)
class Foto:
    tipo: str
    nome: str
    arquivo: str
    tamanho: int
    sha256: str
    arquivo_original: str = ""
    ajustes: str = ""

    def __post_init__(self) -> None:
        if (self.tipo not in TIPOS_FOTO or not re.fullmatch(r"[a-f0-9]{64}\.(jpg|png)", self.arquivo)
                or self.arquivo.split(".")[0] != self.sha256 or not 0 < self.tamanho <= LIMITE_FOTO):
            raise ValidacaoErro("Referência de foto inválida (tipo, caminho, tamanho ou hash).")
        if self.arquivo_original and not re.fullmatch(r"[a-f0-9]{64}\.(jpg|png)", self.arquivo_original):
            raise ValidacaoErro("Referência da foto original inválida.")


def ler_fotos(valor: Any) -> list[Foto]:
    if valor is None or valor == "":
        return []
    try:
        itens = json.loads(valor) if isinstance(valor, str) else valor
        if not isinstance(itens, list):
            raise ValueError("Esperada uma lista de fotos.")
        return [item if isinstance(item, Foto) else Foto(**item) for item in cast(list[Any], itens)]
    except (ValueError, TypeError, KeyError) as erro:
        raise ValidacaoErro(f"Metadados de fotos inválidos: {erro}") from erro
