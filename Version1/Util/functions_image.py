import numpy as np
import cv2
from Config.Constantes.skin_color import franja_colores
from Config.videos_manitor import LIENZO_MOSTRAR_VIDEOS


def LeerFotograma(cap):
    _, frame = cap.read()
    # cv2.imshow("Original Image", frame)
    return frame


def CrearMascara(frame):
    masking, punto_elegido = None, None
    if frame is not None:
        # convierto la imagen a HSV para quitar capas y mejorar el procesamiento
        hsv_img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Creo una mascara, donde pinto en blanco el color a buscar (color piel) y en negro lo que no cumpla dentro del color de interes
        masking = cv2.inRange(hsv_img, franja_colores["min"], franja_colores["max"])

        # eliminamos el ruido
        if False:
            kernel = np.ones((10, 10), np.uint8)
            masking = cv2.morphologyEx(masking, cv2.MORPH_OPEN, kernel)
            masking = cv2.morphologyEx(masking, cv2.MORPH_CLOSE, kernel)

        # Detectamos contornos, nos quedamos con el mayor y calculamos su centro
        punto_elegido = 0
        if False:
            contours, hierarchy = cv2.findContours(masking, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            mayor_contorno = max(contours, key=cv2.contourArea)
            momentos = cv2.moments(mayor_contorno)
            cx = float(momentos['m10'] / momentos['m00'])
            cy = float(momentos['m01'] / momentos['m00'])
            punto_elegido = np.array([[[cx, cy]]], np.float32)

        # cv2.imshow("Deteccion Color", masking)
    return masking, punto_elegido


def QuitarPartesNoMarcadasEnMascara(frame, masking):
    # Creo una nueva imagen tomando la imagen original y dejando solo las partes blancas de la mascara
    new_img = cv2.bitwise_and(frame, frame, mask=masking)
    return new_img


def CalcularNuevaDimension(actual, marco=0.8):
    deseado_0 = int(LIENZO_MOSTRAR_VIDEOS[0] * marco)
    deseado_1 = int(LIENZO_MOSTRAR_VIDEOS[1] * marco)

    dimen_0 = (deseado_0) / actual[0]
    dimen_1 = (deseado_1) / actual[1]

    nuevo_0 = int(actual[0] * dimen_0), int(actual[1] * dimen_0)
    nuevo_1 = int(actual[0] * dimen_1), int(actual[1] * dimen_1)

    if LIENZO_MOSTRAR_VIDEOS[0] >= nuevo_0[0] and LIENZO_MOSTRAR_VIDEOS[1] >= nuevo_0[1]:
        return dimen_0

    if LIENZO_MOSTRAR_VIDEOS[0] >= nuevo_1[0] and LIENZO_MOSTRAR_VIDEOS[1] >= nuevo_1[1]:
        return dimen_1

    return 1


def CrearFondoPonerVideos():
    black_screen = np.zeros([LIENZO_MOSTRAR_VIDEOS[0], LIENZO_MOSTRAR_VIDEOS[1], 3],
                            dtype=np.uint8)  ## fondo donde poner el video

    return black_screen
