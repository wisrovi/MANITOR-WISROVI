from Config.videos_manitor import INSTRUCCIONES
from Util.util_show_videos import Avatar_video

avatar_class = Avatar_video('../resources')


def Contar(*args):
    if avatar_class.instruccion_actual >= len(INSTRUCCIONES):
        avatar_class.terminar_proceso_avatar()
    else:
        avatar_class.continuar_siguiente_paso_instruccion()


import cv2

cv2.namedWindow("Frame")
cv2.createButton("Contar", Contar, None, cv2.QT_PUSH_BUTTON, 1)

if __name__ == "__main__":
    avatar_class.iniciar_avatar()

    while True:
        black_screen, video_inicial_final = avatar_class.proceso()

        if video_inicial_final is not None:
            pass
            # if avatar_class.get_instruccion_actual() > 0:
            #     font = cv2.FONT_HERSHEY_SIMPLEX
            #     org = (50, 50)
            #     fontScale = 1
            #     color = (255, 0, 0)  # BLue
            #     thickness = 2  # Line thickness
            #     black_screen = cv2.putText(black_screen, INSTRUCCIONES[avatar_class.get_instruccion_actual() - 1]['name'], org,
            #                                     font,
            #                                     fontScale,
            #                                     color,
            #                                     thickness, cv2.LINE_AA)

        cv2.imshow("Frame", black_screen)

        # ---------------- salida del while al oprimir la tecla ESC
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

    avatar_class.cerrar_avatar()
    cv2.destroyAllWindows()
