#Importação dos pacotes
import cv2
import time
import numpy as np
import math

import HandTrackingModule as htm

from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Parâmetros da câmera (resolução da tela)
##################################################
wCam, hCam = 640, 480
##################################################

# Inicialização das classes para mudança de volume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)

volRange = volume.GetVolumeRange() # Obtendo o Range de volume

# Inicializando as variáveis de volume 
vol = 0

#Recebendo o volume máximo e mínimo
minVol = volRange[0]
maxVol = volRange[1]

# Escolhendo qual câmera será capturada
cap = cv2.VideoCapture(0)
cap.set(3, wCam) # Setando a resolução largura
cap.set(4, hCam) # Setando a resolução altura

pTime = 0 # Previous time, para obter o FPS

detector = htm.handDetector(detectionConfidence=0.7) # Inicialização da classe Hands no módulo 'HandTrackingModule'

# Inicialização da captura
while True:
    success, img = cap.read() # Leitura da imagem capturada pela webcam
    img = detector.findHands(img) # Detectando a mão
    lmList = detector.findPosition(img, draw=False) # Recebendo a lista das posições da mão

    # Caso haja alguma mão na tela
    if len(lmList) != 0:
        x1, y1 = lmList[4][1], lmList[4][2] # Recebendo as posições da ponta do polegar [4] * Ps: Cada parte da mão existe um ID 
        x2, y2 = lmList[8][1], lmList[8][2] # Recebendo a posição da ponta do indicador [8] * Ps: Cada parte da mão existe um ID
        
        x3, y3 = lmList[0][1], lmList[0][2] # Recebendo a posição da parte de baixo da palma da mão [0] * Ps: Cada parte da mão existe um ID
        x4, y4 = lmList[9][1], lmList[9][2] # Recebendo a posição da parte de baixo do dedo do meio [9] * Ps: Cada parte da mão existe um ID

        # Recebendo o tamanho da diferença da distância 
        # entre a parte de baixo da palma da mão e a parte de baixo do dedo do meio
        distanceBetweenBottomHandBottomMiddle = math.hypot((x3-x4)/wCam, (y3-y4)/hCam) 
        
        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED) # Desenhando circulo apenas no polegar
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED) # Desenhando circulo apenas no indicador

        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3) # Desenhando uma linha que faz um ligamento entre a ponta do polegar e a ponta do indicador 

        # Recebendo o tamanho da diferença da distância entre a ponta do polegar e a ponta do indicador
        distanceBetweenTopIndexTopThumb = math.hypot((x2-x1)/wCam, (y2-y1)/hCam) 

        # Resolvendo a mudança de volume, dividindo as distâncias, para que não ocorra quando se afastar ou se aproximar 
        # da câmera haver alteração no resultado
        changeVolume = distanceBetweenTopIndexTopThumb / distanceBetweenBottomHandBottomMiddle

        # Volume range -50 - 5, do meu computador
        
        vol = np.interp(changeVolume, [0, 1], [minVol, maxVol]) # Convertendo a distância entre os ranges de [20 - 270] e para os volumes mínimos e máximos

        volume.SetMasterVolumeLevel(vol, None) # Setando o volume de acordo com a converção
    
    # Colocando o FPS na tela
    cTime = time.time() # Recebendo o tempo atual 
    fps = 1/(cTime-pTime) # Cálculando o FPS
    pTime = cTime # Atribuindo ao tempo anterior o tempo atual

    cv2.putText(img, f'FPS:{int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 2) # Colocando o FPS na tela

    cv2.imshow("Img", img) # Mostrar a imagem da webcam 
    cv2.waitKey(1) # Tempo de mostragem da tela em milisegundos