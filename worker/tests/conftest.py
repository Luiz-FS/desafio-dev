import pytest


class ConsumerAdapterMock:
    def run(self):
        pass


class ConsumerMock:
    def callback(self):
        pass


class IOMock:
    def read(self):
        pass


class OpenMock:
    def __init__(*args, **kwargs):
        pass

    def __enter__(self):
        return IOMock()
    
    def __exit__(self, *args, **kwargs):
        pass


class ProducerMock:
    def open_connection(self):
        pass

    def publish(self):
        pass

    def close(self):
        pass


@pytest.fixture
def consumer_adapter():
    return ConsumerAdapterMock()


@pytest.fixture
def consumer():
    return ConsumerMock()


@pytest.fixture
def open():
    return OpenMock()


@pytest.fixture
def io():
    return IOMock


@pytest.fixture
def producer():
    return ProducerMock()
