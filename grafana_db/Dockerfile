FROM grafana/grafana
COPY ./grafana_provisioning/grafana_datasources/datasource.yml /etc/grafana/provisioning/datasources
COPY ./grafana_provisioning/grafana_dashboards/default.yml /etc/grafana/provisioning/dashboards
COPY ./grafana_provisioning/grafana_dashboards/UPB_IoT_Data.json /etc/grafana/provisioning/dashboards
COPY ./grafana_provisioning/grafana_dashboards/Battery_Data.json /etc/grafana/provisioning/dashboards
