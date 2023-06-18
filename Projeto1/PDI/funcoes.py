from PIL import Image
from math import *
import numpy as np
from time import time
from time import sleep

fonte: str = "S:/Programming/Python/2023/PDI/Fontes/"
resultado: str = "S:/Programming/Python/2023/PDI/Resultado/"

# * Transformações
def same_image(image1, image2):

	matriz_1 = image1.load()
	matriz_2 = image2.load()

	altura1: int = image1.size[0]
	comprimento1: int = image1.size[1]
	altura2: int = image2.size[0]
	comprimento2: int = image2.size[1]

	if (altura1 != altura2 or comprimento1 != comprimento2):
		print("Tamanhos diferentes")
		return False

	for i in range(altura1):
		for j in range(comprimento2):
			if not (matriz_1[i, j] == matriz_2[i, j]):
				print("\n", matriz_1[i, j], matriz_2[i, j], i, j)
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


def yiq_to_rgb(imagem_rgb, matriz_yiq):

	altura = imagem_rgb.size[0]
	comprimento = imagem_rgb.size[1]
	matriz_rgb = imagem_rgb.load()

	for i in range(altura):
		for j in range(comprimento):
			pixel = matriz_yiq[i, j]

			R: int = round(pixel[0] + 0.956 * pixel[1] + 0.621 * pixel[2])
			G: int = round(pixel[0] - 0.272 * pixel[1] - 0.647 * pixel[2])
			B: int = round(pixel[0] - 1.106 * pixel[1] + 1.703 * pixel[2])

			matriz_rgb[i, j] = (R, G, B)


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

			Y: int = 255 - pixel[0]

			matrizYIQ[i, j] = (Y, pixel[1], pixel[2])

	yiq_to_rgb(imagem_rgb, matrizYIQ)


def correlacao(imagem_rgb, matriz, mascara, mascara_m: int, mascara_n: int, pivoH: int, pivoV: int, offset: int):

	altura: int = imagem_rgb.size[0]
	comprimento: int = imagem_rgb.size[1]

	dtype = [('valor1', int), ('valor2', int), ('valor3', int)]
	matrizResultante = np.zeros((altura, comprimento), dtype=dtype)

	lista = np.zeros((mascara_m, mascara_n), tuple)
	for i in range(mascara_m):
		for j in range(mascara_n):
			lista[i, j] = (i - pivoV, j - pivoH)

	for i in range(altura):
		for j in range(comprimento):

			somaR: float = 0
			somaG: float = 0
			somaB: float = 0

			for x in range(mascara_m):
				for y in range(mascara_n):

					item: tuple = lista[x, y]

					matrizX: int = i + item[0]
					matrizY: int = j + item[1]

					# * Extensão pela borda repetida
					if matrizX < 0:
						matrizX = 0
					elif matrizX >= altura:
						matrizX = altura - 1

					if matrizY < 0:
						matrizY = 0
					elif matrizY >= comprimento:
						matrizY = comprimento - 1

					somaR += matriz[matrizX, matrizY][0] * mascara[x, y]
					somaG += matriz[matrizX, matrizY][1] * mascara[x, y]
					somaB += matriz[matrizX, matrizY][2] * mascara[x, y]

			matrizResultante[i, j] = (
				somaR + offset, somaG + offset, somaB + offset)

	return matrizResultante.copy()


