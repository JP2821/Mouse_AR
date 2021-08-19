#######################################
#
# By: João Pedro Ribeiro da Silva Dias
#
#######################################
import cv2
import numpy as np
import ControleDaMaoMouseAr as htm
import time
import autopy

################################
CCam, ACam = 640, 480
frameR = 100 #redução dos frames
suavizando = 5
################################

ptime = 0
clocX, clocY = 0, 0

cap = cv2.VideoCapture(0)
cap.set(3, CCam)
cap.set(4, ACam)
detectar=htm.detectarMao(maxMaos=1)
CScr, AScr = autopy.screen.size()

while True:
    # 1. achar maos
    sucesso, img = cap.read()
    img = detectar.procurarMaos(img)
    plocX, plocY = 0, 0
    lmList, bbox = detectar.acharPosicao(img)

    # 2. pegar a ponta do dedo e indicador e o meio
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

    # 3. checar se os dedos estão levantados
        dedos = detectar.dedosParaCima()
        #print(dedos)
        cv2.rectangle(img, (frameR, frameR), (CCam - frameR, ACam - frameR), (255, 0, 255), 2)
    # 4. Só o inidicador : modo de movimento
        if dedos[1]== 1 and dedos[2]== 0:
            # 5. Converter Coordenadas
            x3 = np.interp(x1, (frameR, CCam-frameR), (0, CScr))
            y3 = np.interp(y1, (frameR, ACam-frameR), (0, AScr))

            # 6. Suavizar os valores
            clocX = plocX + (x3 - plocX)/suavizando
            clocY = plocY + (y3 - plocY)/suavizando
            # 7. Mover o mouse
            autopy.mouse.move(CScr - clocX, clocY)
            cv2.circle(img, (x1, y1), 15, (0, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY
    # 8. Ambos inidicar e medio levantados : modo de clicar
        if dedos[1] == 1 and dedos[2] == 1:
            comprimento, img, lineInfo =detectar.acharDistancia(8, 12, img)
            if comprimento < 40:
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0),cv2.FILLED)
                autopy.mouse.click()
    # 9. Achar a distância entre os dedos
    # 10. Clique do mouse se a distancia for curta

    #11. Display de FPS
    ctime = time.time()
    fps = 1/(ctime-ptime)
    ptime = ctime
    cv2.putText(img, str(int(fps)),(20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    #interface
    cv2.imshow("MouseAr1.0", img)
    cv2.waitKey(1)
