import pytest
import json
from pika.exceptions import AMQPConnectionError
from unittest.mock import MagicMock
from rabbit_queue.exception import BrokerConnectionError
from rabbit_queue.consumer import (
    Consumer,
    BROKER_HOST,
    BROKER_PASS,
    BROKER_PORT,
    BROKER_USER
)


def test_init(mocker, connection, channel):
    mock_parameters = mocker.patch("rabbit_queue.consumer.pika.ConnectionParameters", return_value={})
    mock_credentials = mocker.patch("rabbit_queue.consumer.pika.PlainCredentials", return_value={})
    mock_connection = mocker.patch("rabbit_queue.consumer.pika.BlockingConnection", return_value=connection)
    mock_channel = mocker.patch.object(connection, "channel", return_value=channel)
    mock_exchange_declare = mocker.patch.object(channel, "exchange_declare")
    mock_queue_declare = mocker.patch.object(channel, "queue_declare")
    mock_queue_bind = mocker.patch.object(channel, "queue_bind")
    mock_basic_qos = mocker.patch.object(channel, "basic_qos")
    mock_basic_consume = mocker.patch.object(channel, "basic_consume")

    Consumer(
        queue="queue",
        rounting_key="key",
        callback={}
    )

    mock_credentials.assert_called_with(BROKER_USER, BROKER_PASS)
    mock_parameters.assert_called_with(
        host=BROKER_HOST,
        port=BROKER_PORT,
        credentials={},
        heartbeat=60,
    )
    mock_connection.assert_called_with({})
    mock_channel.assert_called()
    mock_exchange_declare.assert_called_with(
        exchange="streaming",
        exchange_type="direct"
    )
    mock_queue_declare.assert_called_with(
        queue="queue",
        durable=True
    )
    mock_queue_bind.assert_called_with(
        queue="queue",
        exchange="streaming",
        routing_key="key"
    )
    mock_basic_qos.assert_called_with(
        prefetch_count=1
    )
    mock_basic_consume.assert_called()


def test_init_fail(mocker):
    mock_parameters = mocker.patch("rabbit_queue.consumer.pika.ConnectionParameters", return_value={})
    mock_credentials = mocker.patch("rabbit_queue.consumer.pika.PlainCredentials", return_value={})
    mock_connection = mocker.patch("rabbit_queue.consumer.pika.BlockingConnection", side_effect=AMQPConnectionError)

    with pytest.raises(BrokerConnectionError):
        Consumer(
            queue="queue",
            rounting_key="key",
            callback={}
        )

    mock_credentials.assert_called_with(BROKER_USER, BROKER_PASS)
    mock_parameters.assert_called_with(
        host=BROKER_HOST,
        port=BROKER_PORT,
        credentials={},
        heartbeat=60,
    )
    mock_connection.assert_called_with({})


def test_callback(mocker, connection, channel, method):
    mocker.patch("rabbit_queue.consumer.pika.ConnectionParameters", return_value={})
    mocker.patch("rabbit_queue.consumer.pika.PlainCredentials", return_value={})
    mocker.patch("rabbit_queue.consumer.pika.BlockingConnection", return_value=connection)
    mocker.patch.object(connection, "channel", return_value=channel)
    mocker.patch.object(channel, "exchange_declare")
    mocker.patch.object(channel, "queue_declare")
    mocker.patch.object(channel, "queue_bind")
    mocker.patch.object(channel, "basic_qos")
    mocker.patch.object(channel, "basic_consume")
    mock_basic_ack = mocker.patch.object(channel, "basic_ack")
    mock_callback = MagicMock()
    
    data = {
        "test": "fake data"
    }

    consumer = Consumer(
        queue="queue",
        rounting_key="key",
        callback={}
    )

    consumer._callback(channel, method, {}, json.dumps(data), mock_callback)

    mock_callback.assert_called_with(data)
    mock_basic_ack.assert_called_with(
        delivery_tag=method.delivery_tag
    )


def test_run(mocker, connection, channel):
    mocker.patch("rabbit_queue.consumer.pika.ConnectionParameters", return_value={})
    mocker.patch("rabbit_queue.consumer.pika.PlainCredentials", return_value={})
    mocker.patch("rabbit_queue.consumer.pika.BlockingConnection", return_value=connection)
    mocker.patch.object(connection, "channel", return_value=channel)
    mocker.patch.object(channel, "exchange_declare")
    mocker.patch.object(channel, "queue_declare")
    mocker.patch.object(channel, "queue_bind")
    mocker.patch.object(channel, "basic_qos")
    mocker.patch.object(channel, "basic_consume")
    mock_start_consuming = mocker.patch.object(channel, "start_consuming")

    consumer = Consumer(
        queue="queue",
        rounting_key="key",
        callback={}
    )

    consumer.run()

    mock_start_consuming.assert_called()
