import cv2
import numpy as np
import time
from Util.util import FrameSinRuido

last_areas = list()
def hallar_contornos_areas(frame, masking, constante = 500):
    global last_areas

    thresh = cv2.threshold(masking, 25,255, cv2.THRESH_BINARY)[1]   # (masking,127,255,   0) # Aplicamos un umbral para quitar ruido
    thresh = cv2.dilate(thresh, None, iterations=2) # Dilatamos el umbral para tapar agujeros

    contornos = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0] # CHAIN_APPROX_SIMPLE: deja solo los contornos externos obviando los internos (ahorrar memoria y aumentar velocidad computo)

    cajas = list()
    areas = list()
    contornos_finales = list()
    for c in contornos:                 # Recorremos todos los contornos encontrados
        if cv2.contourArea(c) < constante:    # Eliminamos los contornos mas pequenos
            continue
        (x, y, w, h) = cv2.boundingRect(c) # Obtenemos el bounds del contorno, el rectángulo mayor que engloba al contorno
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cajas.append((x,y,x+w,y+h))
        contornos_finales.append(c)

        area = w*h
        areas.append(area)

    cv2.drawContours(frame, contornos_finales, -1, (255,0,0), 3)

    # Determinar movimiento de acuerdo a el cambio de areas (superior a una constante definida) en objeto(s) en la escena
    hay_movimiento_segun_cambio_areas = False
    if len(last_areas) == len(areas):        # if exist(True) in list(  if abs(valor)>constante*1.5 => valor = resta(last_areas, areas)  )
        hay_movimiento_segun_cambio_areas = True if True in [True if i>constante*1.5 else False for i in [abs(i) for i in [e1 - e2 for e1, e2 in zip(last_areas,areas)]]] else False
    else:
        hay_movimiento_segun_cambio_areas = True
        pass
    last_areas = areas

    return cajas, areas, hay_movimiento_segun_cambio_areas



if False:
    doHaveFirtsImage = False
    lk_params = dict( winSize = (15,15),
                    maxLevel = 2,
                    criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

    def getFlow(antes, ahora):
        flow = cv2.calcOpticalFlowFarneback(antes, ahora, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        #flow = cv2.calcOpticalFlowFarneback(antes, ahora, None, 0.4, 8, 10, 5, 7, 3.5, 0)
        return flow

    def ProcessOpticalFlow(antes, ahora):
        flow = getFlow(antes,ahora)
        mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
        hsv[...,0] = ang*180/np.pi/2
        hsv[...,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
        rgb = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)
        return rgb


cap = cv2.VideoCapture(0)
if __name__ == "__main__":
    while(1):
        time_start = time.time()

        frame, punto_elegido, frame_original, masking = FrameSinRuido(cap)
        next = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if False:
            if not doHaveFirtsImage:
                doHaveFirtsImage = True
                prvs = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                hsv = np.zeros_like(frame)
                hsv[...,1] = 5 # 255

        if False:
            # *** Aplicar Optical Flow para determinar movimiento
            next = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            rgb = ProcessOpticalFlow(prvs, next)
            rgb = cv2.GaussianBlur(rgb, (21, 21), 0) #aplicamos suavizado para eliminar el ruido
            cv2.imshow('rgb',rgb)

        if True:
            constante = 1000 # 500
            cajas, areas, hay_movimiento_segun_cambio_areas = hallar_contornos_areas(frame, masking, constante)

            # Impresion de resultados de movimiento detectado
            cv2.putText(frame,'Movimiento por:',(30,30),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,255),2,cv2.LINE_AA)
            if hay_movimiento_segun_cambio_areas:
                cv2.circle(frame,(35,54),10,(255,0,255),-1)
                cv2.putText(frame,'Cambio Area',(50,60),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,255,255),2,cv2.LINE_AA)







        cv2.imshow("frame", frame)
        # cv2.imshow("frame_original", frame_original)
        # cv2.imshow("masking", masking)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
        prvs = next

        # *******************************
        time_end = time.time()
        print("time process: ", int((time_end-time_start)*1000), "milisegundos")

    cap.release()
    cv2.destroyAllWindows()