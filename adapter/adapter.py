import paho.mqtt.client as mqtt
import json
import socket
import time
import os
import sys
import logging as log

from influxdb import InfluxDBClient
from datetime import datetime
from json import loads, dumps
from re import match

reg_str = "[^/]+/[^/]+$"


class Adapter_MQTT:
    def __init__(self, database, mqtt_client, debug_data, logger):
        self.database = database
        self.mqtt_client = mqtt_client
        self.logger = logger
        self.debug_data = debug_data

    def start_adapter(self):
        reach_serv = False

        self.mqtt_client.on_connect = mqtt_connect
        self.mqtt_client.on_message = mqtt_message

        if self.debug_data == "true":
            FORMAT = "%(asctime)s %(message)s"
            log.basicConfig(
                stream=sys.stdout,
                format=FORMAT,
                datefmt="%Y-%m-%d %H:%M:%S",
                level=log.INFO,
            )

        while reach_serv is False:
            try:
                self.mqtt_client.username_pw_set(
                    username=os.environ.get("ADAPTER_USERNAME"),
                    password=os.environ.get("ADAPTER_PASSWORD"),
                )
                self.mqtt_client.connect(os.environ.get("MQTT_IOT_BROKER"), 1883, 60)
                reach_serv = True
            except socket.gaierror as var:
                time.sleep(2)

        self.mqtt_client.loop_forever()


influx_database = InfluxDBClient(
    host=os.environ.get("DATABASE_NAME_SWARM"),
    port=8086,
    database=os.environ.get("DATABASE_NAME_INFLUX"),
    timeout=1000,
)
mqtt_client = mqtt.Client(userdata=influx_database)

logger = log.getLogger()

adapter = Adapter_MQTT(
    influx_database, mqtt_client, os.environ.get("DEBUG_DATA_FLOW"), logger
)


def mqtt_connect(client, userdata, flags, rc):
    client.subscribe("#")
    if adapter.debug_data == "true":
        adapter.logger.info("Adapter connected to MQTT Broker with code " + str(rc))


def mqtt_message(client, userdata, msg):
    if match(reg_str, msg.topic) == None:
        return

    content = json.loads(msg.payload.decode())

    if adapter.debug_data == "true":
        adapter.logger.info("Received a message by topic [{}]".format(msg.topic))

    if "timestamp" not in content.keys():
        curr_info = datetime.now()
        if adapter.debug_data == "true":
            adapter.logger.info("Data timestamp is NOW")
    else:
        try:
            curr_info = datetime.strptime(content["timestamp"], "%Y-%m-%dT%H:%M:%S%z")
        except:
            curr_info = content["timestamp"]
        if adapter.debug_data == "true":
            adapter.logger.info("Data timestamp is {}".format(curr_info))

    json_content = []
    for content_key, content_num in content.items():
        if not (
            isinstance(content_num, float) == True
            or isinstance(content_num, int) == True
        ):
            continue

        aux = {}
        aux["measurement"] = "{}.{}".format(msg.topic.split("/")[1], content_key)
        aux["tags"] = {}
        aux["tags"]["location"] = msg.topic.split("/")[0]
        aux["tags"]["station"] = msg.topic.split("/")[1]
        try:
            aux["timestamp"] = curr_info.strftime("%Y-%m-%dT%H:%M:%S%z")
        except:
            aux["timestamp"] = curr_info
        aux["fields"] = {}
        aux["fields"]["value"] = float(content_num)
        json_content.append(aux)

        if adapter.debug_data == "true":
            adapter.logger.info(
                "{}.{}.{} {}".format(
                    aux["tags"]["location"],
                    aux["tags"]["station"],
                    content_key,
                    content_num,
                )
            )

    if not (json_content == []):
        adapter.database.write_points(
            json_content,
            database=os.environ.get("DATABASE_NAME_INFLUX"),
            time_precision="s",
            protocol="json",
        )


if __name__ == "__main__":
    adapter.start_adapter()
