# -*- coding: utf-8 -*-
#file: imagem_model.py

from datetime import datetime, date
from dataclasses import dataclass
from enum import StrEnum


class TipoImagem(StrEnum):
    PANORAMICA = "PANORAMICA"
    CHAPA = "CHAPA"
    SITUACAO = "SITUACAO"
    CROQUI = "CROQUI"


@dataclass(slots=True)
class IdentificacaoImagem:
    nome_arquivo_original: str
    codigo_estacao: str
    tipo_imagem: TipoImagem
    origem_sadgeo: bool

# ========================================================
# T_IMAGEM
# ========================================================

@dataclass(slots=True)
class TImagem:
    
    # Identificação
    uuid_imagem: bytes | None= None
    tx_hash: str | None= None
    dt_hash: datetime | None= None

    # Arquivo
    nr_tamanho_arquivo: int | None = None
    nr_largura_imagem: int | None = None
    nr_altura_imagem: int | None = None
    tx_dpi : str | None = None

    # Equipamento
    tx_fabricante_dispositivo: str | None = None
    tx_modelo_dispositivo: str | None = None

    # Captura
    dt_captura_imagem_original: datetime | None = None
    tx_iso_imagem: str | None = None
    tx_abertura_imagem: str | None = None
    tx_tempo_exposicao: str | None = None
    tx_distancia_focal: str | None = None

    # Resolução
    nr_resolucao_horizontal: float | None = None
    nr_resolucao_vertical: float | None = None

    # GPS
    gps_latitude: float | None = None
    gps_longitude: float | None = None
    gps_altitude: float | None = None

    tx_modo_flash: str | None = None
    tx_balanco_de_branco: str | None = None
    tx_orientacao: str | None = None
  

# ========================================================
# T_IMAGEM_CONTEUDO
# ========================================================
@dataclass(slots=True)
class TImagemConteudo:
    uuid_imagem: bytes | None= None
    bl_imagem: bytes | None= None


# ========================================================
# T_IMAGEM_ESTACAO
# ========================================================
@dataclass(slots=True)
class TImagemEstacao:

    id_imagem_estacao: int | None= None

    uuid_imagem: bytes | None= None

    cd_estacao: str | None= None

    sq_sadgeo: str | None= None

    tp_imagem: str | None= None

    ds_origem: str | None= None

    tx_hash_arquivo: str | None= None

    nm_arquivo_origem: str | None= None

    dt_inicio_vigencia: date | None= None

    dt_fim_vigencia: date| None = None


# ========================================================
# T_IMAGEM_REPOSITORIO
# ========================================================
@dataclass(slots=True)
class TImagemRepositorio:

    id_imagem_repositorio: int | None= None

    uuid_imagem: bytes | None= None

    id_repositorio: int | None= None

    nm_arquivo: str | None= None

    dt_criacao_arquivo: datetime | None = None

    dt_modificacao_arquivo: datetime | None = None
    
    tx_metadados_dump: str | None = None    
    
    tx_erros_dump: str | None = None


# ========================================================
# T_REPOSITORIO_IMAGEM
# ========================================================
@dataclass(slots=True)
class TRepositorioImagem:

    id_repositorio: int | None= None

    nm_repositorio: str| None  = None

    ds_servidor: str| None = None

    fl_uso: str| None = None

    fl_tipo: str| None = None

    ds_local_imagem_croqui: str | None = None

    ds_local_imagem_panoramica: str | None = None

    ds_local_imagem_chapa: str | None = None

    ds_local_imagem_situacao: str | None = None
