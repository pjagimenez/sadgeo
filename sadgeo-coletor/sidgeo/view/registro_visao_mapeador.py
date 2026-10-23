# -*- coding: utf-8 -*-
"""
file: /sidgeo/ui/registro_visao_mapeador.py
@created: 02-07-2026 pjag
@updated: 02-07-2026 pjag  Refatoração MVC, GRASP, PEP8 pythonic
"""
from typing import Any

from sidgeo.util.settings import PLACEHOLDER
from sidgeo.util.parsing import parse_data

from sidgeo.view.widgets import valor_para_widget, obter_valor_completo

from sidgeo.domain.dominios import (
    TIPO_LOCAL_DICT,
    TIPO_FONTE_COORD_DICT,
    SITUACAO_MARCO_DICT,
    TIPO_CAMPANHA_DICT,
    TIPO_MONUMENTACAO_DICT,
    TIPO_UF_DICT
)

from sidgeo.domain.registro import Registro

from sidgeo.domain.registro_mapeador import RegistroMapeador

class RegistroMapeadorVisao:

    def __init__(self):
        self.mapeador = RegistroMapeador()


    def valor_para_exibicao(self, valor: Any, tipo_valor: str, combo_dict: dict[str, str] | None = None, completo: bool = False) -> Any:
        if completo and combo_dict is not None:
           return obter_valor_completo(valor_para_widget(valor,tipo_valor), combo_dict)
        else:
           return valor_para_widget(valor,tipo_valor)


    def registro_para_dict_view(self, reg: Registro) -> dict[str, Any]:
        reg_dict = self.mapeador.registro_para_dict(reg)  # base vinda do modelo

        view: dict[str, Any] = {}

        # ---- Info Básicas ----
        view["cod_estacao"] = self.valor_para_exibicao(reg_dict.get("cod_estacao"), "str")
        view["monumentacao"] = self.valor_para_exibicao(reg_dict.get("monumentacao"), "str",
                                              TIPO_MONUMENTACAO_DICT, completo=True)
        view["tipo_local"] = self.valor_para_exibicao(reg_dict.get("tipo_local"), "str",
                                            TIPO_LOCAL_DICT, completo=True)
        view["inscr_chapa"] = self.valor_para_exibicao(reg_dict.get("inscr_chapa"), "str")
        view["situacao"] = self.valor_para_exibicao(reg_dict.get("situacao"), "str",
                                          SITUACAO_MARCO_DICT, completo=True)
        view["conexao"] = self.valor_para_exibicao(reg_dict.get("conexao"), "str")

        # Lista simples (sem dicionário): usa placeholder se vazio
        tipo_conexao = self.valor_para_exibicao(reg_dict.get("tipo_conexao"), "str")
        view["tipo_conexao"] = tipo_conexao or PLACEHOLDER

        view["rn_anterior"] = self.valor_para_exibicao(reg_dict.get("rn_anterior"), "str")
        view["campanha"] = self.valor_para_exibicao(reg_dict.get("campanha"), "str",
                                          TIPO_CAMPANHA_DICT, completo=True)

        view["uf"] = self.valor_para_exibicao(reg_dict.get("uf"), "str",
                                          TIPO_UF_DICT, completo=True)

        view["data_levantamento"] = parse_data(reg_dict.get("data_levantamento"))
        view["data_critica"] = parse_data(reg_dict.get("data_critica"))

        view["municipio"] = self.valor_para_exibicao(reg_dict.get("municipio"), "str")

        for k in ("projeto", "nue", "linha", "caderneta", "informante", "siape"):
            view[k] = self.valor_para_exibicao(reg_dict.get(k), "str")

        view["seq"] = (reg_dict.get("seq", "") or "")
        view["status_vrf"] = (reg_dict.get("status_vrf", "") or "")

        # ---- Coordenadas ----
        view["lat_sinal"] = reg_dict.get("lat_sinal", "") or "-"
        view["lat_grau"]  = self.valor_para_exibicao(reg_dict.get("lat_grau"), "str")
        view["lat_min"]   = self.valor_para_exibicao(reg_dict.get("lat_min"), "str")
        view["lat_seg"]   = self.valor_para_exibicao(reg_dict.get("lat_seg"), "str")

        view["lon_sinal"] = reg_dict.get("lon_sinal", "") or "-"
        view["lon_grau"]  = self.valor_para_exibicao(reg_dict.get("lon_grau"), "str")
        view["lon_min"]   = self.valor_para_exibicao(reg_dict.get("lon_min"), "str")
        view["lon_seg"]   = self.valor_para_exibicao(reg_dict.get("lon_seg"), "str")

        view["tipo_fonte_coord"] = self.valor_para_exibicao(reg_dict.get("tipo_fonte_coord"), "str",
                                                  TIPO_FONTE_COORD_DICT, completo=True)

        view["is_atualizar_coord"] = self.valor_para_exibicao(reg_dict.get("is_atualizar_coord", False), "bool")
        view["is_ocup_gps"]        = self.valor_para_exibicao(reg_dict.get("is_ocup_gps", False), "bool")
        view["is_ocup_mira"]       = self.valor_para_exibicao(reg_dict.get("is_ocup_mira", False), "bool")
        view["is_ocup_gravimetro"] = self.valor_para_exibicao(reg_dict.get("is_ocup_gravimetro", False), "bool")

        # ---- Observações ----
        for k in ("descricao", "localizacao", "itinerario", "observacao"):
            view[k] = reg_dict.get(k, "") or ""

        return view
