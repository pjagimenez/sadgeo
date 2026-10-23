# -*- coding: utf-8 -*-
"""
file: /sidgeo/imagem/imagem_resource_connector.py
@created: 26-02-2025 pjag
@updated: 12-09-2025 pjag
"""

import stat
import os
import tempfile
from pathlib import Path
from abc import ABC, abstractmethod
from typing import Generator, Tuple
from  getpass import getpass
import paramiko

import logging
log = logging.getLogger(__name__)


# -----------------------------------------------------------------------------
# Conector SFTP ou LOCAL
# -----------------------------------------------------------------------------
class DataConnector(ABC):    
    """
    Interface base abstrata para conectores de origem de dados (ex: LOCAL, SFTP).
    Garante que subclasses implementem os métodos obrigatórios.
    """
    
    @abstractmethod
    def list_files(self, subfolder_name: str,
                   exts: Tuple[str, ...] = ('.jpg', '.jpeg', '.png', '.tif', '.tiff')) -> Generator[str, None, None]:
        """
        Lista os arquivos da origem de dados com as extensões fornecidas.
        Deve retornar um gerador de caminhos de arquivo.
        """
        pass        

    @abstractmethod
    def download_to_temp(self, remote_path: str) -> str:
        """
        Retorna o caminho local do arquivo.
        Em conectores remotos, deve baixar para um arquivo temporário.
        Em conectores locais, pode retornar o próprio caminho.
        """
        pass

    def close(self):
        """ Fechamento de recursos (se necessário). """
        pass

    # Permite uso com "with"    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()



class LocalConnector(DataConnector):
    def __init__(self, base_path: str):
        self.base = Path(base_path).resolve()

    def list_files(self, subfolder_name: str,
                   exts: Tuple[str, ...] = ('.jpg', '.jpeg', '.png', '.tif', '.tiff')) -> Generator[str, None, None]:
        """
        Percorre recursivamente a subpasta local a partir de base e
        retorna somente arquivos de imagem pelas extensões informadas.
        """
        base = Path(self.base) / subfolder_name
        if not base.exists():
            return iter(())
        
        # rglob para percorrer recursivo; evita arquivos ocultos do SO por padrão
        for p in base.rglob('*'):
            if p.is_file() and p.suffix.lower() in exts:
                yield str(p.resolve())

    # Local não precisa baixar — mas mantemos a assinatura
    def download_to_temp(self, local_path: str) -> str:
        return local_path


class SFTPConnector(DataConnector):
    """
    Conector SFTP resiliente, com:
      - Ciphers modernas (evita Deprecation de Blowfish quando possível)
      - Walk recursivo com checagem correta de diretórios (stat.S_ISDIR)
      - Filtro por extensão antes de baixar
      - Download para arquivo temporário preservando a extensão
    """
    def __init__(self, host: str, user: str, pwd: str, remote_base: str,
                 port: int = 22, timeout: int = 30):
        self.base = remote_base.rstrip('/')
        self._transport = paramiko.Transport((host, port))
        # Ajuste de cifras mais modernas (servidores antigos podem ignorar)
        try:
            sec = self._transport.get_security_options()
            sec.ciphers = ('aes128-ctr', 'aes192-ctr', 'aes256-ctr', 'chacha20-poly1305@openssh.com')
        except Exception:
            # Se não conseguir ajustar, segue o padrão do servidor
            pass
        # Conecta
        self._transport.connect(username=user, password=pwd)
        self.sftp = paramiko.SFTPClient.from_transport(self._transport)
        self.sftp.get_channel().settimeout(timeout)

    def _is_dir(self, path: str) -> bool:
        try:
            st = self.sftp.stat(path)
            return stat.S_ISDIR(st.st_mode)
        except IOError:
            return False

    def _walk(self, root: str) -> Generator[str, None, None]:
        """
        Walk recursivo no SFTP. Gera caminhos completos de arquivos.
        """
        try:
            for entry in self.sftp.listdir_attr(root):
                full = f"{root.rstrip('/')}/{entry.filename}"
                if stat.S_ISDIR(entry.st_mode):
                    # pular links simbólicos de diretório pode evitar loops
                    yield from self._walk(full)
                else:
                    yield full
        except IOError:
            # Permissão negada ou inexistente: ignora a pasta
            return

    def list_files(self, subfolder_name: str,
                   exts: Tuple[str, ...] = ('.jpg', '.jpeg', '.png', '.tif', '.tiff')) -> Generator[str, None, None]:
        """
        Lista **remotamente** apenas os arquivos com extensões desejadas,
        sem baixar ainda.
        """
        root = f"{self.base}/{subfolder_name}".rstrip('/')
        if not self._is_dir(root):
            return iter(())
        
        for remote_file in self._walk(root):
            # filtro por extensão (case-insensitive)
            if Path(remote_file).suffix.lower() in exts:
                yield remote_file

    def download_to_temp(self, remote_path: str) -> str:
        """
        Baixa arquivo remoto para um arquivo temporário preservando a extensão
        (útil para bibliotecas que inspecionam por sufixo).
        """
        suffix = Path(remote_path).suffix  # ex.: ".jpg"
        nome_arquivo = Path(remote_path).name  # ex: "1131Cc.jpg"
        
        # Diretório temporário padrão do sistema (ex.: /tmp no Linux, C:\Users\<user>\AppData\Local\Temp no Windows)
        tmp_dir = tempfile.gettempdir()
        tmp_path = os.path.join(tmp_dir, nome_arquivo)


        log.debug(f"Arquivo {remote_path} baixado para {tmp_path}")
        
        self.sftp.get(remote_path, tmp_path)
        return tmp_path

    def close(self):
        try:
            if self.sftp is not None:
                self.sftp.close()
        finally:
            try:
                if self._transport is not None:
                    self._transport.close()
            except Exception:
                pass

    def __del__(self):
        self.close()
        


