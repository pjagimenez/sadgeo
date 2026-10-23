# -*- coding: utf-8 -*-
"""
file: /sidgeo/application/registro_servico.py
@created: 12-09-2025 pjag
@updated: 03-07-2026 pjag Refatoração MVC, GRASP, PEP8 pythonic
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sidgeo.domain.erros import ValidacaoErro
from sidgeo.domain.registro import Registro
from sidgeo.domain.registro_validador import RegistroValidador
from sidgeo.domain.foto import Foto
from sidgeo.domain.tratamento_foto import AjusteFoto

if TYPE_CHECKING:
    from sidgeo.infra.repositorio_registro import RepositorioRegistro


class RegistroServico:
    """Serviço de aplicação para operações com Registro."""

    def __init__(
        self,
        repositorio: RepositorioRegistro,
        validador: RegistroValidador,
    ) -> None:
        self.repositorio = repositorio
        self.validador = validador

    def finalizar_persistencia(self) -> None:
        self.repositorio.encerrar()

    def adicionar_foto(self, caminho: str, tipo: str) -> Foto:
        return self.repositorio.imagens.adicionar(caminho, tipo)

    def caminho_foto(self, foto: Foto) -> str:
        return str(self.repositorio.imagens.caminho(foto))

    def original_foto(self, foto: Foto) -> bytes:
        return self.repositorio.imagens.ler_original(foto.arquivo_original or foto.arquivo)

    def tratar_foto(self, foto: Foto, ajuste: AjusteFoto) -> Foto:
        return self.repositorio.imagens.tratar(foto, ajuste)

    def salvar(self, registro: Registro) -> None:
        self.validador.validar(registro)
        self.repositorio.salvar(registro)

    def excluir(self, codigo: str) -> bool:
        return self.repositorio.excluir(codigo)

    def buscar(self, codigo: str) -> Registro | None:
        return self.repositorio.buscar_por_codigo(codigo)

    def listar(self) -> list[Registro]:
        return self.repositorio.listar_todos()

    def importar(self, caminho: str, formato: str = "csv") -> int:
        """Importa registros de arquivo, valida e persiste em lote."""
        registros = self.repositorio.importar(caminho, formato)

        if not registros:
            return 0

        ok, erros = self._incluir_em_lote(registros)

        if erros:
            mensagem_erros = "\n".join(erros)
            raise ValidacaoErro(
                f"Processados {ok} com sucesso, mas houve erros:\n"
                f"{mensagem_erros}"
            )

        return ok

    def _incluir_em_lote(
        self,
        registros: list[Registro],
    ) -> tuple[int, list[str]]:
        erros: list[str] = []
        ok = 0

        for registro in registros:
            try:
                self.validador.validar(registro)
                self.repositorio.salvar(registro)
                ok += 1
            except ValidacaoErro as erro:
                erros.append(
                    f"Estação {registro.cod_estacao}: "
                    f"{'; '.join(erro.erros)}"
                )

        return ok, erros

    def exportar(self, caminho: str, formato: str) -> None:
        self.repositorio.exportar(caminho, formato)

    def zerar_base(self) -> None:
        self.repositorio.zerar_base()
