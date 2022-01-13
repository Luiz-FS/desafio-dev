import React, {useState, useEffect} from "react";
import Select from '@mui/material/Select';
import FormControl from '@mui/material/FormControl';
import MenuItem from '@mui/material/MenuItem';
import Typography from '@mui/material/Typography';
import InputLabel from '@mui/material/InputLabel';
import { makeStyles } from '@material-ui/styles';
import { CustomTable, Page } from "../../components";
import { getStores } from "../../services/companyService";
import { getOperationsByStore } from "../../services/operationsService";
import { mapOperationsColumns } from "../../utils/mapOperationsColumns";
import { convertIntegerToCurrency } from "../../utils/convertCurrency";


const useStyles = makeStyles(() => ({
    storeBalance: {
        marginTop: "40px"
    }
}));

const Operations = () => {
    const columns = ["Tipo", "Data", "Valor", "CPF", "Cartão", "Hora", "Dono da loja", "Nome da Loja"];
    const [rows, setRows] = useState([]);
    const [stores, setStores] = useState([]);
    const [store, setStore] = useState("");
    const classes = useStyles();

    const loadStores = async () => {
        const data = await getStores();
        setStores(data);
    }

    const loadOperations = async (storeId) => {
        const data = await getOperationsByStore(storeId);
        setRows(mapOperationsColumns(data));
    }

    useEffect(() => {
        loadStores();
    }, []);

    const handleChangeStore = async (event) => {
        const newStore = event.target.value;
        setStore(newStore);
        await loadOperations(newStore.name);
    };

    return (
        <Page
            title="Operações"
        >
            <div>
                <FormControl sx={{ m: 1, minWidth: 300 }}>
                    <InputLabel id="demo-simple-select-disabled-label">Selecione uma loja</InputLabel>
                    <Select
                        labelId="demo-simple-select-disabled-label"
                        id="demo-simple-select-disabled"
                        value={store}
                        label="Selecione uma loja"
                        onChange={handleChangeStore}
                    >
                        {
                            stores.map((store, index) => {
                                return (
                                    <MenuItem key={index} value={store}>{store.name}</MenuItem>
                                )
                            })
                        }
                    </Select>
                </FormControl>

                {(store) ? 
                    <Typography
                        className={classes.storeBalance}
                        sx={{ flex: '1 1 100%' }}
                        variant="h6"
                        id="tableTitle"
                        component="div"
                        >
                        <b>Saldo da loja: { convertIntegerToCurrency(store.balance) }</b>
                    </Typography> : <></>}
                <CustomTable columns={columns} rows={rows} tableTitle="Operações"/>
            </div>
        </Page>
    );
}

export default Operations;
