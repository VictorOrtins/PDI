from PIL import Image
from math import *
import numpy as np
from time import time

# resultado: str = "S:/Programming/Python/2023/PDI/Resultado/"

# * Transformações

def same_image(image1, image2):
    
    matriz_1 = image1.load()
    matriz_2 = image2.load()

    altura1: int = image1.size[0]
    comprimento1: int = image1.size[1]

    altura2: int = image2.size[0]
    comprimento2: int = image2.size[1]

    if (altura1 != altura2 or comprimento1 != comprimento2):
        return False

    for i in range(altura1):
        for j in range(comprimento2):
            if not (matriz_1[i, j] == matriz_2[i, j]):
                return False

    return True

def rgb_to_yiq(imagem_rgb, matriz):

    altura: int = imagem_rgb.size[0]
    comprimento: int = imagem_rgb.size[1]

    matrizNova = np.zeros((altura, comprimento), tuple)

    for i in range(altura):
        for j in range(comprimento):
            pixel = matriz[i, j]

            Y: float = 0.299 * pixel[0] + 0.587 * pixel[1] + 0.114 * pixel[2]
            I: float = 0.596 * pixel[0] - 0.274 * pixel[1] - 0.322 * pixel[2]
            Q: float = 0.211 * pixel[0] - 0.523 * pixel[1] + 0.312 * pixel[2]

            matrizNova[i, j] = (Y, I, Q)

    return matrizNova.copy()

def yiq_to_rgb(imagem_rgb, matriz):

    altura = imagem_rgb.size[0]
    comprimento = imagem_rgb.size[1]
    matriz_rgb = imagem_rgb.load()


    for i in range(altura):
        for j in range(comprimento):
            pixel = matriz[i, j]

            R: int = round(pixel[0] + 0.956 * pixel[1] + 0.621 * pixel[2])
            G: int = round(pixel[0] - 0.272 * pixel[1] - 0.647 * pixel[2])
            B: int = round(pixel[0] - 1.106 * pixel[1] + 1.703 * pixel[2])

            matriz_rgb[i, j] = (R, G, B)

def mostrarPixel(image):

    matriz = image.load()

    for i in range(image.size[0]):
        for j in range(image.size[1]):
            pixel = matriz[i, j]
            print(f"{pixel}")


def negativoRGB(imagem_rgb, matriz):

    altura = imagem_rgb.size[0]
    comprimento = imagem_rgb.size[1]

    for i in range(altura):
        for j in range(comprimento):
            pixel = matriz[i, j]

            R: int = 255 - pixel[0]
            G: int = 255 - pixel[1]
            B: int = 255 - pixel[2]

            matriz[i, j] = (R, G, B)

def negativo_yiq(imagem_rgb, matriz):

    altura = imagem_rgb.size[0]
    comprimento = imagem_rgb.size[1]

    matrizYIQ = rgb_to_yiq(imagem_rgb, matriz)

    for i in range(altura):
        for j in range(comprimento):
            pixel = matrizYIQ[i, j]

            Y: float = 255 - pixel[0]

            matrizYIQ[i, j] = (Y, pixel[1], pixel[2])

    yiq_to_rgb(imagem_rgb, matrizYIQ)

def correlacao(imagem_rgb, matriz, mascara, m: int, n: int, pivoH: int, pivoV: int, offset: int):

    altura: int = imagem_rgb.size[0]
    comprimento: int = imagem_rgb.size[1]

    matrizResultante = np.zeros((altura, comprimento), tuple)

    lista: list = []
    for i in range(m):
        for j in range(n):
            lista.append((i - pivoH, j - pivoV))

    for i in range(altura):
        for j in range(comprimento):

            listaPosicoes: list = []
            for item in lista:

                valor1: int = i + item[0]
                valor2: int = j + item[1]

                tupla: tuple = (valor1, valor2)
                listaPosicoes.append(tupla)

            pixel: tuple = matriz[i, j]
            somaR: float = 0
            somaG: float = 0
            somaB: float = 0

            for posicao, item in enumerate(listaPosicoes):

                posX: int = posicao // m
                posY: int = posicao % n

                matrizX: int = item[0]
                matrizY: int = item[1]

                # * Extensão pela borda repetida
                if matrizX < 0:
                    matrizX = 0
                elif matrizX >= altura:
                    matrizX = altura - 1

                if matrizY < 0:
                    matrizY = 0
                elif matrizY >= comprimento:
                    matrizY = comprimento - 1

                somaR += matriz[matrizX, matrizY][0] * mascara[posX][posY]
                somaG += matriz[matrizX, matrizY][1] * mascara[posX][posY]
                somaB += matriz[matrizX, matrizY][2] * mascara[posX][posY]

            matrizResultante[i, j] = (trunc(somaR) + offset, trunc(somaG) + offset, trunc(somaB) + offset)

    for i in range(altura):
        for j in range(comprimento):
            matriz[i, j] = matrizResultante[i, j]


def mediana(image, matriz_rgb, mascara_m: int, mascara_n: int):

    if mascara_m % 2 == 0 or mascara_n % 2 == 0:
        return False

    altura: int = image.size[0]
    comprimento: int = image.size[1]

    matrizResultante = np.zeros((altura, comprimento), tuple)

    mascara: list = []
    # (-1, -1), (-1,0), (-1, + 1) 
    pivo: tuple = (mascara_m // 2, mascara_n // 2)

    for i in range(mascara_m):
        for j in range(mascara_n):
            mascara.append((i - pivo[0], j - pivo[1]))

    ###  i-1, j-1 | i-1, j | i - 1,j + 1
    ###  i, j - 1 | i, j | i, j + 1
    ###  i + 1, j - 1 | i + 1, j | i + 1, j + 1

    elemento_mediana: int = (mascara_m * mascara_n) // 2

    for i in range(altura):
        for j in range(comprimento):
            vizinhanca_R: list = []
            vizinhanca_G: list = []
            vizinhanca_B: list = []

            for item in mascara:
                pos_i = i + item[0]
                pos_j = j + item[1]

                if pos_i < 0:
                    pos_i = 0
                elif pos_i >= altura:
                    pos_i = altura - 1

                if pos_j < 0:
                    pos_j = 0
                elif pos_j >= comprimento:
                    pos_j = comprimento - 1

                pixel = matriz_rgb[pos_i, pos_j]

                vizinhanca_R.append(pixel[0])
                vizinhanca_G.append(pixel[1])
                vizinhanca_B.append(pixel[2])

            vizinhanca_R.sort()
            vizinhanca_G.sort()
            vizinhanca_B.sort()

            R = vizinhanca_R[elemento_mediana]
            G = vizinhanca_G[elemento_mediana]
            B = vizinhanca_B[elemento_mediana]

            matrizResultante[i, j] = (R, G, B)

    for i in range(altura):
        for j in range(comprimento):
            matriz_rgb[i, j] = matrizResultante[i, j]
