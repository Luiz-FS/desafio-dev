from unittest.mock import patch
from django.test import TestCase
from tests.mocks import ProducerMock
from core.utils import send_to_worker
from cnab.settings import (
    BROKER_HOST,
    BROKER_PORT,
    BROKER_USER,
    BROKER_PASS
)


class UtilsTest(TestCase):

    @patch("core.utils.Producer", return_value=ProducerMock())
    @patch.object(ProducerMock, 'open_connection')
    @patch.object(ProducerMock, 'publish')
    @patch.object(ProducerMock, 'close')
    def test_send_to_worker(self, mock_close, mock_publish, mock_open_connection, mock_producer):
        data = {
            "test": "test"
        }

        send_to_worker(data)

        mock_producer.assert_called_with(
            broker_host=BROKER_HOST,
            broker_port=BROKER_PORT,
            broker_user=BROKER_USER,
            broker_pass=BROKER_PASS,
        )
        mock_open_connection.assert_called()
        mock_publish.assert_called_with(
            routing_key="file_parser",
            message=data
        )
        mock_close.assert_called()
