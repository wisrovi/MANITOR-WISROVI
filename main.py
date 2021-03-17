import cv2
import time

from Config.avatar import AVATAR
from Util.util import FrameSinRuido, currentTime
from Config.time_validation_pose import TIEMPO_POR_INSTRUCCION, TIEMPO_ESCANEO_BEACON
from Config.videos_manitor import INSTRUCCIONES, PATH_VIDEOS, LIENZO_MOSTRAR_VIDEOS
from Util.mqtt import Get_MAC, EnviarDatoServidor, Leer_HoraActual, SuscribirTopic, MatricularFuncionRecibidoMQTT, GetClientConectionMQTT
from Config.Constantes.topic_subscribirse_mqtt import TOPICS_USAR
from Util.functions_image import CalcularNuevaDimension, CrearFondoPonerVideos


# ******************** proceso de escaneo de beacon ************************************
if True:
    import numpy as np
    from beacontools import BeaconScanner, IBeaconAdvertisement
    size_vector = 10
    FCV = "00706786" # http://1.bp.blogspot.com/-gTya0k5EPtY/UlsYUkVM-HI/AAAAAAAAAIg/YeMEivnolAY/s1600/IMAGEN13.jpg

    def vector_vacio():
        return [int(i) for i in list( np.zeros(size_vector) )]

    BEACONs_SCANNED = dict()
    HISTORY_BEACON_SCAN = dict()
    HISTORY_MORE_NEAR_BEACON = vector_vacio()
    there_is_caldholder = False

    class Beacon_Obj(object):
        mac = str()
        rssi = int()
        uuid = str()
        tx_power = int()
        major = int()
        minor = int()

        def __init__(self, mac:str, rssi:int, uuid:str, tx:int, maj:int, min:int):
            self.mac = mac
            self.rssi = rssi
            self.uuid = uuid
            self.tx_power = tx
            self.major = maj
            self.minor = min

        def getJson(self):
            return self.__dict__

    def callback(bt_addr, rssi, packet, additional_info):
        mac_scan = bt_addr
        rssi_scan = rssi
        uuid = packet.uuid
        tx_po = packet.tx_power
        maj = packet.major
        min = packet.minor

        empresa = uuid[0:8]
        if empresa == FCV:
            b = Beacon_Obj(mac_scan, rssi_scan, uuid, tx_po, maj, min)
            BEACONs_SCANNED[uuid] = b

    # scan for all iBeacon advertisements regardless from which beacon
    scanner = BeaconScanner(callback, packet_filter=IBeaconAdvertisement)

    def diff(list1, list2): 
        c = set(list1).union(set(list2)) # or c = set(list1) | set(list2) 
        d = set(list1).intersection(set(list2)) # or d = set(list1) & set(list2) 
        return list(c - d)

    def process_scan_beacon():
        global BEACONs_SCANNED
        global HISTORY_BEACON_SCAN
        global HISTORY_MORE_NEAR_BEACON
        global there_is_caldholder

        mas_cercano = { 'k' : "", 'rssi' : -150 }
        beacons_encontrados = list()
        for k, v in BEACONs_SCANNED.items():
            if not v.uuid in HISTORY_BEACON_SCAN:
                HISTORY_BEACON_SCAN[v.uuid] = {'beacon':v, 'history':vector_vacio() }
            historico = HISTORY_BEACON_SCAN[v.uuid]['history']
            for i in range(size_vector-1,0,-1):
                historico[i] = historico[i-1]
            historico[0] = v.rssi
            HISTORY_BEACON_SCAN[v.uuid]['history'] = historico
            beacons_encontrados.append(v.uuid)
            if mas_cercano['rssi'] < v.rssi:
                mas_cercano['rssi'], mas_cercano['k'] = v.rssi, v.uuid
        todos_beacons = [k for k in HISTORY_BEACON_SCAN]

        for k in diff(todos_beacons, beacons_encontrados):
            historico = HISTORY_BEACON_SCAN[k]['history']
            for i in range(size_vector-1,0,-1):
                historico[i] = historico[i-1]
            historico[0] = 0
            HISTORY_BEACON_SCAN[k]['history'] = historico
        BEACONs_SCANNED = dict()

        for i in range(size_vector-1,0,-1):
            HISTORY_MORE_NEAR_BEACON[i] = HISTORY_MORE_NEAR_BEACON[i - 1]
        HISTORY_MORE_NEAR_BEACON[0] = mas_cercano

    scanner.start()

