import React, {useState, useEffect} from "react";
import TextField from '@mui/material/TextField';
import LoadingButton from '@mui/lab/LoadingButton';
import Button from '@mui/material/Button';
import { makeStyles } from '@material-ui/styles';
import { CustomTable, Page } from "../../components";
import { getFiles, uploadFile } from "../../services/fileService";
import mapFileColumns from "../../utils/mapFileColumns";


const useStyles = makeStyles(() => ({
    inputFile: {
        display: "none"
    },
    inputText: {
        "& input": {
            cursor: "pointer"
        },
        minWidth: "600px",
        marginBottom: "15px"
    }
}));


const UploadFile = () => {
    const columns = ["Nome", "Status", "Criado em", "Atualizado em"];
    const classes = useStyles();

    const [rows, setRows] = useState([]);
    const [file, setFile] = useState({"name": ""});
    const [disableSubmit, setDisableSubmit] = useState(false);

    const handleChangeFile = (event) => {
        const file = event.target.files[0];
        setFile(file);
    }

    const handleSubmitFile = async () => {
        setDisableSubmit(true);

        if (file) {
            await uploadFile(file);
            setFile({"name": ""})
            loadFiles();
        }

        setDisableSubmit(false);
    }

    const inputClick = () => {
        document.getElementById("file").click()
    }
    
    const loadFiles = async () => {
        const data = await getFiles();
        setRows(mapFileColumns(data));
    }

    useEffect(() => {
        loadFiles();
    }, []);

    return (
        <Page
            title="Enviar arquivo"
        >
            <div>
                <input className={classes.inputFile} id="file" type="file" accept="text/plain" onChange={handleChangeFile} style={{Diplay: "none"}}/>
                <div>
                    <TextField className={classes.inputText} id="standard-basic" label="Selecione um arquivo" variant="standard"  value={file.name} onClick={inputClick}/>
                </div>
                <div>
                    {(!disableSubmit) ? 
                        <Button 
                            variant="contained"
                            onClick={handleSubmitFile}>Enviar
                        </Button> :
                    
                        <LoadingButton loading variant="outlined">
                            Enviar
                        </LoadingButton>
                    }
                </div>
                <CustomTable columns={columns} rows={rows} tableTitle="Histórico de processamento"/>
            </div>
        </Page>
    );
}


export default UploadFile;
