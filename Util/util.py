from Config.movimiento_frente_camara import TIEMPO_POR_INSTRUCCION
from Util.functions_image import LeerFotograma, CrearMascara, QuitarPartesNoMarcadasEnMascara
from time import strftime
import time


def FrameSinRuido(self, cap):
    # ********* Paso 1: Leo el fotograma de la camara
    frame = LeerFotograma(cap)

    # ********* Paso 2: Detecto el color piel y el resto de colores los elimino dejando una mascara con blanco (color de interes) y negro (otros colores)
    masking, punto_elegido = CrearMascara(frame)

    # ********* Paso 3: tomo la imagen original y le aplico la mascara, para tener la imagen original sin los colores NO deseados    
    new_img = QuitarPartesNoMarcadasEnMascara(frame, masking)
    return new_img, punto_elegido, frame, masking

def currentTime(): # Obtain current time in seconds
    now=strftime("%H,%M,%S")
    (h,m,s) = now.split(',')
    currentTime = int(h)*3600+int(m)*60+int(s)
    return currentTime



import getmac
mac = getmac.get_mac_address()
def Get_MAC():
    return mac


import datetime
def Leer_HoraActual():
    x = datetime.datetime.now()
    return "{}/{}/{}".format(x.day, x.month, x.year) + "-" + "{}:{}:{}".format(x.hour, x.minute, x.second)


def diff(list1, list2):
    c = set(list1).union(set(list2))  # or c = set(list1) | set(list2)
    d = set(list1).intersection(set(list2))  # or d = set(list1) & set(list2)
    return list(c - d)


import numpy as np
def vector_vacio(size_vector):
    return [int(i) for i in list(np.zeros(size_vector))]



if __name__ == "__main__":
    chrono_siguiente_instruccion = currentTime()
    chrono_aux = currentTime()
    while(abs(chrono_siguiente_instruccion - chrono_aux) < TIEMPO_POR_INSTRUCCION):
        time.sleep(0.5)
        chrono_aux = currentTime()

    print( "Tiempo terminado" )