# **************************************************************************************












last_areas = list()
def hallar_contornos_areas(frame, masking, constante = 500):
    global last_areas

    thresh = cv2.threshold(masking, 25,255, cv2.THRESH_BINARY)[1]   # (masking,127,255,   0) # Aplicamos un umbral para quitar ruido
    thresh = cv2.dilate(thresh, None, iterations=2) # Dilatamos el umbral para tapar agujeros

    contornos = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0] # CHAIN_APPROX_SIMPLE: deja solo los contornos externos obviando los internos (ahorrar memoria y aumentar velocidad computo)

    cajas = list()
    areas = list()
    contornos_finales = list()
    for c in contornos:                 # Recorremos todos los contornos encontrados
        if cv2.contourArea(c) < constante:    # Eliminamos los contornos mas pequenos
            continue
        (x, y, w, h) = cv2.boundingRect(c) # Obtenemos el bounds del contorno, el rectángulo mayor que engloba al contorno
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cajas.append((x,y,x+w,y+h))
        contornos_finales.append(c)

        area = w*h
        areas.append(area)

    cv2.drawContours(frame, contornos_finales, -1, (255,0,0), 3)

    # Determinar movimiento de acuerdo a el cambio de areas (superior a una constante definida) en objeto(s) en la escena
    hay_movimiento_segun_cambio_areas = False
    if len(last_areas) == len(areas):        # if exist(True) in list(  if abs(valor)>constante*1.5 => valor = resta(last_areas, areas)  )
        hay_movimiento_segun_cambio_areas = True if True in [True if i>constante*1.5 else False for i in [abs(i) for i in [e1 - e2 for e1, e2 in zip(last_areas,areas)]]] else False
    else:
        hay_movimiento_segun_cambio_areas = True
        pass
    last_areas = areas

    return cajas, areas, hay_movimiento_segun_cambio_areas











cap = cv2.VideoCapture(0)











# **************** Control estado actual instruccion a seguir *****************
contador_cambio_estado = 0
estado = False
proceso_iniciado = True
instruccion_actual = -1
def MostrarVideo(i, frame):
    if i == 0:
        print("Bienvenido al MANITOR, le voy a guiar en los pasos del lavado de manos")
    else:
        if i > 0:
            if i >= len(INSTRUCCIONES):
                print("Felicidades, ha superado todos los pasos del lavado de manos")
            else:
                print("Instruccion superada, paso a la siguiente instruccion: {}".format( INSTRUCCIONES[instruccion_actual] ))
        else:
            print("Sistema iniciado")

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












# ****************************************** MQTT *******************************************
for topic in TOPICS_USAR:                                                                # **
    SuscribirTopic(topic)                                                                # **
    print("Suscrito a:", topic)                                                          # **
                                                                                         # **
def on_message(client, userdata, message):                                               # **
    print("*************************")                                                   # **
    print("Recibiendo Manitor:")                                                         # **
    mensaje = message.topic + ": " + str(message.payload.decode("utf-8"))                # **
    print(mensaje)                                                                       # **
    print("*************************")                                                   # **
                                                                                         # **
