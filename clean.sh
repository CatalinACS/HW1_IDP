#!/bin/bash

docker stack rm idp_project

docker service rm stack_services

docker swarm leave --force

docker rmi 127.0.0.1:5000/grafana 127.0.0.1:5000/adapter_mqtt 127.0.0.1:5000/login_server_img -f

docker image prune -f

sudo rm -rf ./mosquitto_mqtt_vol/mosquitto.log ./influx_database/influx_db ./influx_database/config.yml \
        ./mosquitto_mqtt_vol/mosquitto.db ./grafana_db/data ./mysql_database/mysql-db/
