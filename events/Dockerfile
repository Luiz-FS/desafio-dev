FROM python:3.9-slim

RUN apt update && apt upgrade && apt install git -y

COPY requirements/requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt --no-cache-dir

WORKDIR /app/

COPY ./events/ ./events/

COPY setup.cfg setup.cfg

COPY setup.py setup.py

RUN python setup.py install

CMD ["runevent"]
