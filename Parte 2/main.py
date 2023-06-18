##### Segunda parte da disciplina

from PIL import Image

def expansao_de_histograma(imagem_rgb, matriz):

    largura, altura = imagem_rgb.size

    max_R = 0 
    max_G = 0
    max_B = 0
    min_R = 255
    min_G = 255
    min_B = 255

    for i in range(largura):
            for j in range(altura):
                pixel = matriz[i,j]

                if (pixel[0] > max_R):
                    max_R = pixel[0]
                if (pixel[0] < min_R):
                    min_R = pixel[0]
                
                if (pixel[1] > max_G):
                    max_G = pixel[1]
                if (pixel[1] < min_G):
                    min_G = pixel[1]

                if (pixel[2] > max_B):
                    max_B = pixel[2]
                if (pixel[2] < min_B):
                    min_B = pixel[2]

    mapeamento_R = [0]*256
    mapeamento_G = [0]*256
    mapeamento_B = [0]*256

    for i in range(256):
            mapeamento_R[i] = round( (i - min_R)/(max_R - min_R)*(255) )
            mapeamento_G[i] = round( (i - min_G)/(max_G - min_G)*(255) )
            mapeamento_B[i] = round( (i - min_B)/(max_B - min_B)*(255) )

    for i in range(largura):
            for j in range(altura):
                pixel = matriz[i,j]

                R = mapeamento_R[pixel[0]]
                G = mapeamento_G[pixel[1]]
                B = mapeamento_B[pixel[2]]

                matriz[i,j] = (R,G,B)

def equalizacao_de_histograma(imagem_rgb, matriz):

    largura, altura = imagem_rgb.size

    quant_pixels_R = [0]*256
    quant_pixels_G = [0]*256
    quant_pixels_B = [0]*256

    for i in range(largura):
            for j in range(altura):
                pixel = matriz[i,j]

                quant_pixels_R[pixel[0]] += 1
                quant_pixels_G[pixel[1]] += 1
                quant_pixels_B[pixel[2]] += 1

    for i in range(1, 256):
            quant_pixels_R[i] = quant_pixels_R[i - 1] + quant_pixels_R[i]
            quant_pixels_G[i] = quant_pixels_G[i - 1] + quant_pixels_G[i]
            quant_pixels_B[i] = quant_pixels_B[i - 1] + quant_pixels_B[i]

    mapeamento_R = [0]*256
    mapeamento_G = [0]*256
    mapeamento_B = [0]*256

    for i in range(256):
            mapeamento_R[i] = round( (255/(altura*largura))*quant_pixels_R[i] )
            mapeamento_G[i] = round( (255/(altura*largura))*quant_pixels_G[i] )
            mapeamento_B[i] = round( (255/(altura*largura))*quant_pixels_B[i] )

    for i in range(largura):
            for j in range(altura):
                pixel = matriz[i,j]

                R = mapeamento_R[pixel[0]]
                G = mapeamento_G[pixel[1]]
                B = mapeamento_B[pixel[2]]

                matriz[i,j] = (R,G,B)


def media_imagens(image1, image2, t):

    if (image1.size != image2.size):
        return False

    largura, altura = image1.size
    matriz1 = image1.load()
    matriz2 = image2.load()

    ret_image = Image.new('RGB', (largura, altura), (0,0,0))
    ret_matriz = ret_image.load()

    for i in range(largura):
            for j in range(altura):
                pixel1 = matriz1[i,j]
                pixel2 = matriz2[i,j]

                R = int((1 - t)*pixel1[0] + t*pixel2[0])
                G = int((1 - t)*pixel1[1] + t*pixel2[1])
                B = int((1 - t)*pixel1[2] + t*pixel2[2])

                ret_matriz[i,j] = (R,G,B)

    return ret_image

def media_nao_uniforme_imagens(image1, image2, funcao_nao_uniforme):
    if (image1.size != image2.size):
        return False

    largura, altura = image1.size
    matriz1 = image1.load()
    matriz2 = image2.load()

    ret_image = Image.new('RGB', (largura, altura), (0,0,0))
    ret_matriz = ret_image.load()

    for coluna in range(largura):
        for linha in range(altura):

            t = funcao_nao_uniforme(linha, coluna, altura, largura)

            pixel1 = matriz1[coluna,linha]
            pixel2 = matriz2[coluna,linha]

            
            R = int((1 - t)*pixel1[0] + t*pixel2[0])
            G = int((1 - t)*pixel1[1] + t*pixel2[1])
            B = int((1 - t)*pixel1[2] + t*pixel2[2])

            # R = int(t*pixel1[0] + (1 - t)*pixel2[0])
            # G = int(t*pixel1[1] +  (1 - t)*pixel2[1])
            # B = int(t*pixel1[2] + (1 - t)*pixel2[2])

            ret_matriz[coluna,linha] = (R,G,B)

    return ret_image


def func1(linha, coluna, R, C): 
    return coluna/(C - 1)

def func2(linha, coluna, R, C): 
    return (C - 1 - coluna)/(C - 1)

def func3(linha, coluna, R, C): 
    return linha/(R - 1)

def func4(linha, coluna, R, C): 
    return (R - 1 - linha)/(R - 1)

def func5(linha, coluna, R, C):
    return (R + C - 2 - linha - coluna)/(R + C - 2)

def func6(linha, coluna, R, C):
    return (linha + coluna)/(R + C - 2)

def func7(linha, coluna, R, C):
    return (C - 1 - coluna + linha)/(R + C - 2)

def func8(linha, coluna, R, C):
    return (R - 1 + coluna - linha)/(R + C - 2)

def aplicar_expansao_histograma(url, show: bool, show_before: bool):
    image = Image.open(url)
    if(show_before):
            image.show()
    expansao_de_histograma(image, image.load())
    if(show):
            image.show()

def aplicar_equalizacao_histograma(url, show: bool, show_before: bool):
    image = Image.open(url)
    if(show_before):
            image.show()
    equalizacao_de_histograma(image, image.load())
    image.save('teste.jpg')
    if(show):
            image.show()

imagemNome = '1_L_5_2'
imagem1URL = f'.\\enhancements100\\{imagemNome}.png'
imagemNSURL = f'.\\baseOriginal\\100\\ns\\{imagemNome}.png'
imagemTeleaURL = f'.\\saida\\dilatacao-2x2\\telea\\{imagemNome}.png'

imagem1 = Image.open(imagem1URL).convert('RGB')
imagemNS = Image.open(imagemNSURL).convert('RGB')
imagemTelea = Image.open(imagemTeleaURL).convert('RGB')

ns = media_imagens(imagem1, imagemNS, 0.25)
telea = media_imagens(imagem1, imagemTelea, 0.25)

ns.save('ns.png')
telea.save('telea.png')