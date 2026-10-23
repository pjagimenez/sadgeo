# -*- coding: utf-8 -*-
"""
file: /sidgeo/imagem/imagem_bd_processador.py
@created: 29-09-2026 pjag
@updated: 29-09-2026 pjag
"""
import argparse

from imagem_bd_loader import ImagemLoader
from imagem_bd_repository import OracleRepository


def parse_conn(conn):

    credenciais, dsn = conn.split(
        "@",
        1
    )

    usuario, senha = credenciais.split(
        "/",
        1
    )

    return usuario, senha, dsn


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--arquivo",
        required=True
    )

    parser.add_argument(
        "--id-base",
        required=True,
        type=int
    )

    parser.add_argument(
        "--conn",
        required=True
    )

    args = parser.parse_args()

    usuario, senha, dsn = parse_conn(
        args.conn
    )

    loader = ImagemLoader()

    df = loader.carregar(
        args.arquivo
    )

    registros = loader.transformar(
        df,
        args.id_base
    )

    repo = OracleRepository(
        usuario,
        senha,
        dsn
    )

    repo.bulk_insert(
        registros
    )

    print(
        f"Registros carregados: {len(registros)}"
    )

    print(
        f"TX_METADADOS_DUMP truncados: "
        f"{loader.truncados_metadados}"
    )

    print(
        f"TX_ERROS_DUMP truncados: "
        f"{loader.truncados_erros}"
    )


if __name__ == "__main__":
    main()