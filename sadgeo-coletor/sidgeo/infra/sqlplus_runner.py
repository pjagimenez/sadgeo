# -*- coding: utf-8 -*-
"""
file: /sidgeo/infra/sqlplus_runner.py
@created: 09-09-2025 pjag
@updated: 03-07-2026 pjag Refatoração MVC, GRASP, PEP8 pythonic
"""

from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path


class SQLPlusErro(Exception):
    """Erro na execução do SQL*Plus."""


class ExecutorSQLPlus:
    """Executor de scripts SQL via SQL*Plus."""

    def __init__(self, arquivo_sql: str | Path, conn_str: str) -> None:
        self.arquivo_sql = Path(arquivo_sql)
        self.conn_str = conn_str

    @staticmethod
    def detectar_erro_log_sqlplus(
        stdout: str,
        stderr: str,
    ) -> tuple[bool, str]:
        mensagens: list[str] = []

        erros_ora = re.findall(r"ORA-\d{5}.*", stdout)
        if erros_ora:
            mensagens.append("Erro detectado no SQL*Plus:")
            mensagens.extend(erros_ora)

        if stderr:
            mensagens.append("Conteúdo do stderr:")
            mensagens.append(stderr.strip())

        return bool(mensagens), "\n".join(mensagens)

    def executar(self) -> Path:
        """Executa o script SQL e grava arquivo .log ao lado do .sql."""
        env = os.environ.copy()
        env["NLS_LANG"] = "AMERICAN_AMERICA.AL32UTF8"

        comando = [
            "sqlplus",
            "-s",
            self.conn_str,
            f"@{self.arquivo_sql}",
        ]

        try:
            resultado = subprocess.run(
                comando,
                capture_output=True,
                text=True,
                check=False,
                encoding="utf-8",
                env=env,
            )
        except OSError as erro:
            raise SQLPlusErro(
                f"Falha ao iniciar SQL*Plus: {erro}"
            ) from erro

        log_path = self.arquivo_sql.with_suffix(".log")
        log_path.write_text(
            "Saída do SQL*Plus:\n\n"
            f"LOG:\n{resultado.stdout}\n"
            f"ERR:\n{resultado.stderr}\n",
            encoding="utf-8",
        )

        houve_erro, mensagem_erro = self.detectar_erro_log_sqlplus(
            resultado.stdout,
            resultado.stderr,
        )

        if resultado.returncode != 0 or houve_erro:
            raise SQLPlusErro(
                f"Erro ao executar SQL*Plus.\n"
                f"Log: {log_path}\n"
                f"{mensagem_erro}"
            )

        return log_path