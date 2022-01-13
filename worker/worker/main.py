import signal
from rabbit_queue.consumer import Consumer as ConsumerAdapter
from rabbit_queue.producer import Producer
from rabbit_queue.exception import BrokerConnectionError
from worker.consumer import Consumer
from worker.logger import logger
from worker.settings import BROKER_HOST, BROKER_PORT, BROKER_USER, BROKER_PASS, QUEUE, ROUTING_KEY


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
    producer = Producer(
        broker_host=BROKER_HOST,
        broker_port=BROKER_PORT,
        broker_user=BROKER_USER,
        broker_pass=BROKER_PASS,
    )

    try:
        consumer = ConsumerAdapter(
            broker_host=BROKER_HOST,
            broker_port=BROKER_PORT,
            broker_user=BROKER_USER,
            broker_pass=BROKER_PASS,
            queue=QUEUE,
            rounting_key=ROUTING_KEY,
            callback=Consumer(producer).callback,
        )

        signal.signal(signal.SIGTERM, handle_sigterm)

        logger.info("Starting worker consumer...")
        consumer.run()
    except BrokerConnectionError:
        logger.info("Unable to connect to broker...")
        exit(1)
    except (KeyboardInterrupt, SystemExit):
        logger.info("Stoping worker consumer...")


if __name__ == "__main__":  # pragma nocover
    main()
