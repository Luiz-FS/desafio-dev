import Api from "./api";

const FILE_ROUTE = "/file/"


const getFiles = async () => {
    const resp = await Api.get(FILE_ROUTE);
    const data = resp.data
    return data
}

const uploadFile = async (file) => {
    const formData = new FormData();
    formData.append("file", file);

    const headers = {
        'Content-Type': 'multipart/form-data'
    }

    await Api.post(FILE_ROUTE, formData, {
        headers
    });
}

export { 
    getFiles,
    uploadFile
};