import cv2
import cvlib as cv
from cvlib.object_detection import draw_bbox
import urllib.request
import numpy as np
import requests
import json

url = 'http://192.168.2.98/cam-hi.jpg'

# URL do Realtime Database
link_base = 'https://projetopcs-default-rtdb.firebaseio.com/'

# Dados a serem enviados
dados = {'lotado': 1}
modifica = 0

def contar_pessoas(imagem):
    bbox, label, conf = cv.detect_common_objects(imagem)
    pessoas_detectadas = 0
    for l in label:
        if l == 'person':
            pessoas_detectadas += 1
    return pessoas_detectadas, bbox, label, conf

def detectar_pessoas():
    cv2.namedWindow("detection", cv2.WINDOW_AUTOSIZE)
    while True:
        img_resp = urllib.request.urlopen(url)
        imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
        imagem = cv2.imdecode(imgnp, -1)

        pessoas, bbox, label, conf = contar_pessoas(imagem)
        imagem = draw_bbox(imagem, bbox, label, conf)
        cv2.putText(imagem, f'Pessoas: {pessoas}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        print(f"Quantidade de pessoas detectadas: {pessoas}")

        if(pessoas >5):
            modifica = requests.patch(f'{link_base}/sistema/.json', json=dados)

        cv2.imshow('detection', imagem) 
        key = cv2.waitKey(5)
        if key == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == '__main__':
    detectar_pessoas()
