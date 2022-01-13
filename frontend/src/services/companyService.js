import Api from "./api";

const getStores = async () => {
    const resp = await Api.get("/store/");
    const data = resp.data
    return data
}

export { 
    getStores
};