from enum import Enum


class TransactionType(Enum):
    DEBITO = lambda value: value
    BOLETO = lambda value: value * -1
    FINANCIAMENTO = lambda value: value * -1
    CREDITO = lambda value: value
    RECEBIMENTO_EMPRESTIMO = lambda value: value
    VENDAS = lambda value: value
    RECEBIMENTO_TED = lambda value: value
    RECEBIMENTO_DOC = lambda value: value
    ALUGUEL = lambda value: value * -1
