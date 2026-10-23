# -*- coding: utf-8 -*-
"""
file: /sidgeo/imagem/imagem_bd_repository.py
@created: 29-09-2026 pjag
@updated: 29-09-2026 pjag
"""
import oracledb


class OracleRepository:

    def __init__(
        self,
        user,
        password,
        dsn
    ):

        self.conn = oracledb.connect(
            user=user,
            password=password,
            dsn=dsn
        )

    def bulk_insert(
        self,
        registros
    ):

        sql = """
        INSERT INTO bdg_valida.t_arquivo_carga_imagem
        (
            id_base,
            nm_arquivo_original,
            cd_estacao,
            tp_imagem,
            fl_origem_sadgeo,

            tx_hash,
            dt_hash,

            nr_tamanho_arquivo,

            nr_largura_imagem,
            nr_altura_imagem,

            tx_fabricante_dispositivo,
            tx_modelo_dispositivo,

            dt_captura_imagem_original,

            tx_iso_imagem,
            tx_abertura_imagem,
            tx_tempo_exposicao,

            nr_resolucao_horizontal,
            nr_resolucao_vertical,

            gps_latitude,
            gps_longitude,
            gps_altitude,

            tx_dpi,
            tx_distancia_focal,

            dt_criacao_arquivo,
            dt_modificacao_arquivo,

            tx_metadados_dump,
            tx_erros_dump
        )
        VALUES
        (
            :1,:2,:3,:4,:5,
            :6,:7,:8,:9,:10,
            :11,:12,:13,:14,:15,
            :16,:17,:18,:19,:20,
            :21,:22,:23,:24,:25,
            :26,:27
        )
        """

        cur = self.conn.cursor()

        """ cur.executemany(
            sql,
            registros,
            batcherrors=True
        )
       """ 
        for i, registro in enumerate(registros):
            try:
               cur.execute(sql, registro)
            except Exception as e:
                print(f"Erro no registro {i}")
                print(registro)
                raise

        self.conn.commit()

        cur.close()