#!/bin/bash

docker stack rm sprc3

docker service rm stack_services

docker swarm leave --force

docker rmi 127.0.0.1:5000/grafana 127.0.0.1:5000/adapter_mqtt -f

docker image prune -f

sudo rm -rf ./mosquitto_mqtt_vol/mosquitto.log ./database/influx_db ./database/config.yml \
            ./mosquitto_mqtt_vol/mosquitto.db ./grafana_db/data
