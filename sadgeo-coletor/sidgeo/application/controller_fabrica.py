# -*- coding: utf-8 -*-
"""
file: /sidgeo/application/controller_fabrica.py
@created: 03-07-2026 pjag
@updated: 03-07-2026 pjag Refatoração MVC, GRASP, PEP8 pythonic
"""

from sidgeo.application.bdg_servico import BdgServico
from sidgeo.application.sadgeo_servico import SadgeoServico
from sidgeo.application.registro_servico import RegistroServico
from sidgeo.application.aplicacao_controller import AplicacaoController

from sidgeo.util.settings import APP_URL_BDG, APP_URL_SADGEO

from sidgeo.infra.notificacao_evento_log import NotificadorEventoLog
from sidgeo.infra.repositorio_registro import RepositorioRegistro

from sidgeo.domain.registro_mapeador import RegistroMapeador
from sidgeo.domain.registro_validador import RegistroValidador

from sidgeo.infra.bdg_client import BdgClient
from sidgeo.infra.sadgeo_client import SadgeoClient


class ControllerFactory:

    @staticmethod
    def criar(log_app : NotificadorEventoLog):

        log_servico = log_app
        mapeador = RegistroMapeador()

        repo = RepositorioRegistro(log_servico, mapeador)

        validador = RegistroValidador()

        bdg_api = BdgClient(base_url= APP_URL_BDG)
        
        sadgeo_api = SadgeoClient(base_url= APP_URL_SADGEO )
        
        registro_servico = RegistroServico(
            repositorio=repo,
            validador=validador,
        )

        sadgeo_servico = SadgeoServico(sadgeo_api, mapeador)

        bdg_servico = BdgServico(bdg_api, mapeador)

        return AplicacaoController (            
            reg_servico = registro_servico, 
            log_servico = log_servico,
            bdg_servico = bdg_servico,
            sadgeo_servico = sadgeo_servico,
        )
