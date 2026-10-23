# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 14:29:11 2026

@author: paulo.gimenez
"""

import paramiko
import hashlib
import os
import getpass
import shutil
from datetime import datetime

# ========================================
# CONFIGURAÇÃO (ARRAYS)
# ========================================

DESTINOS = [
    {
        "tipo": "remoto",
        "host": "wiisint03v.ibge.gov.br",
        "base_dir": "/E:/BDG/bdg/pdf/images"
    },
    {
        "tipo": "remoto",
        "host": "wiisprd31v.ibge.gov.br",
        "base_dir": "/E:/SERVICOSCGED/pagina/images"
    },    
    {
        "tipo": "local",
        "host": "",
        "base_dir": "X:\prod\BDG_imagens"
    }
    ]



# ========================================
# FUNÇÕES
# ========================================

def copiar_local(arquivo_local, base_dir, hash_local):
    nome = os.path.basename(arquivo_local)
    tipo = determinar_tipo(nome)

    diretorio_destino = os.path.join(base_dir, tipo)
    os.makedirs(diretorio_destino, exist_ok=True)

    arquivo_destino = os.path.join(diretorio_destino, nome)

    versionar_arquivo_local_se_existir(arquivo_destino)

    shutil.copy2(arquivo_local, arquivo_destino)

    hash_destino = sha256_local(arquivo_destino)

    if hash_destino != hash_local:
        raise RuntimeError(
            f"Hash divergente no destino local\n"
            f"Local origem : {hash_local}\n"
            f"Local destino: {hash_destino}"
        )

    print(f"📂 Arquivo copiado para: LOCAL:{arquivo_destino}")
    print("        Hash iguais")
    print(f"                Local origem : {hash_local}")
    print(f"                Local destino: {hash_destino}")

    return arquivo_destino


def copiar_remoto(servidor, usuario, senha, arquivo_local, hash_local):
    host = servidor["host"]
    base_dir = servidor["base_dir"]

    nome = os.path.basename(arquivo_local)
    tipo = determinar_tipo(nome)

    arquivo_remoto = f"{base_dir.rstrip('/')}/{tipo}/{nome}"

    print(f"\n📡 Conectando ao servidor: {host}")

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=host, username=usuario, password=senha)

    print("✅ Conexão SSH estabelecida")

    sftp = ssh.open_sftp()
    
    try:
        for item in sftp.listdir('/'):
            print(item)
        sftp.stat(arquivo_remoto)
        print("EXISTE:", arquivo_remoto)
    except Exception as e:
        print("NAO EXISTE:", arquivo_remoto, e)
    
    sftp.put(arquivo_local, arquivo_remoto)
    print(f"📂 Arquivo copiado para: {host}:{arquivo_remoto}")

    hash_remoto = sha256_remoto_auto(ssh, sftp, arquivo_remoto)

    sftp.close()
    ssh.close()

    if hash_remoto != hash_local:
        raise RuntimeError(
            f"Hash divergente no servidor {host}\n"
            f"Local : {hash_local}\n"
            f"Remoto: {hash_remoto}"
        )

    print("        Hash iguais")
    print(f"                Local : {hash_local}")
    print(f"                Remoto: {hash_remoto}")

    return arquivo_remoto


def versionar_arquivo_local_se_existir(arquivo_destino):

    if not os.path.exists(arquivo_destino):
        return

    nome = os.path.basename(arquivo_destino)
    tipo = determinar_tipo(nome)

    # Usar a data da operação de backup
    #data_mod = datetime.fromtimestamp(
    #    os.path.getmtime(arquivo_destino)
    #)    
    #data_str = data_mod.strftime("%Y%m%d")
    data_str = datetime.now().strftime("%Y%m%d")

    nome_sem_ext, ext = os.path.splitext(nome)

    nome_backup = f"{nome_sem_ext}_BKP{data_str}{ext}"

    pasta_versionamento = os.path.join(
        r"X:\prod\BDG_imagens\versionamento",
        tipo
    )

    os.makedirs(pasta_versionamento, exist_ok=True)

    destino_backup = os.path.join(
        pasta_versionamento,
        nome_backup
    )

    # Reprocessamento: já existe backup dessa data
    if os.path.exists(destino_backup):
        os.remove(destino_backup)

    shutil.move(arquivo_destino, destino_backup)

    print(
        f"📦 Arquivo versionado:\n"
        f"    Origem : {arquivo_destino}\n"
        f"    Backup : {destino_backup}"
    )
    
    
def sha256_local(arquivo):
    h = hashlib.sha256()
    with open(arquivo, "rb") as f:
        for bloco in iter(lambda: f.read(4096), b""):
            h.update(bloco)
    return h.hexdigest().lower()


def sha256_remoto_via_sftp(sftp, arquivo_remoto):
    h = hashlib.sha256()
    with sftp.open(arquivo_remoto, "rb") as f:
        for bloco in iter(lambda: f.read(4096), b""):
            h.update(bloco)
    return h.hexdigest().lower()


def sha256_remoto_auto(ssh, sftp, arquivo_remoto):
    comandos = [
        f'sha256sum "{arquivo_remoto}"',
        f'certutil -hashfile "{arquivo_remoto}" SHA256'
    ]

    # 1️⃣ Tentativa via shell
    for cmd in comandos:
        stdin, stdout, stderr = ssh.exec_command(cmd)

        saida = stdout.read().decode().strip()
        erro = stderr.read().decode().strip()

        if not saida or "usage" in saida.lower():
            continue

        linhas = [l.strip() for l in saida.splitlines() if l.strip()]

        # Linux
        if len(linhas[0]) >= 64 and all(c in "0123456789abcdefABCDEF" for c in linhas[0][:64]):
            return linhas[0].split()[0].lower()

        # Windows (certutil)
        if len(linhas) > 1:
            hash_limpo = linhas[1].replace(" ", "").lower()
            if len(hash_limpo) == 64:
                return hash_limpo

    # 2️⃣ Fallback via SFTP (método universal)
    try:
        return sha256_remoto_via_sftp(sftp, arquivo_remoto)
    except Exception as e:
        raise RuntimeError(
            "Não foi possível calcular o SHA-256 remoto nem via shell nem via SFTP:\n"
            f"{arquivo_remoto}\n"
            f"Erro: {e}"
        )


def determinar_tipo(nome_arquivo):
    nome_sem_ext = os.path.splitext(nome_arquivo)[0]

    if nome_arquivo.startswith("I"):
        return "croqui"
    elif nome_sem_ext.endswith("c"):
        return "chapa"
    else:
        return "foto"


def copiar_remoto_conexao_aberta(ssh, sftp, servidor, arquivo_local, hash_local):
    host = servidor["host"]
    base_dir = servidor["base_dir"]

    nome = os.path.basename(arquivo_local)
    tipo = determinar_tipo(nome)

    dir_remoto = f"{base_dir.rstrip('/')}/{tipo}"
    arquivo_remoto = f"{dir_remoto}/{nome}"
 

    try:
        #for item in sftp.listdir('/'):
        #    print(item)
        sftp.stat(arquivo_remoto)
        print("EXISTE, será atualizado:", arquivo_remoto)
    except IOError:
        print("NÃO EXISTE:, será incluído:", arquivo_remoto)

    try:
        sftp.put(arquivo_local, arquivo_remoto)
        print(f"📂 Arquivo copiado para: {host}:{arquivo_remoto}")
    except Exception as e:
        print(f"* FALHA na copia para: {host}:{arquivo_remoto} \t\n {e}")
        return
    
    hash_remoto = sha256_remoto_auto(ssh, sftp, arquivo_remoto)
    
    if hash_remoto != hash_local:
        raise RuntimeError(
            f"\tHash divergente no servidor {host}\n"
            f"\t\tLocal : {hash_local}\n"
            f"\t\tRemoto: {hash_remoto}"
        )
    else:
        print(f"\tHash iguais \n"
        f"\t\tLocal : {hash_local}\n"
        f"\t\tRemoto: {hash_remoto}"
    )
        
    return arquivo_remoto

            
#//-------

if __name__ == "__main__":
        
    # ========================================
    # EXECUÇÃO
    # ========================================
    
    print("\n=== CÓPIA DE IMAGENS JPG PARA SERVIDORES ===")
    
    usuario = input("Usuário SSH: ")
    senha = getpass.getpass("Senha SSH: ")
    
    origem = input("Diretório de origem dos JPGs: ").strip()
    
    if not os.path.isdir(origem):
        raise RuntimeError("Diretório de origem não existe")
    
    
    arquivos = [
        os.path.join(origem, f)
        for f in os.listdir(origem)
        if f.lower().endswith(".jpg")
    ]
    
    if not arquivos:
        raise RuntimeError("Nenhum arquivo JPG encontrado no diretório")
    
    print(f"\n📸 {len(arquivos)} arquivo(s) JPG encontrado(s)\n")
    
    
    resultados_ok = []
    erros = []
    
    # Preparar os destinos
    destinos_ativos = []

    for destino in DESTINOS:
    
        print(f"\n▶ Preparando destino: {destino['host']}")
            
        if destino["tipo"] == "local":
            destinos_ativos.append(destino)
            continue
    
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(
                paramiko.AutoAddPolicy()
            )
    
            ssh.connect(
                hostname=destino["host"],
                username=usuario,
                password=senha
            )
    
            destino["ssh"] = ssh
            destino["sftp"] = ssh.open_sftp()
            

            destinos_ativos.append(destino)
    
        except Exception as e:
            erros.append(f"Falha ao conectar {destino['host']} -> {e}"            )
            
            
    # Processar as copias de arquivos
    for arquivo_local in arquivos:
        
        print(f"\n▶ Processando: {arquivo_local}")
        hash_local = sha256_local(arquivo_local)
        
        for destino in destinos_ativos:
        
            try:                
                if destino["tipo"] == "local":
                
                    caminho = copiar_local(
                        arquivo_local,
                        destino["base_dir"],
                        hash_local
                        )
                    resultados_ok.append(f"CENTRAL: {caminho}")
            
                elif destino["tipo"] == "remoto":
                        
                    caminho= copiar_remoto_conexao_aberta(
                            destino["ssh"],
                            destino["sftp"],
                            destino,
                            arquivo_local,
                            hash_local
                    )
                    resultados_ok.append(f"{destino['host']}:{caminho}")
                
            except Exception as e:
                erros.append(f"{arquivo_local} → {destino} → {e}")

    #Fechar conexoes remotas
    for destino in destinos_ativos:
        if destino["tipo"] != "remoto":
            continue
    
        try:
            destino["sftp"].close()
        except Exception:
            pass
    
        try:
            destino["ssh"].close()
        except Exception:
            pass
            
    
    # ========================================
    # RESULTADO FINAL
    # ========================================
    
    print("\n=== RESULTADO FINAL ===")
    
    for r in resultados_ok:
        print("✅", r)
    
    for e in erros:
        print("❌", e)
    
    if erros:
        print(f"\n⚠️ Concluído com {len(erros)} erro(s).")
    else:
        print("\n✅ Todos os arquivos foram copiados e validados com sucesso.")