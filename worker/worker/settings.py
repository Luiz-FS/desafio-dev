from decouple import config


BROKER_HOST = config("BROKER_HOST", default="localhost", cast=str)
BROKER_USER = config("BROKER_USER", default="guest", cast=str)
BROKER_PASS = config("BROKER_PASS", default="guest", cast=str)
BROKER_PORT = config("BROKER_PORT", default=5672, cast=int)
PROCESS_AREA = config("PROCESS_AREA", default="/opt/process_area", cast=str)
QUEUE = config("QUEUE", default="file_parser_queue", cast=str)
ROUTING_KEY = config("ROUTING_KEY", default="file_parser", cast=str)
