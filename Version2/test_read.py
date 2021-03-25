import json
import time
from Process.Beacon_scan.config_beacon import NAME_FILE_BEACON, TIME_SCAN


def read_data_scan():
    with open(NAME_FILE_BEACON) as json_file:
        data = json.load(json_file)
        return data
    return dict()


if __name__ == '__main__':
    while True:
        print("result:")
        for key, value in read_data_scan().items():
            print(key, value)

        time.sleep(TIME_SCAN)
