from config.BROKER_CONECTION import BROKER_MQTT,  PORT_MQTT
IDENTIFICADOR_SERVER = "SERVER" # Debe ser unico y no se puede repetir en todo el broker









from config.BALIZAs import ALL_MACs_BALIZA
from config.MANITORs import ALL_MACs_MANITOR
from config.CARHOLDERs import ALL_CARD_HOLDER
from config.general import PROJECT

def Generar_lista_suscripciones():
    listado_suscripcion_manitor = list()
    for MAN in ALL_MACs_MANITOR:
        topic = "/" + PROJECT + "/" + "manitor" + "/" + MAN + "/" + "#"
        listado_suscripcion_manitor.append(topic)
    
    listado_suscripcion_baliza = list()
    for BAL in ALL_MACs_BALIZA:
        topic = "/" + PROJECT + "/" + "baliza" + "/" + BAL + "/" + "#"
        listado_suscripcion_baliza.append(topic)

    return listado_suscripcion_manitor + listado_suscripcion_baliza

import paho.mqtt.client as mqtt

TOPIC_SUSBCRIBE_MQTT = Generar_lista_suscripciones()
#print(TOPIC_SUSBCRIBE_MQTT)



# imprimir cada mensaje recibido
def on_message(client, userdata, message):
    print("*************************")
    print(message.topic +" "+str(message.payload.decode("utf-8")))
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)

    mensaje = message.topic + ": " + str(message.payload.decode("utf-8"))

    recibido_mqtt.configure(state='normal')
    recibido_mqtt.insert(END, mensaje + "\n\n")
    recibido_mqtt.yview(END)
    recibido_mqtt.configure(state='disabled')


# Creando el cliente MQTT al Broker
client = mqtt.Client(client_id=IDENTIFICADOR_SERVER, clean_session=False, userdata=None)
client.on_message = on_message
client.connect(host=BROKER_MQTT, port=PORT_MQTT)
for topic in TOPIC_SUSBCRIBE_MQTT:
    client.subscribe(topic)

# Lanzo el receptor broker
client.loop_start()





if True:
    ## Interfaz grafica para enviar datos
    from tkinter import *
    from tkinter import scrolledtext 
    from functools import partial

    def clic_restart_baliza(i=-1):
        mac = ALL_MACs_BALIZA[i]
        topic = "/" + PROJECT + "/" + mac + "/restart"
        print("B:restart:", topic)
        client.publish(topic,"1")#publish

    def clic_ota_baliza(i=-1):
        mac = ALL_MACs_BALIZA[i]
        topic = "/" + PROJECT + "/" + mac + "/OTA"
        print("B:ota", topic)
        client.publish(topic,"1")#publish

    def clic_alarma_baliza(i=-1):
        mac = ALL_MACs_BALIZA[i]
        topic = "/" + PROJECT + "/" + mac + "/Alarma"
        print("B:alarma", topic)
        client.publish(topic,"1")#publish



    def clic_restart_manitor(i=-1):
        mac = ALL_MACs_MANITOR[i]
        topic = "/" + PROJECT + "/" + mac + "/restart"
        print("M:restart:", topic)
        client.publish(topic,"1")#publish

    def clic_ota_manitor(i=-1):
        mac = ALL_MACs_MANITOR[i]
        topic = "/" + PROJECT + "/" + mac + "/OTA"
        print("M:ota", topic)
        client.publish(topic,"1")#publish



    def clic_restart_global():
        topic = "/" + PROJECT + "/" +"restart"
        print("G:restart:", topic)
        client.publish(topic,"1")#publish

    def clic_ota_global():
        topic = "/" + PROJECT + "/" +"OTA"
        print("G:ota:", topic)
        client.publish(topic,"1")#publish

    # Construyo la ventana
    window = Tk()
    window.title("Server")
    window.geometry('820x430')

    mi_Frame = Frame()
    mi_Frame.grid(column=0, row=0)

    fila = 0
    Label(mi_Frame, text="Balizas:", font=("Arial Bold", 20), fg="red").grid(column=0, row=fila)
    for i, mac in enumerate(ALL_MACs_BALIZA):
        fila = fila + 1
        Label(mi_Frame, text=mac, font=("Arial Bold", 12)).grid(column=0, row=fila)
        Button(mi_Frame, text="Restart", command=partial(clic_restart_baliza, i) ).grid(column=1, row=fila)
        Button(mi_Frame, text="OTA", command=partial(clic_ota_baliza, i) ).grid(column=2, row=fila)
        Button(mi_Frame, text="Alarma", command=partial(clic_alarma_baliza, i) ).grid(column=3, row=fila)


    fila = fila + 1
    Label(mi_Frame, text="Manitors:", font=("Arial Bold", 20), fg="red").grid(column=0, row=fila)
    for i, mac in enumerate(ALL_MACs_MANITOR):
        fila = fila + 1
        Label(mi_Frame, text=mac, font=("Arial Bold", 12)).grid(column=0, row=fila)
        Button(mi_Frame, text="Restart", command=partial(clic_restart_manitor, i) ).grid(column=1, row=fila)
        Button(mi_Frame, text="OTA", command=partial(clic_ota_manitor, i) ).grid(column=2, row=fila)

    fila = fila + 1
    Label(mi_Frame, text="Global:", font=("Arial Bold", 20), fg="red").grid(column=0, row=fila)

    fila = fila + 1
    Button(mi_Frame, text="Restart", command=clic_restart_global).grid(column=1, row=fila)
    Button(mi_Frame, text="OTA", command=clic_ota_global).grid(column=2, row=fila)


    mi_Frame2 = Frame()
    mi_Frame2.grid(column=1, row=0)

    fila = fila + 2
    Label(mi_Frame2, text="Historial Recibido:", font=("Arial Bold", 20), fg="red").grid(column=0, row=fila)

    recibido_mqtt = scrolledtext.ScrolledText(mi_Frame2, height='16', width='45', wrap=WORD, font=("Arial", 12))
    recibido_mqtt.grid(pady = 10, padx = 10)
    recibido_mqtt.configure(state='disabled')
    recibido_mqtt.focus()

    # Lanzo la ventana
    window.mainloop()



