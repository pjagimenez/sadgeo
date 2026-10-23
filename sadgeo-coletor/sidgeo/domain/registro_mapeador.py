# -*- coding: utf-8 -*-
"""
file: /sidgeo/domain/registro_mapeador.py
@created: 12-09-2025 pjag
@updated: 03-07-2026 pjag Refatoração MVC, GRASP, PEP8 pythonic
"""

from __future__ import annotations

from dataclasses import asdict
import json
import unicodedata
from typing import Any, cast

import pandas as pd

from sidgeo.util.geofuncoes import parse_gms
from sidgeo.domain.registro import Registro
from sidgeo.domain.registro_fabrica import RegistroFabrica
from sidgeo.domain.dominios import (
    SITUACAO_MARCO_DICT,
    TIPO_FONTE_COORD_DICT,
)


class RegistroMapeador:
    """Converte dados externos/DataFrame para Registro e vice-versa."""

    def dict_para_registro(self, dados: dict[str, Any]) -> Registro:
        """Converte do padrão python Dict para o conjunto do formato interno da aplicação."""
        return RegistroFabrica.criar(dados)

    def dict_sadgeo_para_registro(self, dados: dict[str, Any]) -> Registro:
        """Converte do padrão Dict oriundo od SADGEO para o conjunto do formato interno da aplicação."""
        dados_normalizados = self.renomear_campos_sadgeo(dados)
        return RegistroFabrica.criar(dados_normalizados)

    def dict_bdg_para_registro(self, dados: dict[str, Any]) -> Registro:
        """Converte do padrão Dict oriundo do BDG para o conjunto do formato interno da aplicação."""
        dados_normalizados = self.renomear_campos_bdg(dados)
        return RegistroFabrica.criar(dados_normalizados)

    @staticmethod
    def registro_para_dict(registro: Registro) -> dict[str, Any]:
        """Converte o conjunto do formato interno da aplicação para padrão python Dict."""
        dados = asdict(registro)
        dados["fotos"] = json.dumps(dados["fotos"], ensure_ascii=False)
        return dados

    def df_para_registros(self, df: pd.DataFrame) -> list[Registro]:
        """Converte do padrão Panda DataFrame para o conjunto do formato interno da aplicação."""
        registros: list[Registro] = []
        # Colunas opcionais ausentes não devem virar os textos '<NA>', 'nan' ou 'NaT'.
        for linha in df.to_dict(orient="records"):
            dados = {str(chave): None if pd.isna(valor) else valor for chave, valor in linha.items()}
            registros.append(self.dict_para_registro(dados))

        return registros


    def registros_para_df(self, registros: list[Registro]) -> pd.DataFrame:
        """Converte o conjunto do formato interno da aplicação para padrão Panda DataFrame."""
        return pd.DataFrame([
            self.registro_para_dict(registro)
            for registro in registros
        ])

    @staticmethod
    def renomear_campos_sadgeo(origem: dict[str, Any]) -> dict[str, Any]:
        """Ajusta os nomes dos campos do conjunto origem SADGEO para o padrão de nomes internos da aplicação."""
        mapeamento = {
            "codEstacao": "cod_estacao",
            "tipoMonumentacao": "monumentacao",
            "tipoLocal": "tipo_local",
            "inscricaoChapa": "inscr_chapa",
            "codSituacaoMarcoPrincipal": "situacao",
            "nomenclatConex": "conexao",
            "tipoConexao": "tipo_conexao",
            "rnAnterior": "rn_anterior",
            "campanha": "campanha",
            "datFimLevantamento": "data_levantamento",
            "datCritica": "data_critica",
            "projeto": "projeto",
            "etapaPta": "nue",
            "linha": "linha",
            "caderneta": "caderneta",
            "anotador": "informante",
            "siapeAnotador": "siape",
            "codFonteCoord": "tipo_fonte_coord",
            "sinalLat": "lat_sinal",
            "grauLat": "lat_grau",
            "minLat": "lat_min",
            "segLat": "lat_seg",
            "sinalLon": "lon_sinal",
            "grauLon": "lon_grau",
            "minLon": "lon_min",
            "segLon": "lon_seg",
            "iocupacaoGps": "is_ocup_gps",
            "iocupacaoNivel": "is_ocup_mira",
            "iocupacaoGravimetro": "is_ocup_gravimetro",
            "dscEstacao": "descricao",
            "dscLocalizacao": "localizacao",
            "dscItinerario": "itinerario",
            "dscObservacao": "observacao",
            "seq": "seq",
            "statusVrf": "status_vrf",
            "municipio": "municipio",
            "uf": "uf",
            "unidadeInformante": "unidade_informante",
            "dataCoordenada": "data_coordenada",
        }

        return {
            chave_destino: origem.get(chave_origem)
            for chave_origem, chave_destino in mapeamento.items()
        }

    @staticmethod
    def renomear_campos_bdg(origem: dict[str, Any]) -> dict[str, Any]:
        """Ajusta os nomes dos campos do conjunto origem BDG para o padrão de nomes internos da aplicação"""
        lat = parse_gms(origem.get("latitudeGMS"))
        lon = parse_gms(origem.get("longitudeGMS"))

        cod_situacao = RegistroMapeador._codigo_por_descricao(
            SITUACAO_MARCO_DICT,
            origem.get("situacao"),
        )
        cod_fonte = RegistroMapeador._codigo_por_descricao(
            TIPO_FONTE_COORD_DICT,
            origem.get("fonteCoordenada"),
        )

        municipio = cast(dict[str, Any], origem.get("municipio") or {})
        uf = cast(dict[str, Any], municipio.get("uf") or {})

        nome_municipio = str(municipio.get("nomeMunicipio", ""))
        sigla_uf = str(uf.get("sigla", ""))

        return {
            "cod_estacao": origem.get("codigoEstacao"),
            "monumentacao": "",
            "tipo_local": origem.get("tipoLocal"),
            "inscr_chapa": origem.get("inscricaoChapa"),
            "situacao": cod_situacao,
            "conexao": "",
            "tipo_conexao": "",
            "rn_anterior": origem.get("codigoEstacaoMaterializada") or "",
            "campanha": origem.get("tema") or "",
            "data_levantamento": origem.get("dataVisita"),
            "data_coordenada": origem.get("dataCoordenada") or origem.get("dataCoordenadas"),
            "data_critica": "",
            "projeto": "",
            "nue": "",
            "linha": "",
            "caderneta": "",
            "informante": "",
            "siape": "",
            "tipo_fonte_coord": cod_fonte,
            "lat_sinal": lat["sinal"],
            "lat_grau": lat["grau"],
            "lat_min": lat["min"],
            "lat_seg": lat["seg"],
            "lon_sinal": lon["sinal"],
            "lon_grau": lon["grau"],
            "lon_min": lon["min"],
            "lon_seg": lon["seg"],
            "is_atualizar_coord": "",
            "is_ocup_gps": "",
            "is_ocup_mira": "",
            "is_ocup_gravimetro": "",
            "descricao": origem.get("descricaoEstacao"),
            "localizacao": origem.get("localizacao"),
            "itinerario": origem.get("itinerario"),
            "observacao": origem.get("observacao"),
            "seq": "",
            "status_vrf": "",
            "municipio": nome_municipio,
            "uf": sigla_uf,
        }


    @staticmethod
    def _codigo_por_descricao(
        dicionario: dict[str, str],
        descricao: str | None,
    ) -> str:
        """Normaliza o codigo a partir da descrição textual onde o código está inserido"""
        if not descricao:
            return ""

        chave = str(descricao).strip()
        if chave in dicionario:
            return chave
        def normalizar(texto: str) -> str:
            return "".join(letra for letra in unicodedata.normalize("NFD", texto.casefold().strip())
                           if unicodedata.category(letra) != "Mn")
        descricao_normalizada = normalizar(chave)
        for codigo, texto in dicionario.items():
            if normalizar(str(texto)) == descricao_normalizada:
                return str(codigo)

        return ""
