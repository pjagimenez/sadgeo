"""Redimensionamento proporcional e etiqueta aplicados a uma cópia da imagem."""
from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO
import re

from PIL import Image, ImageDraw, ImageFont, ImageOps

from sidgeo.domain.erros import ValidacaoErro
from sidgeo.domain.foto import LIMITE_FOTO


@dataclass(frozen=True)
class AjusteFoto:
    tipo_estacao: str = "SAT"
    codigo: str = ""
    horizontal: int = 370
    vertical: int = 280
    comprimento: int = 70
    altura: int = 15
    largura_maxima: int = 640
    altura_maxima: int = 480
    redimensionar: bool = True


def renderizar_foto(dados: bytes, ajuste: AjusteFoto) -> Image.Image:
    if not re.fullmatch(r"[A-Z0-9]{1,10}", ajuste.codigo):
        raise ValidacaoErro("Informe o código da estação para a etiqueta (até 10 letras/números).")
    if not re.fullmatch(r"[A-Z0-9-]{1,10}", ajuste.tipo_estacao):
        raise ValidacaoErro("Informe o tipo da estação para a etiqueta, por exemplo SAT ou RN.")
    if not (1 <= ajuste.largura_maxima <= 8192 and 1 <= ajuste.altura_maxima <= 8192):
        raise ValidacaoErro("As dimensões de saída devem ficar entre 1 e 8192 pixels.")
    with Image.open(BytesIO(dados)) as original:
        corrigida = ImageOps.exif_transpose(original).convert("RGBA")
        fundo = Image.new("RGBA", corrigida.size, "white")
        fundo.alpha_composite(corrigida)
        imagem = fundo.convert("RGB")
    if ajuste.redimensionar:
        imagem.thumbnail((ajuste.largura_maxima, ajuste.altura_maxima), Image.Resampling.LANCZOS)
    x, y, largura, altura = ajuste.horizontal, ajuste.vertical, ajuste.comprimento, ajuste.altura
    if (min(x, y) < 0 or largura < 8 or altura < 8
            or x + largura > imagem.width or y + altura > imagem.height):
        raise ValidacaoErro(f"A etiqueta deve caber na foto final ({imagem.width} × {imagem.height} pixels).")
    desenho = ImageDraw.Draw(imagem)
    texto = f"{ajuste.tipo_estacao} {ajuste.codigo}"
    tamanho = altura - 3
    while tamanho >= 4:
        fonte = ImageFont.load_default(size=tamanho)
        caixa = desenho.textbbox((0, 0), texto, font=fonte)
        if caixa[2] - caixa[0] <= largura - 4 and caixa[3] - caixa[1] <= altura - 2:
            break
        tamanho -= 1
    else:
        raise ValidacaoErro("Aumente o comprimento/altura da etiqueta para acomodar o texto.")
    desenho.rectangle((x, y, x + largura - 1, y + altura - 1), fill="white", outline="#555555")
    desenho.text((x + (largura - (caixa[2] - caixa[0])) / 2 - caixa[0],
                  y + (altura - (caixa[3] - caixa[1])) / 2 - caixa[1]), texto, font=fonte, fill="black")
    return imagem


def jpeg_tratado(dados: bytes, ajuste: AjusteFoto) -> bytes:
    imagem = renderizar_foto(dados, ajuste)
    saida = BytesIO()
    imagem.save(saida, format="JPEG", quality=90, optimize=True)
    resultado = saida.getvalue()
    if len(resultado) > LIMITE_FOTO:
        raise ValidacaoErro("A foto tratada excedeu 5 MB; reduza as dimensões de saída.")
    return resultado
