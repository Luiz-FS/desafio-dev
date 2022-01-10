from decouple import config


BROKER_HOST = config("BROKER_HOST", default="localhost", cast=str)
BROKER_USER = config("BROKER_USER", default="guest", cast=str)
BROKER_PASS = config("BROKER_PASS", default="guest", cast=str)
BROKER_PORT = config("BROKER_PORT", default=5672, cast=int)
DB_URI = config("DB_URI", default="postgresql://postgres:postgres@localhost/cnab", cast=str)
QUEUE = config("QUEUE", default="events_queue", cast=str)
ROUTING_KEY = config("ROUTING_KEY", default="events", cast=str)