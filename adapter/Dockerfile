FROM python:3.8

COPY requirements.txt /tmp

RUN pip3 install --upgrade pip
RUN pip install -r /tmp/requirements.txt

COPY adapter.py /adapter/
WORKDIR /adapter

ENTRYPOINT ["python3", "-u"]
CMD ["adapter.py"]
