








from config.BROKER_CONECTION import BROKER_MQTT,  PORT_MQTT





from config.BALIZAs import ALL_MACs_BALIZA
from config.CARHOLDERs import ALL_CARD_HOLDER
from config.general import PROJECT


import random
import datetime
import paho.mqtt.client as mqtt

def Manitor_aleatorio():
    return random.choice(ALL_MACs_BALIZA)

def CardHolder_aleatorio():
    return random.choice(ALL_CARD_HOLDER)

def Generar_nivel_bateria_aleatorio():
    min_bateria = 2.2
    max_bateria = 4.0
    return str(int(random.uniform(min_bateria, max_bateria) * 100) / 100)


TOPIC_BASE = "/" + PROJECT
mac_usar = Manitor_aleatorio()


TOPIC_PUBLISH_MQTT = TOPIC_BASE + "/baliza/" + mac_usar + "/" + CardHolder_aleatorio()
MENSAJE_ENVIAR_MQTT="{ 'LV' : " + Generar_nivel_bateria_aleatorio() + ", 'mac': " + mac_usar +"}"
IDENTIFICADOR_MANITOR = mac_usar.replace(":","") # Debe ser unico y no se puede repetir en todo el broker
client = mqtt.Client(IDENTIFICADOR_MANITOR) #create new instance
client.connect(host=BROKER_MQTT, port=PORT_MQTT) #, keepalive=60, bind_address="") #connect to broker






from tkinter import *
window = Tk()
window.title("Baliza")
window.geometry('380x180')
Label(window, text="MAC:" + mac_usar, font=("Arial Bold", 20)).grid(column=0, row=0)
recibido_mqtt = Label(window, font=("Arial", 12), text = "Recibiendo...")
recibido_mqtt.grid(column=0, row=2)
def clic_restart_global():
    topic = TOPIC_BASE+ "/baliza/"+mac_usar+"/"+CardHolder_aleatorio()
    msg = "{ 'LV' : " + Generar_nivel_bateria_aleatorio() + ", 'mac': " + mac_usar +"}"
    print("G:restart:", topic)
    client.publish(topic,msg)#publish
Button(window, text="Send CardHolder", command=clic_restart_global).grid(column=0, row=4)



def Enviar_Dato_MQTT():
    print("##################################")
    print("# BALIZA ENVIA:")
    print("Topic:",TOPIC_PUBLISH_MQTT)
    print("Msg:",MENSAJE_ENVIAR_MQTT)
    print("##################################")
    client.publish(TOPIC_PUBLISH_MQTT,MENSAJE_ENVIAR_MQTT)#publish




# imprimir cada mensaje recibido
def on_message(client, userdata, message):
    print("*************************")
    print("Recibiendo Baliza:")
    mensaje = message.topic + ": " + str(message.payload.decode("utf-8"))
    print(mensaje)
    print("*************************")
    recibido_mqtt['text'] = mensaje

client.on_message = on_message

TOPICS_USAR = list()
TOPICS_USAR.append(TOPIC_BASE + "/OTA")
TOPICS_USAR.append(TOPIC_BASE+"/" +mac_usar+"/" + "OTA")
TOPICS_USAR.append(TOPIC_BASE + "/restart")
TOPICS_USAR.append(TOPIC_BASE+"/" +mac_usar+"/" + "restart")
TOPICS_USAR.append(TOPIC_BASE+"/" +mac_usar+"/" + "Alarma")

for topic in TOPICS_USAR:
    client.subscribe(topic)
    print("Suscrito a:", topic)

client.loop_start()





window.mainloop()



import time
TIEMPO_INTERVALO_ENVIAR = 5
while 1:
    time.sleep(TIEMPO_INTERVALO_ENVIAR)
    Enviar_Dato_MQTT()