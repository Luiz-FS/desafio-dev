from events.consumer import Consumer

def test_init():
    consumer = Consumer({})
    assert consumer._events_repository == {}


def test_callback(mocker, repository):
    mock_save = mocker.patch.object(repository, 'save')
    consumer = Consumer(repository)
    body = {
        "name": "Test",
        "data": {"test": "test"}
    }

    consumer.callback(body)
    mock_save.assert_called_with(body["name"], body["data"])
