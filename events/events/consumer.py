class Consumer:
    def __init__(self, events_repository):
        self._events_repository = events_repository

    def callback(self, body):
        name = body["name"]
        data = body["data"]
        self._events_repository.save(name, data)
