from Config.movimiento_frente_camara import TIEMPO_POR_INSTRUCCION, TIEMPO_AVISO_NO_MOVIMIENTO
from Util.util import currentTime

if __name__ == "__main__":
    chrono_siguiente_instruccion = currentTime()
    chrono_conteo_movimiento = currentTime()
    chrono_conteo_NO_movimiento = currentTime()

    while (1):
        hay_movimiento_segun_cambio_areas = True
        if True:
            if hay_movimiento_segun_cambio_areas:
                status_lavado_manos_activo = True
                print(".", end="")
                if abs(chrono_siguiente_instruccion - chrono_conteo_movimiento) < TIEMPO_POR_INSTRUCCION:
                    chrono_conteo_movimiento = currentTime()
                    chrono_conteo_NO_movimiento = currentTime()
                else:
                    chrono_siguiente_instruccion = currentTime()
                    print("")
                    print("Instruccion superada, paso a la siguiente instruccion")
            else:
                if status_lavado_manos_activo:
                    chrono_siguiente_instruccion = currentTime()
                    status_lavado_manos_activo = False

                print("*", end="")
                if abs(chrono_siguiente_instruccion - chrono_conteo_NO_movimiento) < TIEMPO_AVISO_NO_MOVIMIENTO:
                    chrono_conteo_NO_movimiento = currentTime()
                else:
                    chrono_siguiente_instruccion = currentTime()
                    print("")
                    print("Por favor mueva mas las manos, para validar la instruccion")