def create_connector(modo: str, **kwargs) -> DataConnector:
    if modo == "1":
        return LocalConnector(kwargs["base_path"])
    elif modo == "2":
        return SFTPConnector(kwargs["host"], kwargs["user"], kwargs["pwd"], kwargs["remote_base"])



# -----------------------------------------------------------------------------
# Ponto de entrada
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    
    # Subpastas padrão do sistema
    subpastas = ["croqui", "foto", "chapa"]
    
    print("Selecione o modo de operação:")
    print("1 - Local")
    print("2 - SFTP")
    modo = input("Digite 1 ou 2: ").strip()

    # Escolha da subpasta
    print("\nSelecione a subpasta:")
    for i, nome in enumerate(subpastas, start=1):
        print(f"{i} - {nome}")
    opcao_subpasta = input("Digite o número da subpasta: ").strip()

    try:
        subpasta = subpastas[int(opcao_subpasta) - 1]
    except (ValueError, IndexError):
        print("Opção de subpasta inválida.")
        exit(1)

    
    if modo == "1":
        # -------------------- LOCAL MODE --------------------
        base_path = input("caminho base local: ").strip() or r"X:\prod\BDG_imagens"  # caminho base local (use r-string no Windows)

        with LocalConnector(base_path) as connector:
            print(f"\nListando imagens locais em {Path(base_path) / subpasta}...\n")
            arquivos = list(connector.list_files(subpasta))
            
            if not arquivos:
                print("Nenhum arquivo encontrado.")
            else:
                for arquivo in arquivos:
                    print("Arquivo encontrado:", arquivo)

                # Exemplo de uso de download_to_temp()
                caminho_exemplo = arquivos[0]
                caminho_local = connector.download_to_temp(caminho_exemplo)
                print("\nArquivo disponível localmente em:", caminho_local)

    elif modo == "2":
        # -------------------- SFTP MODE --------------------
        host = input("Host SFTP: ").strip() or "wiisint03v.ibge.gov.br"
        user = input("Usuário: ").strip() or "usrbdg"
        pwd = getpass("Senha: ") or "Gsd#2025"
        remote_base = input("Caminho remoto base (onde as subpastas tem as imagens): ").strip() or "E:/BDG/bdg/pdf/images"
        
        with SFTPConnector(host, user, pwd, remote_base) as connector:
            print(f"\nListando imagens remotas em {remote_base}/{subpasta}...\n")

            arquivos = list(connector.list_files(subpasta))
            if not arquivos:
                print("Nenhum arquivo encontrado no SFTP.")
            else:
                for arquivo in arquivos:
                    print("Arquivo remoto encontrado:", arquivo)

                # Exemplo de download
                caminho_exemplo = arquivos[0]
                caminho_temp = connector.download_to_temp(caminho_exemplo)
                print("\nArquivo baixado temporariamente em:", caminho_temp)

    else:
        print("Opção inválida! Digite 1 para Local ou 2 para SFTP.")