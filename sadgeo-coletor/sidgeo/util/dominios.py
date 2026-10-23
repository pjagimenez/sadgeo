# -*- coding: utf-8 -*-
"""
file: /sidgeo/util/dados_globais.py
@created: 26-02-2025 pjag
@updated: 12-09-2025 pjag
"""

# -------------------------
# Monumentação
# -------------------------

TIPO_MONUMENTACAO_DICT = {
    "C": "Chapa",
    "P": "Pino",
    "M": "Marco",
}

# -------------------------
# Tipo de conexão (lista simples)
# -------------------------
TIPO_CONEXAO_LIST = [
    "DOPPLER",
    "EG",
    "EP",
    "GPS",
    "RN",
    "VT",
]

# -------------------------
# Tipo de Local (códigos em UPPER com descrição)
# -------------------------
TIPO_LOCAL_DICT = {
    "AC": "Açude, sangradouro, represa, vertedouro, barragem",
    "AE": "Aeroporto, Aeródromo ou campo de pouso",
    "AT": "Linha de alta tensão",
    "BU": "Bueiro",
    "CE": "Cemitério",
    "CM": "Comércio (loja, armazem, hotel, posto de gasolina, etc.)",
    "CP": "Capela",
    "EE": "Estação Ecológica, Parque Nacional",
    "EF": "Estação de estrada de ferro",
    "EL": "Elevação, morro, chapada",
    "EM": "Estação meteorológica",
    "ES": "Escola, Grupo escolar, faculdade, Centros Sociais, etc",
    "ET": "Entroncamento, bifurcação",
    "FZ": "Sítio, Fazenda",
    "HO": "Hospital, maternidade, posto de saúde e de vacinação",
    "ID": "Indústria ( olaria, serraria, engenho, usina de leite)",
    "IG": "Igreja",
    "IM": "Igreja Matriz",
    "LF": "Linha férrea",
    "LG": "Lâmina D'água",
    "OU": "Outros",
    "PC": "Praça",
    "PF": "Prefeitura , Câmara Municipal",
    "PN": "Passagem de nível",
    "PO": "Porto",
    "PP": "Prédio Público ( DNER, Polícia Rodoviária, Posto fiscal)",
    "PT": "Ponte",
    "PU": "Perímetro urbano PU",
    "QT": "Quartel",
    "RC": "Rede de comunicação (telegrafia, telefonia,etc...)",
    "RI": "Reserva indígena",
    "RO": "Rodovias e estradas vicinais",
    "TU": "Túnel",
    "TV": "Trevo",
    "US": "Usina Hidrelétrica, Termoelétrica, nuclear, subestação de energia",
    "VT": "Viaduto",
}

# -------------------------
# Tipo de Fonte (códigos numéricos 2 dígitos)
# -------------------------
TIPO_FONTE_COORD_DICT = {
    "01": "Triangulação",
    "02": "Poligonação",
    "22": "GPS Geodésico",
    "23": "Doppler",
    "25": "GPS Topográfico",
    "26": "GPS Navegação",
    "27": "Imagem",
    "31": "Carta 1:25000",
    "32": "Carta 1:50000",
    "33": "Carta 1:100000",
    "34": "Carta 1:250000",
    "35": "Carta 1:500000",
    "36": "Carta 1:1000000",
    "37": "Carta não Especificada",
    "40": "Interpolação",
    "50": "Astronomia",
    "99": "Não Especificada",
}

# -------------------------
# Situação (códigos numéricos)
# -------------------------
SITUACAO_MARCO_DICT = {
    "10": "BOM",
    "20": "DESTRUÍDO",
    "21": "DESTRUÍDO (SEM CHAPA)",
    "22": "DESTRUÍDO (CHAPA DANIFICADA)",
    "30": "NÃO ENCONTRADO",
    "40": "NÃO VISITADO",
    "50": "NÃO CONSTRUÍDO",
}

# -------------------------
# Campanha (ATENÇÃO: manter case original — NÃO normalizar)
# -------------------------
TIPO_CAMPANHA_DICT = {
    "cons": "Construção",
    "medA": "Altimetria",
    "medG": "Gravimetria",
    "medP": "Planimetria",
    "vrf": "VRF",
}


