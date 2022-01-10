import json
from rabbit_queue.producer import (
    Producer,
    BROKER_HOST,
    BROKER_PORT,
    BROKER_PASS,
    BROKER_USER
)


def test_init(mocker):
    mock_parameters = mocker.patch("rabbit_queue.producer.pika.ConnectionParameters", return_value={})
    mock_credentials = mocker.patch("rabbit_queue.producer.pika.PlainCredentials", return_value={})
    mock_properties = mocker.patch("rabbit_queue.producer.pika.BasicProperties", return_value={})

    Producer()

    mock_credentials.assert_called_with(BROKER_USER, BROKER_PASS)
    mock_parameters.assert_called_with(
        host=BROKER_HOST,
        port=BROKER_PORT,
        credentials={},
        heartbeat=0,
    )
    mock_properties.assert_called_with(
        content_type="application/json",
        delivery_mode=2
    )


def test_open_connection(mocker, connection, channel):
    mocker.patch("rabbit_queue.producer.pika.ConnectionParameters", return_value={})
    mocker.patch("rabbit_queue.producer.pika.PlainCredentials", return_value={})
    mocker.patch("rabbit_queue.producer.pika.BasicProperties", return_value={})
    mock_connection = mocker.patch("rabbit_queue.producer.pika.BlockingConnection", return_value=connection)
    mock_channel = mocker.patch.object(connection, "channel", return_value=channel)
    mock_exchange_declare = mocker.patch.object(channel, "exchange_declare")

    producer = Producer()
    producer.open_connection()

    mock_connection.assert_called_with({})
    mock_channel.assert_called()
    mock_exchange_declare.assert_called_with(
        exchange="streaming",
        exchange_type="direct"
    )


def test_publish(mocker, channel):
    mocker.patch("rabbit_queue.producer.pika.ConnectionParameters", return_value={})
    mocker.patch("rabbit_queue.producer.pika.PlainCredentials", return_value={})
    mocker.patch("rabbit_queue.producer.pika.BasicProperties", return_value={})
    mock_basic_publish = mocker.patch.object(channel, "basic_publish")
    message = {
        "test": "fake msg"
    }

    producer = Producer()
    producer._channel = channel
    producer.publish(
        routing_key="key",
        message=message
    )

    mock_basic_publish.assert_called_with(
        exchange="streaming",
        routing_key="key",
        body=json.dumps(message),
        properties={}
    )


def test_close(mocker, connection):
    mocker.patch("rabbit_queue.producer.pika.ConnectionParameters", return_value={})
    mocker.patch("rabbit_queue.producer.pika.PlainCredentials", return_value={})
    mocker.patch("rabbit_queue.producer.pika.BasicProperties", return_value={})
    mock_close = mocker.patch.object(connection, "close")

    producer = Producer()
    producer._connection = connection
    producer.close()

    mock_close.assert_called()
