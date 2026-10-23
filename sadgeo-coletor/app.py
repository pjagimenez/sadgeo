"""Entrada do coletor desktop SIDGEO e verificação do aplicativo empacotado."""
from __future__ import annotations

import argparse
from pathlib import Path
from tempfile import TemporaryDirectory

from sidgeo.view.aplicativo_tela import AplicativoVisual
from sidgeo.application.controller_fabrica import ControllerFactory
from sidgeo.infra.notificacao_evento_log import NotificadorEventoLog


def executar(data_dir: Path | None = None, smoke_test: bool = False) -> None:
    notificacao = NotificadorEventoLog()
    notificacao.instalar_excepthook()
    controle = ControllerFactory.criar(notificacao, data_dir=data_dir)
    app = AplicativoVisual(controle_app=controle, notificacao_app=notificacao)
    if smoke_test:
        # Exercita a criação real dos widgets e a persistência com dados temporários.
        app.update_idletasks()
        controle.finalizar_persistencia()
        app.after(300, app.destroy)
    app.mainloop()
    notificacao.info("Teste de inicialização concluído." if smoke_test else "Aplicação encerrada.")


def main() -> None:
    parser = argparse.ArgumentParser(description="SIDGEO — Coletor de campo")
    parser.add_argument("--smoke-test", action="store_true",
                        help="abre e fecha o aplicativo usando uma base temporária, sem consultar APIs")
    args = parser.parse_args()
    if args.smoke_test:
        with TemporaryDirectory(prefix="sidgeo-teste-") as pasta:
            executar(Path(pasta), smoke_test=True)
    else:
        executar()


if __name__ == "__main__":
    main()
