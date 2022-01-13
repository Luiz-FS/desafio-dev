const mapFileColumns = (fileList) => {
    fileList = fileList.sort((fileA, fileB) => {
        return (fileA.created_at < fileB.created_at) ? 1 : -1;
    });

    return fileList.map(file => {
        const created_at = new Date(file.created_at);
        const updated_at = new Date(file.updated_at);
        let status;

        switch(file.display_status) {
            case "PENDING":
                status = "Pendente";
                break;
            case "FINISHED":
                status = "Finalizado";
                break;
            default:
                status = "Inválido";
        }

        return {
            "Nome": file.filepath,
            "Status": status,
            "Criado em": `${created_at.toLocaleDateString()} ${created_at.toLocaleTimeString()}`,
            "Atualizado em": `${updated_at.toLocaleDateString()} ${updated_at.toLocaleTimeString()}`
        }
    });
}

export default mapFileColumns;