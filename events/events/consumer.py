class Consumer:
    def __init__(self, events_repository):
        self._events_repository = events_repository

    def callback(self, body):
        """Method for processing the messages received by the queue.

        Parameters
        ----------
        body : dict
            Message data.
        """
        name = body["name"]
        data = body["data"]
        self._events_repository.save(name, data)
