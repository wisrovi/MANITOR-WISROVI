import cv2

# **********************************************************
import numpy as np
def ColorAzul():
    black_screen  = np.zeros([500,500,3], dtype=np.uint8)

    black_screen[:,:,0] = np.ones([500,500])*255
    black_screen[:,:,1] = np.ones([500,500])*0
    black_screen[:,:,2] = np.ones([500,500])*0

    return black_screen
def ColorRojo():
    black_screen  = np.zeros([500, 500,3], dtype=np.uint8)

    black_screen[:,:,0] = np.ones([500,500])*0
    black_screen[:,:,1] = np.ones([500,500])*0
    black_screen[:,:,2] = np.ones([500,500])*255

    return black_screen
hay_movimiento_segun_cambio_areas = False
def back(*args):
    global hay_movimiento_segun_cambio_areas
    global proceso_iniciado
    if hay_movimiento_segun_cambio_areas:
        hay_movimiento_segun_cambio_areas = False
    else:
        hay_movimiento_segun_cambio_areas = True

    if not proceso_iniciado and estado:
        proceso_iniciado = True
cv2.namedWindow("Frame")
cv2.createButton("Change Color", back)
# **********************************************************
from time import strftime
import time
def currentTime(): # Obtain current time in seconds
    now=strftime("%H,%M,%S")
    (h,m,s) = now.split(',')
    currentTime = int(h)*3600+int(m)*60+int(s)
    return currentTime
# **********************************************************



TIEMPO_POR_INSTRUCCION = 10

INSTRUCCIONES = list()
INSTRUCCIONES.append("enjabonece")
INSTRUCCIONES.append("frote dedos")
INSTRUCCIONES.append("frote pulgares")
INSTRUCCIONES.append("palma con palma")
INSTRUCCIONES.append("uñas")


chrono_siguiente_instruccion = currentTime()
chrono_conteo_movimiento = currentTime()
chrono_conteo_NO_movimiento = currentTime()


def MostrarVideo(i, frame):
    if i == 0:
        print("Bienvenido al MANITOR, le voy a guiar en los pasos del lavado de manos")
        time.sleep(TIEMPO_POR_INSTRUCCION/2)

    if i >= len(INSTRUCCIONES):
        print("Felicidades, ha superado todos los pasos del lavado de manos")
    else:
        print("Instruccion superada, paso a la siguiente instruccion: {}".format( INSTRUCCIONES[instruccion_actual] ))

    return frame

def IndicarPreaviso(i):
    if i==0:
        print("Primer preaviso: por favor mueva las manos siguiendo la instruccion dada")
    elif i==1:
        print("Segundo preaviso: por favor mueva las manos siguiendo la instruccion dada")
    elif i==2:
        print("Tercer preaviso: por favor mueva las manos siguiendo la instruccion dada")
    else:
        print("Tu lavado de manos no ha sido exitoso, intentalo nuevamente")


contador_cambio_estado = 0
estado = False
proceso_iniciado = True
instruccion_actual = 0

# **********************************************************
if __name__ == "__main__":

    while True:
        start_time = time.time()
        frame  = ColorAzul() if hay_movimiento_segun_cambio_areas else ColorRojo()
        cv2.putText(frame,"Hay movimiento" if hay_movimiento_segun_cambio_areas else "No hay movimiento",(50,60),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,255,255),2,cv2.LINE_AA)
        # **********************************************************

        #frame = Monitoreo_Control_Tiempos_e_Instruccion(frame)

        valor_cambio=150
        if proceso_iniciado:
            if hay_movimiento_segun_cambio_areas:
                if estado:
                    contador_cambio_estado = 0 # Reinicio contador cambio estado
                else:
                    contador_cambio_estado = contador_cambio_estado + 1
                    if contador_cambio_estado > (valor_cambio/3):
                        estado = True
                        chrono_siguiente_instruccion = currentTime()
                        chrono_conteo_movimiento = currentTime()
                        instruccion_actual = 0
                        frame = MostrarVideo(instruccion_actual, frame)
                        instruccion_actual = 1

                if estado:
                    if abs(chrono_siguiente_instruccion - chrono_conteo_movimiento)>=TIEMPO_POR_INSTRUCCION:
                        frame = MostrarVideo(instruccion_actual, frame)
                        chrono_siguiente_instruccion = currentTime()
                        chrono_conteo_movimiento = currentTime()

                        if instruccion_actual >= len(INSTRUCCIONES):
                            instruccion_actual = 0
                            proceso_iniciado = False
                        instruccion_actual = instruccion_actual + 1
                    else:
                        chrono_conteo_movimiento = currentTime()
            else:
                if estado:
                    contador_cambio_estado = contador_cambio_estado + 1
                    if contador_cambio_estado == int(1*(valor_cambio/4)):
                        IndicarPreaviso(0)

                    if contador_cambio_estado == int(2*(valor_cambio/4)):
                        IndicarPreaviso(1)

                    if contador_cambio_estado == int(3*(valor_cambio/4)):
                        IndicarPreaviso(2)

                    if contador_cambio_estado >= int(4*(valor_cambio/4)):
                        estado = False
                        instruccion_actual = 0
                        chrono_siguiente_instruccion = currentTime()
                        chrono_conteo_NO_movimiento = currentTime()
                else:
                    contador_cambio_estado = 0 # Reinicio contador cambio estado

                if not estado:
                    if abs(chrono_siguiente_instruccion - chrono_conteo_NO_movimiento)>5:
                        IndicarPreaviso(3)
                        chrono_siguiente_instruccion = currentTime()
                        proceso_iniciado = False
                    else:
                        chrono_conteo_NO_movimiento = currentTime()

        # **********************************************************
        time.sleep(0.040)
        txt = str(int( (time.time()-start_time)*1000 )) + "ms"
        cv2.putText(frame,str(txt),(420,470),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,255,255),2,cv2.LINE_AA)
        cv2.imshow('Frame', frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
        #print("Time:", txt)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


