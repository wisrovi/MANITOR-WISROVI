import paho.mqtt.client as mqtt
from Config.broker_mqtt import BROKER_MQTT, PORT_MQTT

NAME_THIS_CLIENT_MQTT = "R1"
client = mqtt.Client(client_id=NAME_THIS_CLIENT_MQTT, clean_session=False, userdata=None)


def on_message(client, userdata, message):
    print("*************************")
    print(message.topic + " " + str(message.payload))
    print("message received ", str(message.payload.decode("utf-8")))
    print("message topic=", message.topic)
    print("message qos=", message.qos)
    print("message retain flag=", message.retain)


client.on_message = on_message

client.connect(host=BROKER_MQTT, port=PORT_MQTT, keepalive=60, bind_address="")

TOPIC_SUSBCRIBE_MQTT = list()
# TOPIC_SUSBCRIBE_MQTT.append("$SYS/#")
TOPIC_SUSBCRIBE_MQTT.append("prueba")
TOPIC_SUSBCRIBE_MQTT.append("/#")
for topic in TOPIC_SUSBCRIBE_MQTT:
    client.subscribe(topic)  # subscribe

client.loop_forever()
