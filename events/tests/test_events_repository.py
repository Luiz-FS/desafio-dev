import json
from events.repository.events_repository import PostgresqlEventsRepository


def test_init(mocker):
    mock_connect = mocker.patch(
        "events.repository.events_repository.psycopg2.connect",
        return_value={}
    )

    repository = PostgresqlEventsRepository("db_uri")

    mock_connect.assert_called_with("db_uri")
    assert repository._db_conn == {}


def test_save(mocker, connection, cursor):
    mock_connect = mocker.patch(
        "events.repository.events_repository.psycopg2.connect",
        return_value=connection
    )
    mock_cursor = mocker.patch.object(connection, "cursor", return_value=cursor)
    mock_commit = mocker.patch.object(connection, "commit")
    mock_execute = mocker.patch.object(cursor, "execute")
    mock_close = mocker.patch.object(cursor, "close")
    query = "INSERT INTO events (name, data) VALUES (%s, %s)"
    name = "SaveFile"
    data = {
        "test": "fake data"
    }

    repository = PostgresqlEventsRepository("db_uri")
    repository.save(name, data)

    mock_connect.assert_called_with("db_uri")
    mock_cursor.assert_called()
    mock_commit.assert_called()
    mock_execute.assert_called_with(
        query,
        (name, json.dumps(data))
    )
    mock_close.assert_called()


def test_close_connection(mocker, connection):
    mock_connect = mocker.patch(
        "events.repository.events_repository.psycopg2.connect",
        return_value=connection
    )
    mock_close = mocker.patch.object(connection, "close")

    repository = PostgresqlEventsRepository("db_uri")
    repository.close_connection()

    mock_connect.assert_called_with("db_uri")
    mock_close.assert_called()
