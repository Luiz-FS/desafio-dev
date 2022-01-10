import pytest


class ConnectionMock:
    def channel(self):
        pass

    def close(self):
        pass


class ChannelMock:
    def exchange_declare(self):
        pass

    def queue_declare(self):
        pass

    def queue_bind(self):
        pass

    def basic_qos(self):
        pass

    def basic_consume(self):
        pass

    def basic_ack(self):
        pass

    def start_consuming(self):
        pass

    def basic_publish(self):
        pass


class MethodMock:
    delivery_tag = 1


@pytest.fixture
def connection():
    return ConnectionMock()


@pytest.fixture
def channel():
    return ChannelMock()


@pytest.fixture
def method():
    return MethodMock()
