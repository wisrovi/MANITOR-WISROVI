import time

import cv2

from Config.beacon import TIME_SCAN_BEACON, MINIMA_DISTANCIA_RSSI
from Config.movimiento_frente_camara import TIEMPO_VOLVER_LAVAR_MANOS
from Config.videos_manitor import PATH_VIDEOS, INSTRUCCIONES
from library.ScanBeaconUtility import Beacon_FCV
from Util.mqtt import FinalizarEscuchaMQTT
from Util.util import currentTime
from Util.util_deteccion_movimiento import Deteccion_movimiento
from Util.util_manitor import EnviarNotificacionLavadoManosCompleto, MatricularFuncionRecibidoMQTT, \
    IniciarEscuchaMQTT
from Util.util_show_videos import Avatar_video
from Util.util_sound import iniciar_sounds, reproducir

chrono_beacon_scan = currentTime()
PRIMER_CARDHOLDER = False
avatar_class = Avatar_video(PATH_VIDEOS)

historial_personas = dict()
actual_cardholder = str()

scan_beacon = Beacon_FCV(0, TIME_SCAN_BEACON)


class Orden_mqtt_recibida:
    @staticmethod
    def public_ota():
        print("Orden publica: OTA")

    @staticmethod
    def public_restart():
        print("Orden publica: restart")

    @staticmethod
    def private_ota():
        print("Orden privada: OTA")

    @staticmethod
    def private_restart():
        print("Orden privada: restart")


class Proceso_deteccion_movimiento:
    import time
    tiempo_transcurrido_por_instruccion = time.time()

    @staticmethod
    def iniciar_proceso():
        print("Proceso iniciado")

    def primer_movimiento_detectado(self):
        print("Primer movimiento")
        self.tiempo_transcurrido_por_instruccion = time.time()

    @staticmethod
    def terminar_proceso():
        global PRIMER_CARDHOLDER
        print("Proceso terminado")
        PRIMER_CARDHOLDER = False
        dm.terminar_proceso_deteccion_movimiento()

    @staticmethod
    def primer_preaviso_no_movimiento():
        print("Primer preaviso")

    @staticmethod
    def segundo_preaviso_no_movimiento():
        print("Segundo preaviso")

    @staticmethod
    def tercer_preaviso_no_movimiento():
        print("Tercer preaviso, por favor repita la instruccion")

    def mostrar_siguiente_video(self):
        transcurrido = int((time.time() - self.tiempo_transcurrido_por_instruccion) * 100) / 100
        print(transcurrido, end=": ")
        print("Siguiente instruccion")

        if avatar_class.instruccion_actual >= len(INSTRUCCIONES):
            avatar_class.terminar_proceso_avatar()
            historial_personas[actual_cardholder] = currentTime()
            EnviarNotificacionLavadoManosCompleto(actual_cardholder)
        else:
            reproducir(avatar_class.instruccion_actual)
            avatar_class.continuar_siguiente_paso_instruccion()
            if avatar_class.instruccion_actual <= len(INSTRUCCIONES):
                dm.set_time(INSTRUCCIONES[avatar_class.instruccion_actual]['time'])
            else:
                dm.set_time(INSTRUCCIONES[0]['time'])

        self.tiempo_transcurrido_por_instruccion = time.time()


dm = Deteccion_movimiento(0, Proceso_deteccion_movimiento)


# Decoradores


class Cardholder(object):
    def __init__(self, name):
        self.name = name

    def __call__(self, f):
        def none(*args, **kw_args):
            print(self.name)
            rta = f(*args, **kw_args)
            scan_beacon.terminar_procesos_beacon()
            return rta

        return none


class Mqtt(object):
    def __init__(self, name):
        self.name = name

    def __call__(self, f):
        def none(*args, **kw_args):
            print(self.name)
            MatricularFuncionRecibidoMQTT(Orden_mqtt_recibida())
            IniciarEscuchaMQTT()
            rta = f(*args, **kw_args)
            FinalizarEscuchaMQTT()
            return rta

        return none


class Manitor(object):
    def __init__(self, name):
        self.name = name

    def __call__(self, f):
        def none(*args, **kw_args):
            print(self.name)
            rta = f(*args, **kw_args)
            dm.cerrar_camara()
            cv2.destroyAllWindows()
            return rta

        return none


class Avatar(object):
    def __init__(self, name):
        self.name = name

    def __call__(self, f):
        def none(*args, **kw_args):
            print(self.name)
            avatar_class.iniciar_avatar()
            rta = f(*args, **kw_args)
            avatar_class.cerrar_avatar()
            return rta

        return none


class Sound(object):
    def __init__(self, name):
        self.name = name

    def __call__(self, f):
        def none(*args, **kw_args):
            print(self.name)
            iniciar_sounds(PATH_VIDEOS)
            rta = f(*args, **kw_args)
            return rta

        return none


# Fin decoradores


@Sound("sound manitor")
@Manitor("Manitor WISROVI")
@Cardholder("cardholder manitor")
@Mqtt("mqtt manitor")
@Avatar("avatar manitor")
def main():
    global chrono_beacon_scan
    global PRIMER_CARDHOLDER
    global actual_cardholder

    while True:
        frame = dm.proceso_completo()
        black_screen, video_inicial_final = avatar_class.proceso()
        if avatar_class.get_primer_inicio_avatar():
            if abs(chrono_beacon_scan - currentTime()) >= TIME_SCAN_BEACON:
                chrono_beacon_scan = currentTime()

                LAST_BEACON = scan_beacon.get_scan_actual()
                if not LAST_BEACON[0]:
                    print("No hay cardholder")
                    dm.terminar_proceso_deteccion_movimiento()
                    PRIMER_CARDHOLDER = False
                    actual_cardholder = ""
                else:
                    if not PRIMER_CARDHOLDER:
                        encontrado_ultimo_registro_tiempo_cumplido = True
                        for key, value in historial_personas.items():
                            if LAST_BEACON[1].__eq__(key):
                                if abs(currentTime() - value) <= TIEMPO_VOLVER_LAVAR_MANOS:
                                    encontrado_ultimo_registro_tiempo_cumplido = False
                                break

                        if encontrado_ultimo_registro_tiempo_cumplido:
                            if MINIMA_DISTANCIA_RSSI < LAST_BEACON[2]:
                                print("Nuevo cardholder:", LAST_BEACON[1], LAST_BEACON[2])
                                PRIMER_CARDHOLDER = True
                                dm.iniciar_proceso_deteccion_movimiento()
                            else:
                                print("Cardholder muy lejano, no valido para el proceso de MANITOR")
                        else:
                            print("Este cardholder aún no cumple el tiempo restrictivo para lavarse las manos")
                    else:
                        actual_cardholder = LAST_BEACON[1]
                        # print("Repetido cardholder:", LAST_BEACON[1], LAST_BEACON[2])
                        pass
        else:
            chrono_beacon_scan = currentTime()

        cv2.imshow("Frame", black_screen)
        if avatar_class.get_primer_inicio_avatar():
            if PRIMER_CARDHOLDER:
                # cv2.imshow("frame_camara", frame)
                pass
        # time.sleep(0.025)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break


if __name__ == "__main__":
    main()
