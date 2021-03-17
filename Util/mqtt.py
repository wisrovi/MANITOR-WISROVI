from Config.broker_mqtt import BROKER_MQTT, PORT_MQTT

from Config.Constantes.topic_subscribirse_mqtt import PROJECT, TOPICS_USAR
from Util.util import Get_MAC

IDENTIFICADOR_MANITOR = Get_MAC()

import paho.mqtt.client as mqtt

client = mqtt.Client(IDENTIFICADOR_MANITOR)  # create new instance

try:
    client.connect(host=BROKER_MQTT, port=PORT_MQTT)  # , keepalive=60, bind_address="") #connect to broker
except:
    print("Error al conectarse al broker de MQTT")


def EnviarDatoServidor(TOPIC_PUBLISH_MQTT, MENSAJE_ENVIAR_MQTT):
    client.publish(TOPIC_PUBLISH_MQTT, MENSAJE_ENVIAR_MQTT)  # publish


def SuscribirTopic(topic):
    client.subscribe(topic)


orden_mqtt = None


def on_message(client, userdata, message):
    topico = message.topic
    topico = topico.replace(PROJECT, "")
    mensaje = str(message.payload.decode("utf-8"))

    OTA = False
    if topico.find("OTA") >= 0:
        OTA = True

    RESTART = False
    if topico.find("restart") >= 0:
        RESTART = True

    if topico.find(Get_MAC()) >= 0:
        if OTA:
            orden_mqtt.private_ota()
        elif RESTART:
            orden_mqtt.private_restart()
    else:
        if OTA:
            orden_mqtt.public_ota()
        elif RESTART:
            orden_mqtt.public_restart()


def MatricularFuncionRecibidoMQTT(clase_ejecutar):
    global orden_mqtt
    orden_mqtt = clase_ejecutar
    client.on_message = on_message


def GetClientConectionMQTT():
    return client


def IniciarEscuchaMQTT():
    client.loop_start()


def FinalizarEscuchaMQTT():
    client.loop_stop()  # stop the loop


for topic in TOPICS_USAR:
    SuscribirTopic(topic)
    print("Suscrito a:", topic)
