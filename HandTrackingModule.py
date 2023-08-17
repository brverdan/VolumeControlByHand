#Importação dos pacotes
import cv2 
import mediapipe as mp

#Criação da classe de detecção das mãos
class handDetector():
    #Inicialização da classe
    #Os parâmetros são com base nos parâmetros da classe Hands do pacote 'mediapipe'
    def __init__(self, mode=False, maxHands=2, modelComp=1, detectionConfidence=0.5, trackConfidence=0.5):
        self.mode = mode # Se as imagens de entrada são estáticas ou é um vídeo 
        self.maxHands = maxHands # Máximo de mão possiveis para detectar
        self.detectionConfidence = detectionConfidence # Confiança de detecção [0 - 1], caso seja menor do que o parâmetro irá ocorrer uma nova tentativa de detecção  
        self.trackConfidence = trackConfidence # Confiança de rastreamento, caso seja menor do que o parâmetro irá ocorrer uma nova tentativa de rastreamento 
        self.modelComp = modelComp # Complexidade do landmark da mão

        self.mpHands = mp.solutions.hands # Recebendo a classe do mediapipe
        
        #Recebendo a classe Hands e passando os parâmetros vindo da inicialização da classe handDetector
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelComp, self.detectionConfidence, self.trackConfidence)
        self.mpDraw = mp.solutions.drawing_utils # Recebendo o objeto de desenho

    #Função para detectar as mãos
    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # Converter a imagem em RGB
        self.results = self.hands.process(imgRGB) # Recebendo os resultados do processamento das imagens  

        if self.results.multi_hand_landmarks: #Caso haja alguma mão detectada
            for handLms in self.results.multi_hand_landmarks: # Para cada mão detectada na imagem (O máximo de mãos possíveis é determinada pelo parâmetro 'maxHands')
                if draw:  # Caso o usuário deseje desenhar as linhas de marcação
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS) # Para desenhar as linhas de marcação na mão

        return img # Retornando a imagem
    
    #Função para detectar a posição da mão
    def findPosition(self, img, handNumber=0, draw=True):

        lmList = [] # Inicialização da lista de marcação da mão

        if self.results.multi_hand_landmarks: # Caso haja detecção da mão 
            firstHand = self.results.multi_hand_landmarks[handNumber] # Recebendo as marcações da mão 

            for id, lm in enumerate(firstHand.landmark): # O ID e a marcação do ponto da mão
                h, w, c = img.shape # Recebendo a altura, largura e os canais da imagem
                cx, cy = int(lm.x*w), int(lm.y*h) # cx e cy são as posições do centro  
                lmList.append([id, cx, cy]) # Adicionando 
                if draw: # Caso o usuário deseje desenhar os circulos de marcação 
                    cv2.circle(img, (cx, cy), 15, (255,0,255), cv2.FILLED) # Desenhando os circulos 

        return lmList # Retornando a lista com as marcações