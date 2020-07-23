# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 20:53:58 2020
@author: pcardona
matplotlib: https://matplotlib.org/
cv2 : https://opencv.org/  
img_Color = mpimg.imread("img/image.jpg
numpy : https://numpy.org/
threshold: 
https://docs.opencv.org/master/d7/d4d/tutorial_py_thresholding.html
getStructuringElement, morphologyEx, MORPH_CLOSE
https://docs.opencv.org/trunk/d9/d61/tutorial_py_morphological_ops.html
findContours: 
https://docs.opencv.org/2.4/modules/imgproc/doc/structural_analysis_and_shape_descriptors.html
fillPoly:
https://docs.opencv.org/2.4/modules/core/doc/drawing_functions.html
"""
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import cv2 


#Comprueba que la imagen no cuente con transparencia (canal alfa).
def CanalAlfa(img):
  alto, ancho, Canales = img.shape
  print("Alto : " , alto , " Ancho: " , ancho , " Canales : " , Canales)
  if Canales < 4:
    #Convierte a escala de grises la imagen.  
    img_Gris = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    return img_Gris

  return img

#Recorta la imagen dejando solo la seccion que corresponde al icono.
def RecortarImagen(img):
  #Convierte la imagen en escala de grises.
  img_Gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  #Para cada pixel se aplica el mismo valor umbral
  th, threshed = cv2.threshold(img_Gris, 240, 255, cv2.THRESH_BINARY_INV)
  #Se genera un nucleo con la libreria de openCv
  kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11,11))
  #Transformacion morfologica (cierre) : 
  #Permite cerrar pequeños agujeros dentro de los objetos en primer plano, 
  #o pequeños puntos negros en el objeto.
  morphed = cv2.morphologyEx(threshed, cv2.MORPH_CLOSE, kernel)
  #Encuentra contornos en una imagen binaria
  contornos, _ = cv2.findContours(morphed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  #Ordena los contornos
  contornos_ord = sorted(contornos, key=cv2.contourArea)[-1]
  #Genera la imagen recortada
  x,y,w,h = cv2.boundingRect(contornos_ord)
  img_recortada = img[y:y+h, x:x+w]
  return img_recortada  


#Genera la transparencia de la imagen
def GeneraTransparencia(img):   
  #Convierte la imagen a escala de grises
  img_gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  #Para cada pixel se aplica el mismo valor umbral
  th, threshed = cv2.threshold(img_gris, 240, 255, cv2.THRESH_BINARY_INV)
  #Se genera un nucleo con la libreria de openCv
  kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11,11))
  #Transformacion morfologica (cierre) : 
  morphed = cv2.morphologyEx(threshed, cv2.MORPH_CLOSE, kernel)
  #Encuentra contornos en una imagen binaria
  roi, _ = cv2.findContours(morphed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  #Se genera una mascara con las caracteristicas de la imagen, con ayuda de numpy
  mask = np.zeros(img.shape, img.dtype)
  #Rellena el area limitada por uno o mas poligonos
  cv2.fillPoly(mask, roi, (255,)*img.shape[2], )
  masked_image = cv2.bitwise_and(img, mask)
  return masked_image


#Lee la imagen
def EliminarFondo(img, out):
    img_Color = mpimg.imread(img)
    img_Color = CanalAlfa(img_Color)
    img_Color = RecortarImagen(img_Color)
    img_Color = GeneraTransparencia(img_Color)
    #Guarda la imagen en la ruta especificada
    mpimg.imsave(out + ".png", img_Color)
    plt.imshow(img_Color)
    img_Color.shape
