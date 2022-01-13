from rabbit_queue.producer import Producer
from cnab.settings import BROKER_HOST, BROKER_PORT, BROKER_USER, BROKER_PASS


def send_to_worker(data):
    """Method to send message to worker queue.

    Parameters
    ----------
    data : dict
        Object data to be sent.
    """
    producer = Producer(
        broker_host=BROKER_HOST,
        broker_port=BROKER_PORT,
        broker_user=BROKER_USER,
        broker_pass=BROKER_PASS,
    )

    producer.open_connection()
    producer.publish(routing_key="file_parser", message=data)
    producer.close()
