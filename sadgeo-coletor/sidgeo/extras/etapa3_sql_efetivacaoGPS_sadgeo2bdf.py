# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 10:38:09 2026

@author: paulo.gimenez
"""


from datetime import datetime

import oracledb
print(f"Oracle DB: {oracledb.__version__}")

import os
os.environ["TNS_ADMIN"] = r"C:\Ora12c_64bits\product\12.1.0\client\network\admin"

import platform
print(f"Plataforma: {platform.architecture()}")

class BdgCargaExecutor:
    def __init__(self, user, password, dsn):
        """
        Inicializa conexão com o Oracle
        """
        self.user = user
        self.password = password
        self.dsn = dsn
        self.connection = None
        
        # 📁 pasta do script
        self.base_dir = os.path.dirname(os.path.abspath(__file__))

        # 📄 arquivos
        self.sql_file = os.path.join(self.base_dir, "integra_sadgeo2bdg.sql")
        self.log_file = os.path.join(self.base_dir, "integra_sadgeo2bdg.log")


    def connect(self):
        """Abre conexão com o banco"""
        self.connection = oracledb.connect(
            user=self.user,
            password=self.password,
            dsn=self.dsn
        )

    def close(self):
        """Fecha conexão"""
        if self.connection:
            self.connection.close()

    def log_sql(self, texto):
        with open(self.sql_file, "a", encoding="utf-8") as f:
            f.write(texto + "\n")

    def obterTimestampHumanReadable(self):
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    
    def log_execucao(self, texto):
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(texto + "\n")

    def efetivar_carga(self, login, seq, estacao):
        """
        Executa a procedure P_EFETIVAR_CARGA_BDG
        """
        cursor = self.connection.cursor()

        # variável de saída
        v_retorno = cursor.var(str)

        print(f"Efetivando carga BDG da estação: {estacao}")

        
        # ✅ log mais seguro e realista
        sql_log = """
        BEGIN
            BDG_VALIDA.K_SADGEO_GPS_2023.P_EFETIVAR_CARGA_BDG(
                :login,
                :seq,
                :retorno
            );
        END;"""
        

        self.log_sql(f"-- {self.obterTimestampHumanReadable()}")
        self.log_sql(sql_log)
        self.log_sql(f"-- binds: login={login}, seq={seq}")


        try:
            cursor.callproc(
                "BDG_VALIDA.K_SADGEO_GPS_2023.P_EFETIVAR_CARGA_BDG",
                [login, seq, v_retorno]
            )
            self.connection.commit()

            retorno = v_retorno.getvalue()
            
            msg = f"[{self.obterTimestampHumanReadable()}] Sucesso | Estacao: {estacao} | Retorno: {retorno}"
            print(msg)
            self.log_execucao(msg)

            return retorno

        except oracledb.DatabaseError as e:
            error, = e.args
            
            msg = f"[{self.obterTimestampHumanReadable()}] ERRO | Estacao: {estacao} | {error.message}"
            print(msg)
            self.log_execucao(msg)

            return None

        finally:
            cursor.close()
            
#//-------



if __name__ == "__main__":
    v_userBD = input("Conta BD:")
    v_senhaBD = input("Senha BD:")
    #v_seq = input("Seq: ")
    #v_estacao = input("Estacao cod: ")

    executor = BdgCargaExecutor(
        user= v_userBD,
        password=v_senhaBD,
        dsn="oraprdent2.ibge.gov.br:1521/pent2"
    )

    executor.connect()
    
    
    v_seq = ["183661-26"]
    v_estacao= ["99951"]
        
    """182761-26	99950
    v_seq = [
    "182482-26",
    "182483-26",
    "182490-26",
    "182491-26",
    "182492-26",
    "182501-26",
    "182502-26",
    "182481-26",
    "182486-26",
    "182485-26",
    "182488-26",
    "182487-26",
    "182489-26",
    "182484-26",
    "182494-26",
    "182498-26",
    "182499-26",
    "182493-26",
    "182503-26",
    "182504-26",
    "182505-26",
    "182506-26",
    "182496-26",
    "182495-26",
    "182497-26",
    "182509-26",
    "182510-26",
    "182507-26",
    "182508-26",
    "182500-26",
    ]

    v_estacao = [
    92979,
    92980,
    92981,
    92982,
    92983,
    92984,
    92985,
    99909,
    99927,
    99928,
    99929,
    99930,
    99931,
    99932,
    99933,
    99934,
    99935,
    99936,
    99937,
    99938,
    99939,
    99940,
    99941,
    99942,
    99943,
    99944,
    99945,
    99946,
    99947,
    99948,
    ]
    """
    
    try:
        """
        cargas = [
            ("fernanda.torres", v_seq,v_estacao),
        ]

        for login, seq, estacao in cargas:
            executor.efetivar_carga(login, seq, estacao)
            """
        for seq, estacao in zip(v_seq, v_estacao):
            executor.efetivar_carga("fernanda.torres", seq, estacao)
            
    finally:
        executor.close()
           
