#!/bin/bash

docker swarm init

docker service create --name stack_services -p published=5000,target=5000 registry:2

sudo chown -R $USER ./grafana_db
sudo chmod -R 777 ./grafana_db

sudo chown -R $USER ./mosquitto_mqtt_vol
sudo chmod 777 ./mosquitto_mqtt_vol/mosquitto.conf

sudo chown -R $USER ./portainer_data
sudo chmod -R 777 ./portainer_data

docker stack deploy -c stack.yml idp_project

docker build grafana_db/ --tag 127.0.0.1:5000/grafana
docker push 127.0.0.1:5000/grafana

docker build adapter/ --tag 127.0.0.1:5000/adapter_mqtt
docker push 127.0.0.1:5000/adapter_mqtt
