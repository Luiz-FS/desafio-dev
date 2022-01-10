from enum import Enum

class TransactionType(Enum):
    DEBITO = 1
    BOLETO = 2
    FINANCIAMENTO = 3
    CREDITO = 4
    RECEBIMENTO_EMPRESTIMO = 5
    VENDAS = 6
    RECEBIMENTO_TED = 7
    RECEBIMENTO_DOC = 8
    ALUGUEL = 9


class FileStatus(Enum):
    PENDING = 1
    FINISHED = 2
