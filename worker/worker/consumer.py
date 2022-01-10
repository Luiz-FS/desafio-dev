from worker.enumerators import TransactionType
from worker.logger import logger
from worker.settings import PROCESS_AREA

class Consumer:
    def __init__(self, producer):
        self._producer = producer
        self._map_type = {
            "1": TransactionType.DEBITO,
            "2": TransactionType.BOLETO,
            "3": TransactionType.FINANCIAMENTO,
            "4": TransactionType.CREDITO,
            "5": TransactionType.RECEBIMENTO_EMPRESTIMO,
            "6": TransactionType.VENDAS,
            "7": TransactionType.RECEBIMENTO_TED,
            "8": TransactionType.RECEBIMENTO_DOC,
            "9": TransactionType.ALUGUEL
        }

        self._map_field_to_slice = {
            "type": (0, 1),
            "date": (1, 9),
            "value": (9, 19),
            "cpf": (19, 30),
            "card": (30, 42),
            "hour": (42, 48),
            "store_owner": (48, 62),
            "store_name": (62, 81)
        }

    def parse_line(self, line):
        result = {}

        for (field, slice) in self._map_field_to_slice.items():
            start, end = slice
            result[field] = line[start:end].lower().strip()

        return result

    def read_file(self, filepath):
        lines = []

        with open(f"{PROCESS_AREA}/{filepath}") as f:
            lines = f.read().splitlines()

        return lines


    def parse_lines(self, lines):
        parsed_lines = []

        for line in lines:
            parsed_lines.append(self.parse_line(line))

        return parsed_lines

    def send_to_events(self, name, data):
        self._producer.open_connection()
        self._producer.publish(
            routing_key="events",
            message={
                "name": name,
                "data": data
            }
        )
        self._producer.close()

    def mount_cnab_object(self, data):
        return {
            "type": data["type"],
            "date": f"{data['date']}{data['hour']}",
            "value": data["value"],
            "cpf": data["cpf"],
            "card": data["card"],
            "store_owner": data["store_owner"],
            "store_name": data["store_name"]
        }

    def mount_store_object(self, cnab_data):
        return {
            "name": cnab_data["store_name"],
            "owner": cnab_data["store_owner"],
            "balance": self._map_type[cnab_data["type"]](int(cnab_data["value"]))
        }  

    def process_lines(self, lines):
        for line in lines:
            cnab_object = self.mount_cnab_object(line)
            store_object = self.mount_store_object(cnab_object)

            self.send_to_events(name="SaveCNAB", data=cnab_object)
            self.send_to_events(name="SaveStore", data=store_object)

    def callback(self, body):
        status_finished = 2
        file_id = body["file_id"]
        filepath = body["filepath"]

        logger.info("Reading file...")
        lines = self.read_file(filepath)

        logger.info("Parsing lines...")
        parsed_lines = self.parse_lines(lines)

        logger.info("Processing lines...")
        self.process_lines(parsed_lines)

        logger.info("Sending to events")
        self.send_to_events(
            name="SaveFile",
            data={
                "id": file_id,
                "status": status_finished
            }
        )
