FROM python:3.8

COPY requirements.txt /tmp

RUN pip3 install --upgrade pip
RUN pip install -r /tmp/requirements.txt
RUN pip install mysqlclient

COPY login_server.py /login_server/
WORKDIR /login_server

ENTRYPOINT ["python3", "-u"]
CMD ["login_server.py"]
