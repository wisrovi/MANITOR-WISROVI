import datetime


def Leer_HoraActual():
    x = datetime.datetime.now()
    return "{}/{}/{}".format(x.day, x.month, x.year) + "-" + "{}:{}:{}".format(x.hour, x.minute, x.second)


BROQUER_MQTT = "100.24.61.248"
PORT_MQTT = 1883
USER = "analitica"
PWD = "welcome1"

import paho.mqtt.client as mqtt  # import the client1

credenciales = {
    "": "",
    "": ""
}

client = mqtt.Client("python1", transport="tcp")  # , userdata=credenciales)             #create new instance
client.connect(host=BROQUER_MQTT, port=PORT_MQTT)  # connect to broker
