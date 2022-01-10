class IOMock:
    def write(self):
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
