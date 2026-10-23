"""Entrada do coletor desktop SIDGEO e verificação do aplicativo empacotado."""
from __future__ import annotations

import argparse
from pathlib import Path
from tempfile import TemporaryDirectory
from PIL import Image

from sidgeo.view.aplicativo_tela import AplicativoVisual
from sidgeo.application.controller_fabrica import ControllerFactory
from sidgeo.infra.notificacao_evento_log import NotificadorEventoLog
from sidgeo.domain.registro_fabrica import RegistroFabrica
from sidgeo.domain.tratamento_foto import AjusteFoto


def executar(data_dir: Path | None = None, smoke_test: bool = False) -> None:
    notificacao = NotificadorEventoLog()
    notificacao.instalar_excepthook()
    controle = ControllerFactory.criar(notificacao, data_dir=data_dir)
    if smoke_test and data_dir is not None:
        origem = data_dir / "foto-teste.png"
        Image.new("RGB", (800, 600), "#174b75").save(origem)
        foto = controle.adicionar_foto(str(origem), "panoramica")
        foto = controle.tratar_foto(foto, AjusteFoto(codigo="9999T"))
        controle.salvar_registro(RegistroFabrica.criar({"cod_estacao": "9999T", "fotos": [foto]}))
        controle.exportar(str(data_dir / "pacote-teste.zip"), "zip")
    app = AplicativoVisual(controle_app=controle, notificacao_app=notificacao)
    if smoke_test:
        # Exercita a criação real dos widgets e a persistência com dados temporários.
        app.update_idletasks()
        app.reg_frame.lb.selection_set(0)
        app.acao_buscar()
        app.fotos_frame.lista.selection_set("0")
        app.fotos_frame.mostrar_previa()
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
