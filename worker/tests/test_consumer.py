from unittest.mock import call
from worker.consumer import Consumer
from worker.settings import PROCESS_AREA


def test_init():
    consumer = Consumer(producer={})
    assert consumer._producer == {}


def test_parse_line():
    consumer = Consumer(producer={})
    line = "5201903010000013200556418150633123****7687145607MARIA JOSEFINALOJA DO Ó - MATRIZ"
    expected = {
        "type": '5',
        "date": '20190301',
        "value": '0000013200',
        "cpf": '55641815063',
        "card": '3123****7687',
        "hour": '145607',
        "store_owner": 'maria josefina',
        "store_name": 'loja do ó - matriz'
    }

    parsed_line = consumer.parse_line(line)

    assert parsed_line == expected


def test_parse_lines():
    consumer = Consumer(producer={})
    lines = ["5201903010000013200556418150633123****7687145607MARIA JOSEFINALOJA DO Ó - MATRIZ"] * 5
    expected = [{
        "type": '5',
        "date": '20190301',
        "value": '0000013200',
        "cpf": '55641815063',
        "card": '3123****7687',
        "hour": '145607',
        "store_owner": 'maria josefina',
        "store_name": 'loja do ó - matriz'
    }] * 5

    parsed_lines = consumer.parse_lines(lines)

    assert parsed_lines == expected


def test_read_file(mocker, open, io):
    file_txt = "line1\nline2\nlin3"
    mock_open = mocker.patch("worker.consumer.open", return_value=open)
    mock_read = mocker.patch.object(io, "read", return_value=file_txt)

    consumer = Consumer(producer={})
    lines = consumer.read_file("file_test.txt")

    mock_open.assert_called_with(f"{PROCESS_AREA}/file_test.txt")
    mock_read.assert_called()

    assert lines == file_txt.splitlines()


def test_send_to_events(mocker, producer):
    mock_open_connection = mocker.patch.object(producer, "open_connection")
    mock_publish = mocker.patch.object(producer, "publish")
    mock_close = mocker.patch.object(producer, "close")
    name = "SaveFile"
    data = {
        "test": "fakedata"
    }

    consumer = Consumer(producer=producer)
    consumer.send_to_events(name, data)

    mock_open_connection.assert_called()
    mock_publish.assert_called_with(
        routing_key="events",
        message={
            "name": name,
            "data": data
        }
    )
    mock_close.assert_called()


def test_mount_cnab_object():
    consumer = Consumer(producer={})
    data = {
        "type": '5',
        "date": '20190301',
        "value": '0000013200',
        "cpf": '55641815063',
        "card": '3123****7687',
        "hour": '145607',
        "store_owner": 'maria josefina',
        "store_name": 'loja do ó - matriz'
    }
    expected = {
        "type": '5',
        "date": '20190301145607',
        "value": '0000013200',
        "cpf": '55641815063',
        "card": '3123****7687',
        "store_owner": 'maria josefina',
        "store_name": 'loja do ó - matriz'
    }

    mounted = consumer.mount_cnab_object(data)

    assert mounted == expected


def test_mount_store_object():
    consumer = Consumer(producer={})
    cnab_data = {
        "type": '5',
        "date": '20190301145607',
        "value": '0000013200',
        "cpf": '55641815063',
        "card": '3123****7687',
        "store_owner": 'maria josefina',
        "store_name": 'loja do ó - matriz'
    }
    expected = {
        "name": cnab_data["store_name"],
        "owner": cnab_data["store_owner"],
        "balance": int(cnab_data["value"])
    }

    mounted = consumer.mount_store_object(cnab_data)

    assert mounted == expected


def test_process_lines(mocker):
    mock_mount_cnab_object = mocker.patch("worker.consumer.Consumer.mount_cnab_object", return_value={})
    mock_mount_store_object = mocker.patch("worker.consumer.Consumer.mount_store_object", return_value={})
    mock_send_to_events = mocker.patch("worker.consumer.Consumer.send_to_events")
    lines = [{"test": "fakedata"}]

    consumer = Consumer(producer={})
    consumer.process_lines(lines)

    calls = [
        call(name="SaveCNAB", data={}),
        call(name="SaveStore", data={})
    ]
    mock_mount_cnab_object.assert_called_with(lines[0])
    mock_mount_store_object.assert_called_with({})
    mock_send_to_events.assert_has_calls(calls)
    

def test_callback(mocker):
    mock_read_file = mocker.patch("worker.consumer.Consumer.read_file", return_value=[])
    mock_parse_lines = mocker.patch("worker.consumer.Consumer.parse_lines", return_value=[])
    mock_process_lines = mocker.patch("worker.consumer.Consumer.process_lines", return_value=[])
    mock_send_to_events = mocker.patch("worker.consumer.Consumer.send_to_events")
    body = {
        "file_id": "file_id",
        "filepath": "filepath"
    }

    consumer = Consumer(producer={})
    consumer.callback(body)

    mock_read_file.assert_called_with(body["filepath"])
    mock_parse_lines.assert_called_with([])
    mock_process_lines.assert_called_with([])
    mock_send_to_events.assert_called_with(
        name="SaveFile",
        data={
            "id": body["file_id"],
            "status": 2
        }
    )
