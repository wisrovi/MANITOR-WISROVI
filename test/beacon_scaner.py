import time

from Config.beacon import TIME_SCAN_BEACON
from Util.beacon import Process_Scan, start_scan_beacon,stop_scan_beacon

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