def mediana(image, matriz_rgb, mascara_m: int, mascara_n: int):

	if mascara_m % 2 == 0 or mascara_n % 2 == 0:
		return False

	altura: int = image.size[0]
	comprimento: int = image.size[1]

	matrizResultante = np.zeros((altura, comprimento), tuple)
	# dtype = [('valor1', int), ('valor2', int), ('valor3', int)]
	# matrizResultante = np.zeros((altura, comprimento), dtype=dtype)

	mascara: list = []
	pivo: tuple = (mascara_m // 2, mascara_n // 2)

	for i in range(mascara_m):
		for j in range(mascara_n):
			mascara.append((i - pivo[0], j - pivo[1]))

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


def trabalharArquivo(nomeArquivo):

	offset: int
	mascara_m: int
	mascara_n: int
	mascaraStr: list = []
	ehSobbel: bool = False
	ehEmboss: bool = False
	temFiltro: bool = False
	filtro: str
	mascara: np.ndarray

	with open(nomeArquivo, "r") as arquivo:

		contador: int = 0
		for linha in arquivo:
			match contador:
				case 0:
					offset = int(linha[linha.find(":") + 1:len(linha) - 1])
				case 1:
					if len(linha) > 8:
						filtro = linha[7: linha.find("\n")]
						temFiltro = True
				case 2:
					mascara_m = int(linha[linha.find(":") + 1:len(linha) - 1])
				case 3:
					mascara_n = int(linha[linha.find(":") + 1:len(linha) - 1])
				case 4:
					mascaraStr = linha[linha.find(":") + 1:].split(" ")
			contador += 1

	if temFiltro:
		match filtro:
			case "soma":
				mascara = np.zeros((mascara_m, mascara_n), float)
				mascara.fill(1)
			case "box":
				mascara = np.zeros((mascara_m, mascara_n), float)
				mascara.fill(1/(mascara_m * mascara_n))
			case "emboss":
				ehEmboss = True
				mascara = np.zeros((1, 1), float)
			case "sobel":
				ehSobbel = True
				mascara = np.zeros((1, 1), float)
			case _:
				print("Filtro inválido!")
				exit(0)

	else:
		mascara = np.zeros((mascara_m, mascara_n), float)

		for i in range(mascara_m):
			for j in range(mascara_n):

				posicao: int = j + i * mascara_n
				if mascara_m == 1:
					posicao = j
				if mascara_n == 1:
					posicao = i

				item: str = mascaraStr[posicao]

				if "/" in item:
					valor: float = float(
						item[0: item.find("/")]) / float(item[item.find("/") + 1:])
					mascara[i, j] = valor
				else:
					mascara[i, j] = float(item)

	return offset, mascara_m, mascara_n, mascara, ehSobbel, ehEmboss


def tonsDeCinza(imagem_rgb):
	altura, comprimento = imagem_rgb.size

	dtype = [('valor1', int), ('valor2', int), ('valor3', int)]
	matrizResultante = np.zeros((altura, comprimento), dtype=dtype)
	
	matrizRGB = imagem_rgb.load()

	for i in range(altura):
		for j in range(comprimento):
			pixel = matrizRGB[i,j]

			R = pixel[0]
			G = R
			B = R

			matrizResultante[i, j] = (R,G,B)

	return matrizResultante.copy()


def expansaoDeHistograma(imagem_rgb, matriz_rgb):

	altura, comprimento = imagem_rgb.size
 
	dtype = [('valor1', int), ('valor2', int), ('valor3', int)]
	matrizResultante = np.zeros((altura, comprimento), dtype=dtype)

	mapeamentoR: list = [0]*256
	mapeamentoG: list = [0]*256
	mapeamentoB: list = [0]*256
	
	minR: int = matriz_rgb[0,0][0]
	minG: int = matriz_rgb[0,0][1]
	minB: int = matriz_rgb[0,0][2]
	maxR: int = matriz_rgb[0,0][0]
	maxG: int = matriz_rgb[0,0][1]
	maxB: int = matriz_rgb[0,0][2]

	for i in range(1, altura):
		for j in range(1, comprimento):
			pixel = matriz_rgb[i, j]

			R = pixel[0]
			G = pixel[1]
			B = pixel[2]

			if R < minR:
				minR = R
			elif R > maxR:
				maxR = R

			if G < minG:
				minG = G
			elif G > maxG:
				maxG = G

			if B < minB:
				minB = B
			elif B > maxB:
				maxB = B

	for i in range(256):
		mapeamentoR[i] = round( ( (i - minR)/(maxR - minR) ) * 255)
		mapeamentoG[i] = round( ( (i - minG)/(maxG - minG) ) * 255)
		mapeamentoB[i] = round( ( (i - minB)/(maxB - minB) ) * 255)

	for i in range(altura):
		for j in range(comprimento):
			pixel = matriz_rgb[i , j]

			R = mapeamentoR[pixel[0]]
			G = mapeamentoG[pixel[1]]
			B = mapeamentoB[pixel[2]]

			matrizResultante[i,j] = (R,G,B)
	
	return matrizResultante.copy()


def sobel(imagem_rgb, matriz, offset: int):

	altura: int = imagem_rgb.size[0]
	comprimento: int = imagem_rgb.size[1]

	mascara_horizontal = np.zeros((3, 3), int)
	mascara_horizontal = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])

	mascara_vertical = np.zeros((3, 3), int)
	mascara_vertical = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])

	matrizCinza_Expansao = np.zeros((altura, comprimento), tuple)
	matrizHorizontal = np.zeros((altura, comprimento), tuple)
	matrizVertical = np.zeros((altura, comprimento), tuple)
	matrizResultante = np.zeros((altura, comprimento), tuple)
 
	# * Registo do tempo do início da execução
	tempoInicio: float = time()

	# matrizCinza_Expansao = tonsDeCinza(imagem_rgb)
	matrizCinza_Expansao = expansaoDeHistograma(imagem_rgb, imagem_rgb.load())

	matrizHorizontal = correlacao(imagem_rgb, matrizCinza_Expansao, mascara_horizontal, 3, 3, 1, 1, offset)

	# * Registo do tempo do final da execução
	tempoFim: float = time()
	print(f"4.1 - Sobel Horizontal: {tempoFim - tempoInicio :.6}s")

	# * Registo do tempo do início da execução
	tempoInicio: float = time()

	matrizVertical = correlacao(imagem_rgb, matrizCinza_Expansao, mascara_vertical, 3, 3, 1, 1, offset)

	for i in range(altura):
		for j in range(comprimento):
			R = abs(matrizHorizontal[i,j][0]) + abs(matrizVertical[i, j][0])
			B = abs(matrizHorizontal[i,j][1]) + abs(matrizVertical[i, j][1])
			G = abs(matrizHorizontal[i,j][2]) + abs(matrizVertical[i, j][2])

			matrizResultante[i, j] = (R,G,B)

	# * Registo do tempo do final da execução
	tempoFim: float = time()
	print(f"4.2 - Sobel Vertical: {tempoFim - tempoInicio :.6}s")

	return matrizResultante.copy()

