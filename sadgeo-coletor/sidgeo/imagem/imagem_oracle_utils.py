# -*- coding: utf-8 -*-
"""
file: /sidgeo/imagem/imagem_oracle_utils.py
@created: 29-09-2026 pjag
@updated: 29-09-2026 pjag
"""
import logging

logger = logging.getLogger(__name__)


class CampoOracle:

    LIMITE_VARCHAR4000 = 4000

    @classmethod
    def varchar4000(
        cls,
        valor,
        nome_campo="CAMPO"
    ):

        if valor is None:
            return None

        valor = str(valor)

        if len(valor) > cls.LIMITE_VARCHAR4000:

            logger.warning(
                "%s truncado de %d para %d caracteres",
                nome_campo,
                len(valor),
                cls.LIMITE_VARCHAR4000
            )

            return valor[:cls.LIMITE_VARCHAR4000]

        return valor