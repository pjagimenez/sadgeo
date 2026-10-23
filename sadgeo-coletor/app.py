# -*- coding: utf-8 -*-
"""
file: /sidgeo/ui/sadgeo_formulario_busca.py
@created: 25-02-2025 pjag Criaçaõ do sistema com edição centrada em CSV local
@updated: 09-09-2025 pjag Mudança para usar HF5 base interna local
@updated: 16-10-2025 pjag Inclusão de busca SADGEO
@updated: 03-07-2026 pjag Refatoração MVC, GRASP, PEP8 pythonic
"""

from __future__ import annotations

# ─── Imports “do projeto” ─────────────────
from sidgeo.view.aplicativo_tela import AplicativoVisual
from sidgeo.application.controller_fabrica import  ControllerFactory
from sidgeo.infra.notificacao_evento_log import NotificadorEventoLog

def main() -> None:   

    # 2) Dependências 
    notificacao_app = NotificadorEventoLog()
    notificacao_app.instalar_excepthook()
        
    controle_app = ControllerFactory.criar(log_app= notificacao_app)

    # 3) UI
    app = AplicativoVisual(
        controle_app=controle_app,
        notificacao_app=notificacao_app
    )
    app.mainloop()
    

if __name__ == "__main__":
    main()
