import cv2
import time

from Util.util import currentTime
from Util.util_deteccion_movimiento import Deteccion_movimiento


class Proceso_deteccion_movimiento:
    def iniciar_proceso(self):
        print("Proceso iniciado")

    def primer_movimiento_detectado(self):
        print("Primer movimiento")

    def terminar_proceso(self):
        print("Proceso terminado")

    def primer_preaviso_no_movimiento(self):
        print("Primer preaviso")

    def segundo_preaviso_no_movimiento(self):
        print("Segundo preaviso")

    def tercer_preaviso_no_movimiento(self):
        print("Tercer preaviso, por favor repita la instruccion")

    def mostrar_siguiente_video(self):
        print("Siguiente instruccion")

dm = Deteccion_movimiento(0, Proceso_deteccion_movimiento)

chrono_temporal = currentTime()
while True:
    frame = dm.proceso_completo()

    if not dm.PROCESS_DETECT_MOVE:
        if abs(chrono_temporal - currentTime()) >= 10:
            chrono_temporal = currentTime()
            dm.iniciar_proceso_deteccion_movimiento()
    else:
        chrono_temporal = currentTime()

    cv2.imshow("frame", frame)

    time.sleep(0.025)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

dm.cerrar_camara()
cv2.destroyAllWindows()
