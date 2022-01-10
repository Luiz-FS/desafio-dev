import signal
import pytest
from rabbit_queue.exception import BrokerConnectionError
from worker.main import main, handle_sigterm
from worker.settings import (
    BROKER_HOST,
    BROKER_PORT,
    BROKER_USER,
    BROKER_PASS,
    QUEUE,
    ROUTING_KEY
)


def test_main(mocker, consumer_adapter, consumer):
    mock_signal = mocker.patch("worker.main.signal.signal")
    mock_producer = mocker.patch("worker.main.Producer", return_value={})
    mock_consumer_adapter = mocker.patch("worker.main.ConsumerAdapter", return_value=consumer_adapter)
    mock_run = mocker.patch.object(consumer_adapter, "run")
    mock_consumer = mocker.patch("worker.main.Consumer", return_value=consumer)
    
    main()

    mock_signal.assert_called_with(signal.SIGTERM, handle_sigterm)
    mock_producer.assert_called_with(
        broker_host=BROKER_HOST,
        broker_port=BROKER_PORT,
        broker_user=BROKER_USER,
        broker_pass=BROKER_PASS,
    )

    mock_consumer_adapter.assert_called_with(
        broker_host=BROKER_HOST,
        broker_port=BROKER_PORT,
        broker_user=BROKER_USER,
        broker_pass=BROKER_PASS,
        queue=QUEUE,
        rounting_key=ROUTING_KEY,
        callback=consumer.callback
    )

    mock_run.assert_called()
    mock_consumer.assert_called_with({})


def test_main_with_connection_error(mocker, consumer_adapter, consumer):
    mock_signal = mocker.patch("worker.main.signal.signal")
    mock_producer = mocker.patch("worker.main.Producer", return_value={})
    mock_consumer_adapter = mocker.patch("worker.main.ConsumerAdapter", return_value=consumer_adapter)
    mock_run = mocker.patch.object(consumer_adapter, "run", side_effect=BrokerConnectionError)
    mock_consumer = mocker.patch("worker.main.Consumer", return_value=consumer)
    mock_exit = mocker.patch("worker.main.exit")
    
    main()

    mock_signal.assert_called_with(signal.SIGTERM, handle_sigterm)
    mock_producer.assert_called_with(
        broker_host=BROKER_HOST,
        broker_port=BROKER_PORT,
        broker_user=BROKER_USER,
        broker_pass=BROKER_PASS,
    )

    mock_consumer_adapter.assert_called_with(
        broker_host=BROKER_HOST,
        broker_port=BROKER_PORT,
        broker_user=BROKER_USER,
        broker_pass=BROKER_PASS,
        queue=QUEUE,
        rounting_key=ROUTING_KEY,
        callback=consumer.callback
    )

    mock_run.assert_called()
    mock_consumer.assert_called_with({})
    mock_exit.assert_called_with(1)


@pytest.mark.parametrize(
    "exception",
    [
        KeyboardInterrupt,
        SystemExit
    ],
)
def test_main_exit(exception, mocker, consumer_adapter, consumer):
    mock_signal = mocker.patch("worker.main.signal.signal")
    mock_producer = mocker.patch("worker.main.Producer", return_value={})
    mock_consumer_adapter = mocker.patch("worker.main.ConsumerAdapter", return_value=consumer_adapter)
    mock_run = mocker.patch.object(consumer_adapter, "run", side_effect=exception)
    mock_consumer = mocker.patch("worker.main.Consumer", return_value=consumer)
    
    main()

    mock_signal.assert_called_with(signal.SIGTERM, handle_sigterm)
    mock_producer.assert_called_with(
        broker_host=BROKER_HOST,
        broker_port=BROKER_PORT,
        broker_user=BROKER_USER,
        broker_pass=BROKER_PASS
    )

    mock_consumer_adapter.assert_called_with(
        broker_host=BROKER_HOST,
        broker_port=BROKER_PORT,
        broker_user=BROKER_USER,
        broker_pass=BROKER_PASS,
        queue=QUEUE,
        rounting_key=ROUTING_KEY,
        callback=consumer.callback
    )

    mock_run.assert_called()
    mock_consumer.assert_called_with({})


def test_handle_sigterm():
    with pytest.raises(SystemExit):
        handle_sigterm()
