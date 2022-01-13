import Api from "./api";

const getOperationsByStore = async (storeName) => {
    const resp = await Api.get(`/cnab-documentation/?store_name=${storeName}`);
    const data = resp.data
    return data
}

export { 
    getOperationsByStore
};