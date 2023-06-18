from funcoes import *
from PIL import ImageFilter

import os

caminho_atual = os.getcwd()
print(caminho_atual)

fonte: str = "C:/Users/Victor/Documents/P4/PDI/Projeto 1/PDI/Fontes"
resultado: str = "C:/Users/Victor/Documents/P4/PDI/Projeto 1/PDI/Fontes"

nomeImagem1: str = "velha.png"
nomeImagem2: str = "DancingInWater.jpg"
nomeImagem3: str = "testpat.1k.color2_1-menor.tiff"
nomeImagem4: str = "einstein.png"
nomeImagem5: str = "maca.png"
# nomeImagem2: str = "DancingInWater-menor.jpg"

imagemUsada: str = nomeImagem2

# | Imagem 0 - NORMAL
imagemNormal(fonte +  imagemUsada)

# | Imagem 1 - RGB -> YIQ -> RGB
rgb_yqi_rgb(fonte + imagemUsada)

# | Imagem 2 - NEGATIVO
imagemNegativaRGB(fonte + imagemUsada)

# | Imagem 3 - NEGATIVO em Y
imagemNegativaY(fonte + imagemUsada)

# | Imagem 4 - CORRELAÇÃO
aplicarCorrelacao(fonte + imagemUsada, "arquivo.txt", mostrarResultante=True)

# | Imagem 5 - MEDIANA
aplicarMediana(fonte + imagemUsada, 11, 11)