def emboss(imagem_rgb, matriz, offset: int):
	mascara = np.array([[-1, 0], [0, 1]])
	altura, comprimento = imagem_rgb.size

	matrizResultante = np.zeros( (altura, comprimento), tuple)
	matrizResultante = correlacao(imagem_rgb, imagem_rgb.load(), mascara, 2, 2, 0, 0, offset)

	for i in range(altura):
		for j in range(comprimento):
			R = abs(matrizResultante[i,j][0]) + offset
			G = abs(matrizResultante[i,j][1]) + offset
			B = abs(matrizResultante[i,j][2]) + offset

			matrizResultante[i,j] = (R,G,B)

	return matrizResultante.copy()

# * Aplicações
def imagemNormal(nomeImagem: str, mostrarResultante=False):

	# * Registro do tempo do início da execução
	tempoInicio: float = time()

	# * Carregando e buscando informações da imagem
	imagem = Image.open(nomeImagem)

	# * Salvando e mostrando o resultado, e fechando a imagem
	imagem.save(resultado + "0_normal.png")
	if mostrarResultante:
		imagem.show()
	imagem.close()

	# * Registo do tempo do final da execução
	tempoFim: float = time()
	print(f"0 - {tempoFim - tempoInicio :2.6}s : Normal")


def rgb_yqi_rgb(nomeImagem: str, mostrarResultante=False):

	# * Carregando e buscando informações da imagem
	imagem = Image.open(nomeImagem)
	matrizImagem = imagem.load()

	# * Registo do tempo do início da execução
	tempoInicio: float = time()

	# * RGB -> YIQ e YIQ -> RGB
	matrizResultante = rgb_to_yiq(imagem, matrizImagem)
	yiq_to_rgb(imagem, matrizResultante)

	# * Registo do tempo do final da execução
	tempoFim: float = time()
	print(f"1 - {tempoFim - tempoInicio :2.6}s : RGB => YIQ => RGB")

	# * Salvando e mostrando o resultado, e fechando a imagem
	imagem.save(resultado + "1_rgb_yiq_rgb.png")
	if mostrarResultante:
		imagem.show()
	imagem.close()


