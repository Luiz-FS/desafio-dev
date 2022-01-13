const convertIntegerToCurrency = (value) => {
    var formatter = new Intl.NumberFormat('pt-br', {
        style: 'currency',
        currency: 'BRL'
    });

    return formatter.format(value/100);
}

export {
    convertIntegerToCurrency
}
