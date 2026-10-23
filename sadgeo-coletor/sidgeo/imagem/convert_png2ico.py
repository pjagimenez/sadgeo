# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 16:53:35 2026

@author: paulo.gimenez
"""
from PIL import Image

img = Image.open(
    r"D:\IBGE\Projetos\gitProjetos\tmp_dynadjustweb_fromGitHub\assets\dynadjustbr.png"
)

img.save(
    r"D:\IBGE\Projetos\gitProjetos\tmp_dynadjustweb_fromGitHub\assets\dynadjustbr.ico",
    format="ICO",
    sizes=[
        (16, 16),
        (32, 32),
        (48, 48),
        (64, 64),
        (128, 128),
        (256, 256)
    ]
)
