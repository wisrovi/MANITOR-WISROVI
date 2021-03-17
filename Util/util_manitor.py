
from Util.mqtt import EnviarDatoServidor, MatricularFuncionRecibidoMQTT, IniciarEscuchaMQTT
from Util.util import Get_MAC, Leer_HoraActual


def EnviarNotificacionLavadoManosCompleto(uuid):
    mac = Get_MAC()
    bateria = uuid[14:18]
    topic = "/SPINPLM/manitor/" + mac + "/" + uuid
    msg = "{" + "'LV' : " + bateria + ", 'HOUR': " + Leer_HoraActual() + ", 'mac' : " + mac + "}"

    EnviarDatoServidor(topic, msg)
    print("Enviando notificacion al servidor (MQTT) usuario se lavo correctamente las manos, uuid:", uuid)

