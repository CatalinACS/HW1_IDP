#!/bin/bash

docker swarm init

docker service create --name stack_services -p published=5000,target=5000 registry:2

sudo chown -R $USER ./grafana_db
sudo chmod -R 777 ./grafana_db

docker stack deploy -c stack.yml sprc3

docker build grafana_db/ --tag 127.0.0.1:5000/grafana
docker push 127.0.0.1:5000/grafana

docker build adapter/ --tag 127.0.0.1:5000/adapter_mqtt
docker push 127.0.0.1:5000/adapter_mqtt
