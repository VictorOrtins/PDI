from time import time
from enum import Enum

import cv2
import os

import threading

class formatoMascara(Enum):
    ELIPSE = "elipse"
    RETANGULAR = "retangulo"

class preProcessamentoMascara(Enum):
    DILATACAO = "dilate"
    MORPH = "morph"
    EROSAO = "erode"

def aplicarTelea(nome: str, imagem, mascara, valor: int, endereco: str):
    telea = cv2.inpaint(imagem, mascara, valor, cv2.INPAINT_TELEA)
    cv2.imwrite(endereco + f"\\{nome}.png", telea)
    
def aplicarNS(nome: str, imagem, mascara, valor: int, endereco: str):
    ns = cv2.inpaint(imagem, mascara, valor, cv2.INPAINT_NS)
    cv2.imwrite(endereco + f"\\{nome}.png", ns)

def aplicarProcessamentoMascara(mascara, m_matriz, n_matriz, preProcessamento: preProcessamentoMascara, formato: formatoMascara, iteracoes=1, tipo=cv2.MORPH_CLOSE):
    if preProcessamento == preProcessamentoMascara.DILATACAO:
        return aplicarDilateMascara(mascara, m_matriz, n_matriz, formato, iteracoes)
    elif preProcessamento == preProcessamentoMascara.EROSAO:
        return aplicarErodeMascara(mascara, m_matriz, n_matriz, formato, iteracoes)
    else:
        return aplicarMorph(mascara, m_matriz, n_matriz, formato, tipo)

def aplicarDilateMascara(mascara, m_matriz, n_matriz, formato: formatoMascara, iteracoes):
    kernel = cria_kernel(m_matriz, n_matriz, formato)
    nova_mascara = cv2.dilate(mascara, kernel, iterations = iteracoes)
    return nova_mascara

def aplicarErodeMascara(mascara, m_matriz, n_matriz, formato: formatoMascara, iteracoes):
    kernel = cria_kernel(m_matriz, n_matriz, formato)
    nova_mascara = cv2.erode(mascara, kernel, iterations = iteracoes)
    return nova_mascara

def aplicarMorph(mascara, m_matriz, n_matriz, formato: formatoMascara, tipo):
    kernel = cria_kernel(m_matriz, n_matriz, formato)
    nova_mascara = cv2.morphologyEx(mascara, tipo, kernel)
    return nova_mascara

def cria_kernel(m_matriz, n_matriz, formato: formatoMascara):
    if formato == formatoMascara.ELIPSE:
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (m_matriz, n_matriz))
    elif formato == formatoMascara.RETANGULAR:
        kernel = np.ones( (m_matriz, n_matriz), np.uint8)

    return kernel

def preProcessamento(caminho_base):
    nomes_arquivos = os.listdir(caminho_base) 

    tam_mascara = 2

    enderecoMascaraTelea = f'.\\mascara\\telea'
    enderecoMascaraNs = f'.\\mascara\\ns'

    try:
        os.mkdir('.\\mascara')
    except FileExistsError as e:
        pass

    try:
        os.mkdir('.\\mascara\\ns')
    except FileExistsError as e:
        pass    

    try:
        os.mkdir('.\\mascara\\telea')
    except FileExistsError as e:
        pass

    for c in range(0, len(nomes_arquivos), 2):
        nomeArquivo: str = nomes_arquivos[c][0:nomes_arquivos[c].find('.')]
        
        # Carregar a imagem à qual será aplicada a máscara
        imagem = cv2.imread(f'.\{caminho_base}\\' + nomes_arquivos[c])

        # Mascara usada na imagem
        mascara = cv2.imread(f'.\{caminho_base}\\' + nomes_arquivos[c + 1])

        mascara = 255 - mascara

        cv2.imwrite(enderecoMascaraNs + '\\' + nomeArquivo + '.png', mascara)

        mascara = aplicarProcessamentoMascara(mascara, tam_mascara, tam_mascara, preProcessamentoMascara.DILATACAO, formatoMascara.ELIPSE, 1, None)

        cv2.imwrite(enderecoMascaraTelea + '\\' + nomeArquivo + '.png', mascara)


