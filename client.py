from json import dumps, load
from numpy import arange
from random import choice
from sys import stdin
from time import sleep

import paho.mqtt.client as mqtt


def _create_connection():
    client = mqtt.Client()
    #  client.username_pw_set(username="writer", password="writer_sprc")
    client.connect("localhost")
    client.loop_start()

    return client


def _close_connection(client):
    client.disconnect()
    client.loop_stop()


def main():
    client = _create_connection()

    batts = list(range(90, 101))
    temps = list(range(20, 31))
    humids = list(range(30, 41))
    secs = list(arange(0.5, 1.6, 0.1))
    stations = ["AA", "BB", "CC"]

    while True:
        iot_data = {
            "BAT": choice(batts),
            "TEMP": choice(temps),
            "HUMID": choice(humids),
            "MEASURE": choice(humids) + choice(temps),
        }

        station = choice(stations)
        client.publish("UPB/" + station, dumps(iot_data))
        print(f"Station {station} published:\n{dumps(iot_data, indent=4)}\n")

        sleep(choice(secs))

    _close_connection(client)


if __name__ == "__main__":
    main()
