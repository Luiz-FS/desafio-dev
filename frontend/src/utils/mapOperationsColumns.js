import { convertIntegerToCurrency } from "./convertCurrency";

const mapOperationsColumns = (operationsList) => {
    operationsList = operationsList.sort((operationA, operationB) => {
        return (operationA.date < operationB.date) ? 1 : -1
    });

    return operationsList.map(operation => {
        const time = new Date(operation.date);
        const date = time.toLocaleDateString();
        const hour = time.toLocaleTimeString();
        let type;

        switch(operation.display_type){
            case "DEBITO":
                type = "Débito"
                break;
            case "BOLETO":
                type = "Boleto"
                break;
            case "FINANCIAMENTO":
                type = "Financiamento"
                break;
            case "CREDITO":
                type = "Crédito"
                break;
            case "RECEBIMENTO_EMPRESTIMO":
                type = "Recebimento de empréstimo"
                break;
            case "VENDAS":
                type = "Vendas"
                break;
            case "RECEBIMENTO_TED":
                type = "Recebimento TED"
                break;
            case "RECEBIMENTO_DOC":
                type = "Recebimento DOC"
                break;
            case "ALUGUEL":
                type = "Aluguel"
                break;
            default:
                type = "Inválido"
        }

        return {
            "Tipo": type,
            "Data": date,
            "Valor": convertIntegerToCurrency(operation.value),
            "CPF": operation.cpf,
            "Cartão": operation.card,
            "Hora": hour,
            "Dono da loja": operation.store_owner,
            "Nome da Loja": operation.store_name
        }
    });
}

export {
    mapOperationsColumns
}