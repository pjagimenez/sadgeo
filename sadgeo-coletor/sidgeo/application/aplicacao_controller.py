# -*- coding: utf-8 -*-
"""
file: /sidgeo/application/aplicacao_controller.py
@created: 25-02-2025 pjag
@updated: 16-10-2025 pjag
"""
from __future__ import annotations

from sidgeo.domain.registro import Registro
from sidgeo.domain.foto import Foto
from sidgeo.domain.tratamento_foto import AjusteFoto

from sidgeo.infra.notificacao_evento_log import NotificadorEventoLog

from sidgeo.application.bdg_servico import BdgServico
from sidgeo.application.sadgeo_servico import SadgeoServico
from sidgeo.application.registro_servico import RegistroServico


class AplicacaoController:
    def __init__(self,
                 reg_servico : RegistroServico, 
                 log_servico : NotificadorEventoLog,
                 bdg_servico : BdgServico,
                 sadgeo_servico : SadgeoServico,):
        
        self.servico_reg = reg_servico
        self.servico_bdg = bdg_servico
        self.servico_sadgeo = sadgeo_servico
        self.servico_log = log_servico
        

    # ───────────────────────────── ações CRUD ─────────────────────────────
    def salvar_registro(self, registro: Registro,) -> None:
        self.servico_reg.salvar(registro)
        
    def excluir_registro(self, cod_estacao: str,) -> bool:
        return self.servico_reg.excluir(cod_estacao)        
        
    def buscar_registro(self, cod_estacao: str,) -> Registro | None:
        return self.servico_reg.buscar(cod_estacao)
       
    def zerar_base_registro(self) -> None:
       self.servico_reg.zerar_base()

    def buscar_sadgeo(self, cod_estacao: str,) -> list[Registro] | None:
        self.servico_log.info(f"Consultando SADGEO: {cod_estacao}" )
        return self.servico_sadgeo.buscar_por_estacao(cod_estacao )
       
    def buscar_bdg(self, cod_estacao: str) -> Registro | None:
       self.servico_log.info( f"Consultando BDG: {cod_estacao}" )
       return self.servico_bdg.buscar_registro_por_estacao(cod_estacao)

    def importar(self, caminho: str, formato: str,) -> int:
        return self.servico_reg.importar( caminho, formato )

    def exportar(self, caminho: str, formato: str,) -> None:
        self.servico_reg.exportar(caminho, formato )


    def listar_registros(self) -> list[Registro]:
        return self.servico_reg.listar()
    
    def finalizar_persistencia(self) -> None:
        self.servico_reg.finalizar_persistencia()

    def adicionar_foto(self, caminho: str, tipo: str) -> Foto:
        return self.servico_reg.adicionar_foto(caminho, tipo)

    def caminho_foto(self, foto: Foto) -> str:
        return self.servico_reg.caminho_foto(foto)

    def original_foto(self, foto: Foto) -> bytes:
        return self.servico_reg.original_foto(foto)

    def tratar_foto(self, foto: Foto, ajuste: AjusteFoto) -> Foto:
        return self.servico_reg.tratar_foto(foto, ajuste)
