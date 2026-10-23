# -*- coding: utf-8 -*-

from __future__ import annotations

import os
import re
import sys

from sidgeo.util.strings import detectar_encoding
from sidgeo.infra.sqlplus_runner import ExecutorSQLPlus

def contar_estacoes(conn_str: str) -> int:
    sql_file = "./count_estacoes.sql"

    with open(sql_file, "w", encoding="utf-8") as f:
        f.write("""
            SET PAGESIZE 0 FEEDBACK OFF VERIFY OFF HEADING OFF ECHO OFF
            SELECT COUNT(*) FROM bdG_valida.t_estacao;
            EXIT;
        """)

    executor = ExecutorSQLPlus(sql_file, conn_str)

    executor.executar()
    '''        
    result = subprocess.run(
        f"sqlplus -s {conn_str} @{sql_file}",
        shell=True,
        capture_output=True,
        text=True,
        encoding="utf-8"
    )

    # Extrai apenas o número da saída
    linhas = result.stdout.strip().splitlines()
    for linha in linhas:
        linha = linha.strip()
        if linha.isdigit():
            return int(linha)
    '''
    return -1   # retorno de erro caso não encontre número



# Solicita a string de conexão ao usuário
conn_str = input("\tDigite a string de conexão (usuario/senha@bd): ").strip()

qtd = contar_estacoes(conn_str)
print("Total de registros:", qtd)
