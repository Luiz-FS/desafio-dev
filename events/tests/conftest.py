import pytest


class RepositoryMock:
    def save(self):
        pass

    def close_connection(self):
        pass


class ConsumerAdapterMock:
    def run(self):
        pass


class ConsumerMock:
    def callback(self):
        pass


class CursorMock:
    def execute(self):
        pass

    def close(self):
        pass


class ConnectionMock:
    def cursor(self):
        pass

    def commit(self):
        pass

    def close(self):
        pass


@pytest.fixture
def repository():
    return RepositoryMock()


@pytest.fixture
def consumer_adapter():
    return ConsumerAdapterMock()


@pytest.fixture
def consumer():
    return ConsumerMock()


@pytest.fixture
def connection():
    return ConnectionMock()


@pytest.fixture
def cursor():
    return CursorMock()