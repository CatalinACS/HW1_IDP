FROM python:3.8

COPY requirements.txt /tmp

RUN pip3 install --upgrade pip
RUN pip install -r /tmp/requirements.txt
RUN pip install mysqlclient

COPY api_server.py /api_server/
WORKDIR /api_server

ENTRYPOINT ["python3", "-u"]
CMD ["api_server.py"]