def rodar_base(valor_inpaint, caminho_base):
    # Obtém os nomes dos arquivos no diretório
    nomes_arquivos = os.listdir(caminho_base)  

    threads: list = []
        
    valor: int = valor_inpaint

    enderecoMascaraTelea: str = f'.\\mascara\\telea\\'
    enderecoMascaraNs: str = f'.\\mascara\\ns\\'

    try:
        os.mkdir(f'.\\baseInicial')
    except FileExistsError as e:
        pass

    try:
        os.mkdir(f'.\\baseInicial\\telea')
    except FileExistsError as e:
        pass
    
    try:
        os.mkdir(f'.\\baseInicial\\ns')
    except FileExistsError as e:
        pass

    salvarTelea: str = f'.\\inpaint\\telea'
    salvarNs: str = f'.\\inpaint\\ns'

    try:
        os.mkdir(f'.\\inpaint')
    except FileExistsError as e:
        pass
    
    try:
        os.mkdir(f'.\\inpaint\\telea')
    except FileExistsError as e:
        pass

    try:
        os.mkdir(f'.\\inpaint\\ns')
    except FileExistsError as e:
        pass

    for c in range(0, len(nomes_arquivos), 2):
        nomeArquivo: str = nomes_arquivos[c][0:nomes_arquivos[c].find('.')]
        # Carregar a imagem à qual será aplicada a máscara
        imagem = cv2.imread(f'.\{caminho_base}\\' + nomes_arquivos[c])

        mascaraTelea = cv2.imread(enderecoMascaraTelea + f'{nomeArquivo}.png', cv2.IMREAD_GRAYSCALE)
        mascaraNs = cv2.imread(enderecoMascaraNs + f'{nomeArquivo}.png', cv2.IMREAD_GRAYSCALE)

        thread1 = threading.Thread(target=aplicarTelea,args=(nomeArquivo, imagem, mascaraTelea, valor, salvarTelea))
        thread2 = threading.Thread(target=aplicarNS,args=(nomeArquivo, imagem, mascaraNs, valor, salvarNs))

        # Aplicar o inpainting na imagem
        thread1.start()
        thread2.start()

        threads.append(thread1)
        threads.append(thread2)

        # Controlando a quantidade de threads criadas
        if (len(threads) == 10):
            for thread in threads:
                thread.join()
            threads.clear()
        
    if (len(threads) != 0):
        for thread in threads:
            thread.join()

def media_ponderada(caminho_base):
    nomes_arquivos = os.listdir(caminho_base)

    enderecoTelea: str = f'.\\inpaint\\telea'
    enderecoNS: str = f'.\\inpaint\\ns'

    t = 0.99

    arquivos_telea = os.listdir(enderecoTelea)

    arquivos_NS = os.listdir(enderecoNS)

    try:
        os.mkdir(f'.\\final')
    except FileExistsError as e:
        pass
    
    try:
        os.mkdir(f'.\\final\\ns')
    except FileExistsError as e:
        pass

    try:
        os.mkdir(f'.\\final\\telea')
    except FileExistsError as e:
        pass


    for c in range(1, len(nomes_arquivos), 2):
        nomeArquivo: str = nomes_arquivos[c][0:nomes_arquivos[c].find('.')]

        imagemEnhanced = cv2.imread(f'.\\{caminho_base}\\' + nomes_arquivos[c])

        try:
            os.mkdir(f'.\\final\\ns\\' + nomeArquivo)
        except FileExistsError:
            pass

        try:
            os.mkdir(f'.\\final\\telea\\' + nomeArquivo)
        except FileExistsError:
            pass

        for d in range(len(arquivos_NS)):

            imagemTelea = cv2.imread(enderecoTelea + '\\' + arquivos_telea[d])
            imagemNS = cv2.imread(enderecoNS + '\\' + arquivos_NS[d])

            ns = cv2.addWeighted(imagemEnhanced, 1-t, imagemNS, t, 0)
            telea = cv2.addWeighted(imagemEnhanced, 1-t, imagemTelea, t, 0)

            cv2.imwrite(caminho_saida + f'.\\final\\ns\\{nomeArquivo}\\{arquivos_NS[d]}', ns)
            cv2.imwrite(caminho_saida + f'.\\final\\telea\\{nomeArquivo}\\{arquivos_telea[d]}', telea)

def passo_a_passo(valor_inpaint, caminho_base):
    preProcessamento(caminho_base)
    rodar_base(valor_inpaint, caminho_base)
    media_ponderada(caminho_base)


passo_a_passo(2, f'.\\enhancements100')