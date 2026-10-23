# -*- coding: utf-8 -*-
"""
file: /sidgeo/domain/registro.py
@created: 26-02-2025 pjag
@updated: 02-07-2026 pjag
"""

 # pylint: disable=too-many-instance-attributes
 
from dataclasses import dataclass, field
from datetime import datetime
from sidgeo.domain.foto import Foto

@dataclass(slots=True)
class Registro: 
    """Classe de representação de linha completa de dados de estação geodésica"""
    versao_app: str
    cod_estacao: str
    monumentacao: str
    tipo_local: str
    inscr_chapa: str
    situacao: str
    conexao: str
    tipo_conexao: str
    rn_anterior: str
    campanha: str
    data_levantamento: datetime | None
    data_critica: datetime | None
    projeto: str
    nue: str
    linha: str
    caderneta: str
    # outros
    informante: str
    siape: str
    # Coordenadas
    tipo_fonte_coord: str  # novo v3
    lat_sinal: str
    lat_grau: int
    lat_min: int
    lat_seg: float
    lon_sinal: str
    lon_grau: int
    lon_min: int
    lon_seg: float
    is_atualizar_coord: bool  # novo v3
    # Possibilidade de Ocupação
    is_ocup_gps: bool
    is_ocup_mira: bool
    is_ocup_gravimetro: bool
    # Observações
    descricao: str
    localizacao: str
    itinerario: str
    observacao: str
    seq: str   # novo v2
    status_vrf: str  # novo v2
    municipio: str
    uf: str
    unidade_informante: str = ""
    data_coordenada: datetime | None = None
    fotos: list[Foto] = field(default_factory=lambda: list[Foto]())
