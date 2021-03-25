class Deteccion_movimiento:
    import cv2

    from Config.movimiento_frente_camara import STATUS_MOVIMIENTO, valor_cambio, TIEMPO_POR_INSTRUCCION
    from Util.areas import hallar_contornos_areas
    from Util.util import FrameSinRuido, currentTime

    chrono_siguiente_instruccion = None
    chrono_tiempo_alerta = None

    PROCESS_DETECT_MOVE = False
    primer_movimiento_secuencia = False
    status = STATUS_MOVIMIENTO[1]
    contador_cambio_estado = 0
    dm = None

    cap = None

    def __init__(self, cam, clase):
        self.elegir_camara(cam)
        self.instanciar_clase(clase)
        self.tiempo = self.TIEMPO_POR_INSTRUCCION

    def instanciar_clase(self, f):
        from Util.util import currentTime
        self.dm = f()
        self.chrono_siguiente_instruccion = currentTime()
        self.chrono_tiempo_alerta = currentTime()

    def iniciar_proceso_deteccion_movimiento(self):
        self.PROCESS_DETECT_MOVE = True
        self.primer_movimiento_secuencia = False
        self.status = self.STATUS_MOVIMIENTO[0]
        self.contador_cambio_estado = 0

        self.dm.iniciar_proceso()

    def terminar_proceso_deteccion_movimiento(self):
        self.PROCESS_DETECT_MOVE = False
        self.primer_movimiento_secuencia = False
        self.status = self.STATUS_MOVIMIENTO[1]
        self.contador_cambio_estado = 0

    def activar_siguiente_video(self):
        self.dm.mostrar_siguiente_video()

    def elegir_camara(self, cam):
        self.cap = self.cv2.VideoCapture(cam)

    def cerrar_camara(self):
        self.cap.release()

    def set_time(self, time_new):
        self.tiempo = time_new

    def proceso_completo(self):
        from Util.util import currentTime
        frame, _, _, masking = self.FrameSinRuido(self.cap)
        _, _, hay_movimiento_segun_cambio_areas = self.hallar_contornos_areas(frame, masking)

        if self.PROCESS_DETECT_MOVE:
            if hay_movimiento_segun_cambio_areas:
                self.cv2.circle(frame, (50, 50), 20, (0, 0, 255), -1)
            else:
                self.cv2.circle(frame, (50, 50), 20, (255, 0, 255), -1)

            if hay_movimiento_segun_cambio_areas:
                if not self.primer_movimiento_secuencia:
                    self.primer_movimiento_secuencia = True
                    self.chrono_siguiente_instruccion = currentTime()
                    self.dm.primer_movimiento_detectado()

                if self.status == self.STATUS_MOVIMIENTO[0]:
                    self.contador_cambio_estado = 0
                else:
                    # si antes no habia movimiento y ahora si lo hay se valida que no se falso positivo al monitorear que el movimiento sea continuo frente a la camara
                    self.contador_cambio_estado += 1
                    if self.contador_cambio_estado > self.valor_cambio / 2:
                        self.status = self.STATUS_MOVIMIENTO[0]
                        self.chrono_siguiente_instruccion = currentTime()

                if self.status == self.STATUS_MOVIMIENTO[0]:
                    if abs(self.chrono_siguiente_instruccion - currentTime()) >= self.tiempo:
                        self.chrono_siguiente_instruccion = currentTime()
                        self.activar_siguiente_video()
            else:
                if self.primer_movimiento_secuencia:
                    if self.status == self.STATUS_MOVIMIENTO[0]:
                        self.contador_cambio_estado += 1
                        if self.contador_cambio_estado == int(self.valor_cambio / 4):
                            self.dm.primer_preaviso_no_movimiento()

                        if self.contador_cambio_estado == int(self.valor_cambio / 3):
                            self.dm.segundo_preaviso_no_movimiento()

                        if self.contador_cambio_estado == int(self.valor_cambio / 2):
                            self.dm.tercer_preaviso_no_movimiento()
                            self.chrono_siguiente_instruccion = currentTime()

                        if self.contador_cambio_estado >= int(self.valor_cambio / 1):
                            self.dm.terminar_proceso()
                            self.terminar_proceso_deteccion_movimiento()
                    else:
                        self.contador_cambio_estado = 0

        return frame


if __name__ == "__main__":
    import cv2
    import time
    from Util.util import currentTime


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
