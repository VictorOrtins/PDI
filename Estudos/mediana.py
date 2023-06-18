import math

def mediana(image, matriz_rgb, mascara_m, mascara_n):
  altura: int = image.size[0]
  comprimento: int = image.size[1]

  mascara: list = []
  for i in range(mascara_m):
    for j in range(mascara_n):
      mascara.append( (i,j) )

  elemento_mediana : int = math.floor( (mascara_m * mascara_n) /2)

  
  for i in range(altura):
    for j in range(comprimento):
      vizinhanca: list = []

      for k in range(len(mascara)):
        if i + mascara[k][0] > 255 or j + mascara[k][1] > 255:
          pixel = (0,0,0)
        else:
          pixel = matriz_rgb[i + mascara[k][0], j + mascara[k][1]]

        vizinhanca.append(pixel[0])

      vizinhanca.sort()

      R = vizinhanca[elemento_mediana]

      vizinhanca = []

      for k in range(len(mascara)):
        if i + mascara[k][0] > 255 or j + mascara[k][1] > 255:
          pixel = (0,0,0)
        else:
          pixel = matriz_rgb[i + mascara[k][0], j + mascara[k][1]]

        vizinhanca.append(pixel[1])

      vizinhanca.sort()

      G = vizinhanca[elemento_mediana]

      vizinhanca = []

      for k in range(len(mascara)):
        if i + mascara[k][0] > 255 or j + mascara[k][1] > 255:
          pixel = (0,0,0)
        else:
          pixel = matriz_rgb[i + mascara[k][0], j + mascara[k][1]]

        
        vizinhanca.append(pixel[2])

      vizinhanca.sort()

      B = vizinhanca[elemento_mediana]


      matriz_rgb[i,j] = (R,G,B)


image = Image.open('maca.png')
image.show()

print('--------------------')

mediana(image, image.load(), 3, 3)
image.show()