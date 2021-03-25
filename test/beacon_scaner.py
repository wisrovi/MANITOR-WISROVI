import time

TIME_SCAN_BEACON = 5

################## Util.beacon #################################################
import numpy as np


def diff(list1, list2):
    c = set(list1).union(set(list2))  # or c = set(list1) | set(list2)
    d = set(list1).intersection(set(list2))  # or d = set(list1) & set(list2)
    return list(c - d)


def vector_vacio(size_vector):
    return [int(i) for i in list(np.zeros(size_vector))]


from beacontools import BeaconScanner, IBeaconAdvertisement


size_vector = 10


class Beacon_Obj(object):
    mac = str()
    rssi = int()
    uuid = str()
    tx_power = int()
    major = int()
    minor = int()

    def __init__(self, mac: str, rssi: int, uuid: str, tx: int, maj: int, min: int):
        self.mac = mac
        self.rssi = rssi
        self.uuid = uuid
        self.tx_power = tx
        self.major = maj
        self.minor = min

    def getJson(self):
        return self.__dict__


BEACONs_SCANNED = dict()  # Guardo todos los beacon escaneados durante el periodo de escaneo
HISTORY_BEACON_SCAN = dict()  # Guardo todo el historial de los beacons escaneados desde el encendido del dispositivo
HISTORY_MORE_NEAR_BEACON = ["" for _ in range(
    size_vector)]  # Guardo un historico de todos los uuid mas cercanos en cada periodo de escaneo


def Process_Scan():
    global BEACONs_SCANNED
    global HISTORY_BEACON_SCAN
    global HISTORY_MORE_NEAR_BEACON

    mas_cercano = {'rssi': -150}
    for uuid, beacon_class in BEACONs_SCANNED.items():
        if mas_cercano['rssi'] < beacon_class.rssi:
            mas_cercano['rssi'] = beacon_class.rssi
            mas_cercano['uuid'] = uuid
            mas_cercano['class'] = beacon_class

        if not uuid in HISTORY_BEACON_SCAN:
            OBJ = dict()
            OBJ['beacon'] = beacon_class
            OBJ['history'] = vector_vacio(size_vector)
            HISTORY_BEACON_SCAN[uuid] = OBJ
        else:
            historico = HISTORY_BEACON_SCAN[uuid]['history']
            for i in range(size_vector - 1, 0, -1):
                historico[i] = historico[i - 1]
            historico[0] = beacon_class.rssi
            HISTORY_BEACON_SCAN[uuid]['history'] = historico

    for i in range(size_vector - 1, 0, -1):
        HISTORY_MORE_NEAR_BEACON[i] = HISTORY_MORE_NEAR_BEACON[i - 1]
    HISTORY_MORE_NEAR_BEACON[0] = mas_cercano['uuid'] if len(mas_cercano) > 1 else ""

    uuid_beacons_this_scan = [uuid for uuid in BEACONs_SCANNED]
    all_uuid_beacons_scan = [uuid for uuid in HISTORY_BEACON_SCAN]
    for uuid_no_vistos_en_este_escaneo in diff(all_uuid_beacons_scan, uuid_beacons_this_scan):
        historico = HISTORY_BEACON_SCAN[uuid_no_vistos_en_este_escaneo]['history']
        for i in range(size_vector - 1, 0, -1):
            historico[i] = historico[i - 1]
        historico[0] = 0
        HISTORY_BEACON_SCAN[uuid_no_vistos_en_este_escaneo]['history'] = historico
    BEACONs_SCANNED = dict()

    if HISTORY_MORE_NEAR_BEACON[0] != "":
        if HISTORY_MORE_NEAR_BEACON[0] == HISTORY_MORE_NEAR_BEACON[1]:
            return True, HISTORY_MORE_NEAR_BEACON[0], mas_cercano['rssi']
        else:
            return False, HISTORY_MORE_NEAR_BEACON[0], mas_cercano['rssi']
    return False, "", 0


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
        if not b.uuid in BEACONs_SCANNED:
            BEACONs_SCANNED[b.uuid] = b


scanner = BeaconScanner(callback, packet_filter=IBeaconAdvertisement)


def start_scan_beacon():
    scanner.start()


def stop_scan_beacon():
    scanner.stop()


################################################################################


start_scan_beacon()
while True:
    time.sleep(TIME_SCAN_BEACON)
    LAST_BEACON = Process_Scan()
    if LAST_BEACON[0]:
        print("Repetido cardholder:", LAST_BEACON[1])
    elif len(LAST_BEACON[1]):
        print("Nuevo cardholder:", LAST_BEACON[1])

    print("Escaneando...")
stop_scan_beacon()
