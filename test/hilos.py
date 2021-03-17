from Config.videos_manitor import GUIONES, PATH_VIDEOS
from Util.functions_image import CrearFondoPonerVideos
from Util.util_sound import iniciar_sounds, reproducir

iniciar_sounds("../resources/")

indicador = -1


def Contar(*args):
    global indicador
    indicador = 0 if indicador > len(GUIONES) else indicador + 1

    reproducir(indicador)
    print("Boton oprimido")


import cv2

cv2.namedWindow("Frame")
cv2.createButton("Contar", Contar, None, cv2.QT_PUSH_BUTTON, 1)

import time

if __name__ == "__main__":
    while True:
        start_time = time.time()
        black_screen = CrearFondoPonerVideos()

        cv2.imshow("Frame", black_screen)

        time.sleep(0.02)
        print("Time:{}".format(int((time.time() - start_time) * 1000) / 1000))
        # ---------------- salida del while al oprimir la tecla ESC
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

    cv2.destroyAllWindows()
