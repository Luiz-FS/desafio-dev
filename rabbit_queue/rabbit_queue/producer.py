import pika
import json
from decouple import config


BROKER_HOST = config("BROKER_HOST", default="localhost", cast=str)
BROKER_USER = config("BROKER_USER", default="guest", cast=str)
BROKER_PASS = config("BROKER_PASS", default="guest", cast=str)
BROKER_PORT = config("BROKER_PORT", default=5672, cast=int)



class Producer:
    def __init__(
        self,
        exchange="streaming",
        exchange_type="direct",
        heartbeat=0,
        broker_host=BROKER_HOST,
        broker_user=BROKER_USER,
        broker_pass=BROKER_PASS,
        broker_port=BROKER_PORT,
    ):
        self._exchange = exchange
        parameters = pika.ConnectionParameters(
            host=broker_host,
            port=broker_port,
            credentials=pika.PlainCredentials(broker_user, broker_pass),
            heartbeat=heartbeat,
        )
        self._properties = pika.BasicProperties(content_type="application/json", delivery_mode=2)
        self._connection = pika.BlockingConnection(parameters)
        self._channel = self._connection.channel()
        self._channel.exchange_declare(
            exchange=exchange,
            exchange_type=exchange_type
        )
    
    def publish(self, routing_key, message):
        self._channel.basic_publish(
            exchange=self._exchange,
            routing_key=routing_key,
            body=json.dumps(message),
            properties=self._properties
        )
