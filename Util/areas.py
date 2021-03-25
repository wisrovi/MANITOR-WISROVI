#############################
import cv2
from Config.movimiento_frente_camara import constante_cambio_area

last_areas = list()


def hallar_contornos_areas(self, frame, masking):
    global last_areas

    thresh = cv2.threshold(masking, 25, 255, cv2.THRESH_BINARY)[
        1]  # (masking,127,255,   0) # Aplicamos un umbral para quitar ruido
    thresh = cv2.dilate(thresh, None, iterations=2)  # Dilatamos el umbral para tapar agujeros

    contornos = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[
        0]  # CHAIN_APPROX_SIMPLE: deja solo los contornos externos obviando los internos (ahorrar memoria y aumentar velocidad computo)

    cajas = list()
    areas = list()
    contornos_finales = list()
    for c in contornos:  # Recorremos todos los contornos encontrados
        if cv2.contourArea(c) < constante_cambio_area:  # Eliminamos los contornos mas pequenos
            continue
        (x, y, w, h) = cv2.boundingRect(
            c)  # Obtenemos el bounds del contorno, el rectángulo mayor que engloba al contorno
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cajas.append((x, y, x + w, y + h))
        contornos_finales.append(c)

        area = w * h
        areas.append(area)

    cv2.drawContours(frame, contornos_finales, -1, (255, 0, 0), 3)

    # Determinar movimiento de acuerdo a el cambio de areas (superior a una constante definida) en objeto(s) en la escena
    hay_movimiento_segun_cambio_areas = False
    if len(last_areas) == len(
            areas):  # if exist(True) in list(  if abs(valor)>constante*1.5 => valor = resta(last_areas, areas)  )
        hay_movimiento_segun_cambio_areas = True if True in [True if i > constante_cambio_area * 1.5 else False for i in
                                                             [abs(i) for i in [e1 - e2 for e1, e2 in
                                                                               zip(last_areas, areas)]]] else False
    else:
        hay_movimiento_segun_cambio_areas = True
        pass
    last_areas = areas

    return cajas, areas, hay_movimiento_segun_cambio_areas
#############################