MatricularFuncionRecibidoMQTT(on_message)                                                # **
client_mqtt = GetClientConectionMQTT()                                                   # **
client_mqtt.loop_start()                                                                 # **
def EnviarNotificacionLavadoManosCompleto():
    mac = Get_MAC()
    bateria = uuid_que_inicia_proceso[14:18]
    topic = "/SPINPLM/manitor/" + mac + "/" + uuid_que_inicia_proceso
    print("Topic:", topic)

    msg = "{" + "'LV' : " + bateria + ", 'HOUR': " + Leer_HoraActual() + ", 'mac' : " + mac + "}"

    EnviarDatoServidor(topic, msg)
    print("Enviando notificacion al servidor (MQTT) usuario se lavo correctamente las manos, uuid:", uuid_que_inicia_proceso)
# *******************************************************************************************









def ProcesoCambioInstruccionParaUsuario():
    global there_is_caldholder
    global uuid_que_inicia_proceso

    if instruccion_actual >= len(INSTRUCCIONES):
        # Si se cumplen todos los pasos y ademas el cardholder (que representa la persona) es la misma que inicio el proceso de lavado de manos, entonces se reporta al server:
        # esta persona con uuid se lavo correctamente las manos (correcta = se movio durante el proceso, confiando que estaba moviendose según se lo indicaba el avatar)
        for r in HISTORY_MORE_NEAR_BEACON:
            if len(r['k']) > 0:
                if uuid_que_inicia_proceso == r['k']:
                    EnviarNotificacionLavadoManosCompleto()
                break
        # desactivar el proceso del MANITOR hasta que un nuevo Beacon aparezca en cercania

        time.sleep(TIEMPO_POR_INSTRUCCION)

        print("Reiniciando bucle")
        there_is_caldholder = False
    else:
        # Validacion que el cardholder siga en frente indicando que la persona esta lavandose las manos
        if True:
            if len(uuid_que_inicia_proceso) > 0:
                for r in HISTORY_MORE_NEAR_BEACON:
                    if r != 0:
                        if len(r['k']) > 0:
                            if uuid_que_inicia_proceso != r['k']:
                                there_is_caldholder = False
                                print(uuid_que_inicia_proceso, r['k'])
                                print("[Alerta]: La persona más cercana al MANITOR no es la misma persona que inicio el proceso de lavado de manos.")
                                break
            else:
                uuid_que_inicia_proceso = HISTORY_MORE_NEAR_BEACON[0]['k']