def imagemNegativaRGB(nomeImagem: str, mostrarResultante=False):

	# * Carregando e buscando informações da imagem
	imagem = Image.open(nomeImagem)
	matrizImagem = imagem.load()

	# * Registo do tempo do início da execução
	tempoInicio: float = time()

	# * Negativo
	negativoRGB(imagem, matrizImagem)

	# * Registo do tempo do final da execução
	tempoFim: float = time()
	print(f"2 - {tempoFim - tempoInicio :2.6}s : Negativo em RGB")

	# * Salvando e mostrando o resultado, e fechando a imagem
	imagem.save(resultado + "2_negativo.png")
	if mostrarResultante:
		imagem.show()
	imagem.close()


def imagemNegativaY(nomeImagem: str, mostrarResultante=False):

	# * Carregando e buscando informações da imagem
	imagem = Image.open(nomeImagem)
	matrizImagem = imagem.load()

	# * Registo do tempo do início da execução
	tempoInicio: float = time()

	# * Negativo
	negativo_yiq(imagem, matrizImagem)

	# * Registo do tempo do final da execução
	tempoFim: float = time()
	print(f"3 - {tempoFim - tempoInicio :2.6}s : Negativo em Y")

	# * Salvando e mostrando o resultado, e fechando a imagem
	imagem.save(resultado + "3_negativo_Y.png")
	if mostrarResultante:
		imagem.show()
	imagem.close()


def aplicarCorrelacao(nomeImagem: str, nomeArquivo, nomeImagemSalva: str = '4_correlacao.png', mostrarResultante=False):

	# * Recuperando as informações do arquivo
	offset: int
	mascara_m: int
	mascara_n: int

	mascara: np.ndarray
	ehSobel: bool

	offset, mascara_m, mascara_n, mascara, ehSobel, ehEmboss = trabalharArquivo(
		nomeArquivo)

	# * Determinação da posição do pivô
	pivoV: int = mascara_m // 2
	pivoH: int = mascara_n // 2

	# * Carregando e buscando informações da imagem
	imagem = Image.open(nomeImagem)

	dtype = [('valor1', int), ('valor2', int), ('valor3', int)]
	matrizResultante = np.zeros((imagem.size[0], imagem.size[1]), dtype=dtype)

	# * Registo do tempo do início da execução
	tempoInicio: float = time()

	if ehSobel:
		matrizResultante = correlacao(imagem, imagem.load(
		), mascara, mascara_m, mascara_n, pivoH, pivoV, offset)
	elif ehEmboss:
		matrizResultante = emboss(imagem, imagem.load(), offset)
	else:
		matrizResultante = sobel(imagem, imagem.load(), offset)
		

	matriz = imagem.load()
	for i in range(imagem.size[0]):
		for j in range(imagem.size[1]):
			matriz[i, j] = (matrizResultante[i, j][0],
							matrizResultante[i, j][1], matrizResultante[i, j][2])

	# * Registo do tempo do final da execução
	tempoFim: float = time()
	print(f"4 - {tempoFim - tempoInicio :2.6}s : Correlação")

	# * Salvando e mostrando o resultado, e fechando a imagem
	imagem.save(resultado + nomeImagemSalva)
	if mostrarResultante:
		imagem.show()
	imagem.close()


def aplicarMediana(nomeImagem: str, m: int, n: int, mostrarResultante=False):

	# * Carregando e buscando informações da imagem
	imagem = Image.open(nomeImagem)

	# * Registo do tempo do início da execução
	tempoInicio: float = time()

	# * Mediana de (m x n) na imagem
	mediana(imagem, imagem.load(), m, n)

	# * Registo do tempo do final da execução
	tempoFim: float = time()
	print(f"5 - {tempoFim - tempoInicio :2.6}s : Mediana")

	# * Salvando e mostrando o resultado, e fechando a imagem
	imagem.save(resultado + "4_mediana.png")
	if mostrarResultante:
		imagem.show()
	imagem.close()
