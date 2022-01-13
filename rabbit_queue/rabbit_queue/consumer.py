import pika
import json
from functools import partial
from decouple import config
from rabbit_queue.exception import BrokerConnectionError


BROKER_HOST = config("BROKER_HOST", default="localhost", cast=str)
BROKER_USER = config("BROKER_USER", default="guest", cast=str)
BROKER_PASS = config("BROKER_PASS", default="guest", cast=str)
BROKER_PORT = config("BROKER_PORT", default=5672, cast=int)


class Consumer:
    def __init__(
        self,
        queue,
        rounting_key,
        callback,
        exchange="streaming",
        exchange_type="direct",
        heartbeat=60,
        broker_host=BROKER_HOST,
        broker_user=BROKER_USER,
        broker_pass=BROKER_PASS,
        broker_port=BROKER_PORT,
    ):
        self._queue = queue
        self._routing_key = rounting_key
        parameters = pika.ConnectionParameters(
            host=broker_host,
            port=broker_port,
            credentials=pika.PlainCredentials(broker_user, broker_pass),
            heartbeat=heartbeat,
        )

        try:
            connection = pika.BlockingConnection(parameters)
        except pika.exceptions.AMQPConnectionError:
            raise BrokerConnectionError()

        self._channel = connection.channel()
        self._channel.exchange_declare(
            exchange=exchange,
            exchange_type=exchange_type
        )
        self._channel.queue_declare(queue=queue, durable=True)
        self._channel.queue_bind(
            queue=queue,
            exchange=exchange,
            routing_key=self._routing_key
        )
        self._channel.basic_qos(prefetch_count=1)
        self._channel.basic_consume(
            queue=self._queue,
            on_message_callback=partial(self._callback, cb=callback),
            auto_ack=False
        )

    def _callback(self, channel, method, properties, body, cb):
        """Method for processing messages received by the message queue.

        Parameters
        ----------
        ch : pika.channel.Channel
            The channel object.
        method : pika.frame.Method
            Informed method.
        properties : pika.Spec.BasicProperties
            Infomed properties.
        body : str|unicode
            The message body.
        cb : function
            Callback function
        """
        body = json.loads(body)
        cb(body)
        channel.basic_ack(delivery_tag=method.delivery_tag)

    def run(self):
        """Method to start queue consumption.
        """
        self._channel.start_consuming()

