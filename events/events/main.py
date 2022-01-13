import signal
from rabbit_queue.consumer import Consumer as ConsumerAdapter
from rabbit_queue.exception import BrokerConnectionError
from events.consumer import Consumer
from events.repository.events_repository import PostgresqlEventsRepository
from events.logger import logger
from events.settings import (
    BROKER_HOST,
    BROKER_PORT,
    BROKER_USER,
    BROKER_PASS,
    QUEUE,
    ROUTING_KEY,
    DB_URI,
)


def handle_sigterm(*args):
    """SIGTERM is the name of a signal known by a computer process in POSIX
    operating systems. This is the default signal sent by the kill and killall
    commands. It causes the process to end, as in SIGKILL, but can be
    interpreted or ignored by the process. With this, SIGTERM performs a more
    friendly closing, allowing the freeing of memory and the closing of files.

    Raises
    ------
    SystemExit
        Friendly ends the execution.
    """
    logger.info("Stop by SIGTERM.")
    raise SystemExit


def main():
    """Function to start the project."""
    repository = PostgresqlEventsRepository(DB_URI)

    try:
        consumer = ConsumerAdapter(
            broker_host=BROKER_HOST,
            broker_port=BROKER_PORT,
            broker_user=BROKER_USER,
            broker_pass=BROKER_PASS,
            queue=QUEUE,
            rounting_key=ROUTING_KEY,
            callback=Consumer(repository).callback,
        )

        signal.signal(signal.SIGTERM, handle_sigterm)

        logger.info("Starting events consumer...")
        consumer.run()

    except BrokerConnectionError:
        logger.info("Unable to connect to broker...")
        exit(1)
    except (KeyboardInterrupt, SystemExit):
        logger.info("Stoping events consumer...")
        repository.close_connection()


if __name__ == "__main__":  # pragma nocover
    main()
