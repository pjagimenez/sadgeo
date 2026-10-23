# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 15:48:08 2026

@author: paulo.gimenez
"""

from PIL import Image
import os
import traceback

ARQUIVO = r"X:\prod\BDG_imagens\foto\3677N.jpg"

print("=" * 70)
print("ANALISE DE IMAGEM PARA ASP/FPDF")
print("=" * 70)

try:

    tamanho_bytes = os.path.getsize(ARQUIVO)

    with Image.open(ARQUIVO) as img:

        largura, altura = img.size
        megapixels = (largura * altura) / 1_000_000

        memoria_rgb = largura * altura * 3
        memoria_mb = memoria_rgb / 1024 / 1024

        modo = img.mode

        progressivo = (
            img.info.get("progressive")
            or img.info.get("progression")
            or False
        )

        print(f"Arquivo...........: {ARQUIVO}")
        print(f"Formato...........: {img.format}")
        print(f"Tamanho arquivo...: {tamanho_bytes:,} bytes")
        print(f"Tamanho...........: {tamanho_bytes/1024:.1f} KB")
        print(f"Tamanho...........: {tamanho_bytes/1024/1024:.2f} MB")
        print(f"Largura...........: {largura}")
        print(f"Altura............: {altura}")
        print(f"Megapixels........: {megapixels:.2f}")
        print(f"Modo de cor.......: {modo}")
        print(f"JPEG progressivo..: {progressivo}")
        print(f"Memória estimada..: {memoria_mb:.2f} MB")

        print("\nVALIDAÇÕES")
        print("-" * 40)

        if megapixels > 20:
            print("⚠ RESOLUÇÃO MUITO ALTA (>20 MP)")
        else:
            print("✓ Resolução OK")

        if memoria_mb > 100:
            print("⚠ IMAGEM CONSOME MAIS DE 100 MB EM MEMÓRIA")
        else:
            print("✓ Consumo de memória OK")

        if modo == "CMYK":
            print("⚠ IMAGEM CMYK (algumas versões do FPDF dão problema)")
        else:
            print("✓ RGB ou compatível")

        if progressivo:
            print("⚠ JPEG PROGRESSIVO (bibliotecas antigas podem falhar)")
        else:
            print("✓ JPEG baseline")

        try:
            exif = img.getexif()
            print(f"EXIF..............: {len(exif)} tags")
        except:
            print("EXIF..............: não encontrado")

    # verifica corrupção
    with Image.open(ARQUIVO) as teste:
        teste.verify()

    print("\n✓ Arquivo não aparenta estar corrompido")

except Exception as e:

    print("\n❌ POSSÍVEL ARQUIVO CORROMPIDO")
    print(e)
    traceback.print_exc()

print("\n" + "=" * 70)
print("FIM DA ANÁLISE")
print("=" * 70)