if __name__ == "__main__":
    chrono_siguiente_instruccion = currentTime()
    chrono_conteo_movimiento = currentTime()
    chrono_conteo_NO_movimiento = currentTime()

    chrono_beacon = currentTime()
    uuid_que_inicia_proceso = str()

    proceso = False # True=Camara, False=Bluetooth
    existe_primer_movimiento = False

    ultimo_video_mostrar = len(INSTRUCCIONES)

    nuevo_video_instruccion_mostrar = False
    frame_video_instruccion_mostrar = None

    # Mostrar videos y avatar
    video_instructivo_mostrar = "Objeto donde se guardaran los videos a mostrar, mas adelante se cambia al tipo de variable: cv2.VideoCapture('path')"
    avatar = "Objeto donde se guardaran los videos a mostrar, mas adelante se cambia al tipo de variable: cv2.VideoCapture('path')"
    instruccion_actual = 0
    path_video_actual = None
    hay_video_mostrar = False
    avatar_inicio = True
    avatar = cv2.VideoCapture(PATH_VIDEOS + "/" + AVATAR['START'])
    multiplexor_avatar = True

    while(1):
        black_screen  = CrearFondoPonerVideos()
        frame, _, _, masking = FrameSinRuido(cap)




        # Proceso escaneos de Beacons (se repite cada 'TIEMPO_ESCANEO_BEACON' segundos)
        if not avatar_inicio:
            if (currentTime()-chrono_beacon) >= TIEMPO_ESCANEO_BEACON:
                chrono_beacon = currentTime()
                process_scan_beacon()

                if False:
                    # imprimir el historial de los beacons escaneados
                    for k,v in HISTORY_BEACON_SCAN.items():
                        print(k, v['history'])

                if len(HISTORY_MORE_NEAR_BEACON[0]['k']) > 0:
                    # Cuando un cardholder (persona) se acerque al MANITOR se inicia el proceso de lavado de manos guiado
                    if not proceso:
                        proceso = True
                        proceso_iniciado = True
                        estado = True
                    there_is_caldholder = True
                else:
                    there_is_caldholder = False
                    # print("No hay cardholder cercanos")





        # Proceso mostrar video
        if avatar_inicio:
            avatar_inicio, frame_avatar = avatar.read()
            if avatar_inicio:
                black_screen = cv2.resize(frame_avatar, (LIENZO_MOSTRAR_VIDEOS[1], LIENZO_MOSTRAR_VIDEOS[0]))
            else:
                avatar = cv2.VideoCapture(PATH_VIDEOS + "/" + AVATAR['BAS1'])
                chrono_siguiente_instruccion = currentTime()
        else:
            if hay_video_mostrar:
                hay_video_mostrar, frame_video_instruccion_mostrar = video_instructivo_mostrar.read()
                if hay_video_mostrar:
                    dimen = CalcularNuevaDimension(frame_video_instruccion_mostrar.shape, 0.7)
                    if dimen is not None:
                        frame_video_instruccion_mostrar = cv2.resize(frame_video_instruccion_mostrar, (0, 0), fx=dimen, fy=dimen)

                        origen_x = int(black_screen.shape[0] - frame_video_instruccion_mostrar.shape[0])
                        origen_x = origen_x - 50 if origen_x >= 50 else int(
                            (black_screen.shape[0] - frame_video_instruccion_mostrar.shape[0]) / 2)
                        origen_y = int((black_screen.shape[1] - frame_video_instruccion_mostrar.shape[1]) / 2)

                        black_screen[origen_x:frame_video_instruccion_mostrar.shape[0] + origen_x, origen_y:frame_video_instruccion_mostrar.shape[1] + origen_y] = frame_video_instruccion_mostrar
                else:
                    chrono_siguiente_instruccion = currentTime()
            else:
                hay_avatar, frame_avatar = avatar.read()
                if hay_avatar:
                    frame_avatar = cv2.resize(frame_avatar, (LIENZO_MOSTRAR_VIDEOS[1], LIENZO_MOSTRAR_VIDEOS[0]))
                    black_screen = frame_avatar
                else:
                    multiplexor_avatar = False if multiplexor_avatar else True
                    avatar = cv2.VideoCapture(
                        PATH_VIDEOS + "/" + AVATAR['BAS1']) if multiplexor_avatar else cv2.VideoCapture(
                        PATH_VIDEOS + "/" + AVATAR['BAS2'])






        # Proceso deteccion movimiento de manos
        if not avatar_inicio:
            if proceso:
                # ************ Proceso camara
                time_start = time.time()
                next = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                constante_cambio_area = 1000 # constante de cambio de area, entre mayor sea el numero, mayor es el area a detectar para cambio, es decir el equivalente a la velocidad de movimiento
                cajas, areas, hay_movimiento_segun_cambio_areas = hallar_contornos_areas(frame, masking, constante_cambio_area)

                if False:
                    # Impresion de resultados de movimiento detectado
                    cv2.putText(frame,'Movimiento por:',(30,30),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,255),2,cv2.LINE_AA)
                    if hay_movimiento_segun_cambio_areas:
                        cv2.circle(frame,(35,54),10,(255,0,255),-1)
                        cv2.putText(frame,'Cambio Area',(50,60),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,255,255),2,cv2.LINE_AA)

                valor_cambio=150 # Constante incremental para cambio de estado [Lavandose_manos, Persona_ausente_o_sin_movimiento]
                if proceso_iniciado:
                    if hay_movimiento_segun_cambio_areas:
                        if not existe_primer_movimiento:
                            existe_primer_movimiento = True

                        if estado:
                            contador_cambio_estado = 0 # Reinicio contador cambio estado
                        else:
                            contador_cambio_estado = contador_cambio_estado + 1
                            if contador_cambio_estado > (valor_cambio/3):
                                estado = True
                                chrono_siguiente_instruccion = currentTime()
                                chrono_conteo_movimiento = currentTime()
                                if HISTORY_MORE_NEAR_BEACON[0] != 0:
                                    uuid_que_inicia_proceso = HISTORY_MORE_NEAR_BEACON[0]
                                    # print("Asignando uuid persona que inicia el proceso")
                                    instruccion_actual = 0

                        if estado:
                            # Validamos si ya paso el tiempo 'TIEMPO_POR_INSTRUCCION' para continuar a la siguiente instrucción
                            if abs(chrono_siguiente_instruccion - chrono_conteo_movimiento) >= TIEMPO_POR_INSTRUCCION:
                                chrono_siguiente_instruccion = currentTime()
                                chrono_conteo_movimiento = currentTime()
                                ProcesoCambioInstruccionParaUsuario()

                                path_video_actual = INSTRUCCIONES[instruccion_actual]['path']
                                path_video_actual = PATH_VIDEOS + "/" + path_video_actual
                                print("nuevo video:", path_video_actual)
                                try:
                                    video_instructivo_mostrar = cv2.VideoCapture(path_video_actual)
                                    hay_video_mostrar = True
                                except:
                                    hay_video_mostrar = False
                                instruccion_actual = instruccion_actual + 1
                                if instruccion_actual >= len(INSTRUCCIONES):
                                    instruccion_actual = 0
                                    avatar = cv2.VideoCapture(PATH_VIDEOS + "/" + AVATAR['END'])
                                    avatar_inicio = True

                            else:
                                chrono_conteo_movimiento = currentTime()
                    else:
                        if existe_primer_movimiento:
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

                                    chrono_siguiente_instruccion = currentTime()
                                    chrono_conteo_NO_movimiento = currentTime()
                            else:
                                contador_cambio_estado = 0 # Reinicio contador cambio estado

                        # Si la persona dejo de moverse o ya no está frente a la camara reinicio el proceso
                        if not estado:
                            if abs(chrono_siguiente_instruccion - chrono_conteo_NO_movimiento)>5:
                                IndicarPreaviso(3)
                                chrono_siguiente_instruccion = currentTime()

                                estado = False
                                proceso = False
                                proceso_iniciado = False
                                existe_primer_movimiento = False
                                instruccion_actual = 0

                                chrono_conteo_movimiento = currentTime()
                                chrono_siguiente_instruccion = currentTime()

                            else:
                                chrono_conteo_NO_movimiento = currentTime()

                    # Apenas la persona se retire de la cercania del MANITOR se interrumpe el proceso de lavado de manos
                    if not there_is_caldholder:
                        proceso = False
                        proceso_iniciado = False
                        estado = False
                        instruccion_actual = 0
                        if existe_primer_movimiento:
                            print("[Alerta]: La persona se ha retirado del MANITOR, el proceso no continua.")
                        uuid_que_inicia_proceso = ""
                        existe_primer_movimiento = False
                        continue


        if not avatar_inicio:
            font = cv2.FONT_HERSHEY_SIMPLEX
            org = (50, 50)
            fontScale = 1
            color = (255, 0, 0)  # BLue
            thickness = 2  # Line thickness
            black_screen = cv2.putText(black_screen, INSTRUCCIONES[instruccion_actual]['name'], org, font, fontScale,
                                       color,
                                       thickness, cv2.LINE_AA)

        # mostramos en pantalla el uuid de la persona mas cercana al MANITOR
        if HISTORY_MORE_NEAR_BEACON[0] != 0:
            cv2.putText(frame, HISTORY_MORE_NEAR_BEACON[0]['k'], (30, 430), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.imshow("frame", frame) if frame is not None else print("Error abrir camara")

        cv2.imshow("black_screen", black_screen)
        # cv2.imshow("frame_original", frame_original)
        # cv2.imshow("masking", masking)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break


    cap.release()
    cv2.destroyAllWindows()

    scanner.stop()