# -------------------------
# UNIDADE DA FEDERAÇÃO
# -------------------------
TIPO_UF_DICT = {
    "AC": "Acre",
    "AL": "Alagoas",
    "AP": "Amapá",
    "AM": "Amazonas",
    "BA": "Bahia",
    "CE": "Ceará",
    "DF": "Distrito Federal",
    "ES": "Espírito Santo",
    "GO": "Goiás",
    "MA": "Maranhão",
    "MT": "Mato Grosso",
    "MS": "Mato Grosso do Sul",
    "MG": "Minas Gerais",
    "PA": "Pará",
    "PB": "Paraíba",
    "PR": "Paraná",
    "PE": "Pernambuco",
    "PI": "Piauí",
    "RJ": "Rio de Janeiro",
    "RN": "Rio Grande do Norte",
    "RS": "Rio Grande do Sul",
    "RO": "Rondônia",
    "RR": "Roraima",
    "SC": "Santa Catarina",
    "SE": "Sergipe",
    "SP": "São Paulo",
    "TO": "Tocantins",
}


# -------------------------
# Helpers para listas "COD - Descrição" (usados no frames.py)
# -------------------------
def _opcoes_from_dict(dicionario: dict[str, str]) -> list[tuple[str, str]]:
    """Retorna lista de tuplas [(COD, 'COD - Descrição'), ...]."""
    return [
        (codigo, f"{codigo} - {descricao}")
        for codigo, descricao in dicionario.items()
    ]


def opcoes_tipo_local():
    return _opcoes_from_dict(TIPO_LOCAL_DICT)

def opcoes_tipo_fonte():
    return _opcoes_from_dict(TIPO_FONTE_COORD_DICT)

def opcoes_situacao():
    return _opcoes_from_dict(SITUACAO_MARCO_DICT)

def opcoes_campanha():
    # Mantém o case das chaves (ex.: 'medA')
    return _opcoes_from_dict(TIPO_CAMPANHA_DICT)

def opcoes_uf():
    # Mantém o case das chaves (ex.: 'medA')
    return _opcoes_from_dict(TIPO_UF_DICT)


# -------------------------
# Validação leve (sem normalizar)
# -------------------------
def validar_dominios() -> None:
    def _assert_unique(keys, nome):
        if len(keys) != len(set(keys)):
            dup = [k for k in keys if keys.count(k) > 1]
            raise ValueError(f"Chaves duplicadas em {nome}: {sorted(set(dup))}")

    _assert_unique(list(TIPO_LOCAL_DICT.keys()), "TIPO_LOCAL_DICT")
    _assert_unique(list(TIPO_FONTE_COORD_DICT.keys()), "TIPO_FONTE_COORD_DICT")
    _assert_unique(list(SITUACAO_MARCO_DICT.keys()), "SITUACAO_MARCO_DICT")
    _assert_unique(list(TIPO_CAMPANHA_DICT.keys()), "campanha_dict")
    _assert_unique(list(TIPO_MONUMENTACAO_DICT.keys()), "TIPO_MONUMENTACAO_DICT")

    # Regras formais (sem alterar case das campanhas)
    for k in TIPO_LOCAL_DICT:
        assert isinstance(k, str) and len(k) == 2 and k.isupper(), f"Código inválido em tipo_local: {k}"
    for k in TIPO_FONTE_COORD_DICT:
        assert isinstance(k, str) and k.isdigit() and len(k) == 2, f"Código inválido em tipo_fonte: {k}"
    for k in SITUACAO_MARCO_DICT:
        assert isinstance(k, str) and k.isdigit(), f"Código inválido em situacao: {k}"
    for k in TIPO_CAMPANHA_DICT:
        assert isinstance(k, str) and k.strip(), "Código de campanha vazio"
    for k in TIPO_MONUMENTACAO_DICT:
        assert k in ("C", "P", "M"), f"Código inválido em tipo_monumentacao: {k}"

# Valida ao carregar o módulo
validar_dominios()
