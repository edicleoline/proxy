import { Grid, Link } from '@mui/material';
import MuiTypography from '@mui/material/Typography';

// project imports
import SubCard from 'ui-component/cards/SubCard';
import MainCard from 'ui-component/cards/MainCard';
import SecondaryAction from 'ui-component/cards/CardSecondaryAction';
import { gridSpacing } from 'store/constant';

import { useEffect, useState } from 'react';

import { getModem, getModems } from 'services/api/server/modem';

import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';

const Modems = () => {
    // const [isLoading, setLoading] = useState(true);
    const [modems, setModems] = useState([]);

    useEffect(() => {
        getModems().then(
            (items) => {
                console.log(items);
                setModems(items);

                // window.setTimeout(function () {
                //     const t = items.map(function (item) {
                //         item.external_ip = '123.123.123.123';
                //         return item;
                //     });
                //     setModems(t);
                //     console.log(t);
                // }, 1000);
                items.map(function (item) {
                    if (item.id == 2 || item.id == 5) {
                        getModem(item.modem.id).then(
                            (modem) => {
                                const _modems = items.map(function (m) {
                                    if (m.modem.id == modem.modem.id) {
                                        m.external_ip = modem.external_ip_through_device;
                                    }
                                    return m;
                                });
                                console.log('map modems', _modems);
                                setModems(_modems);
                                // console.log('asd23');
                                // console.log(modem);
                            },
                            (error) => console.log('modem error', error)
                        );
                    }
                });
            },
            (error) => console.log('modems error', error)
        );
    }, []);

    return (
        <MainCard title="Modems" secondary={<SecondaryAction link="https://next.material-ui.com/system/typography/" />}>
            <Grid container spacing={gridSpacing}>
                <Grid item xs={12} sm={12}>
                    <SubCard>
                        <Grid container direction="column" spacing={1}>
                            <Grid item>
                                <TableContainer component={Paper}>
                                    <Table sx={{ minWidth: 650 }} aria-label="simple table">
                                        <TableHead>
                                            <TableRow>
                                                <TableCell>Modem</TableCell>
                                                <TableCell align="right">Status</TableCell>
                                                <TableCell align="right">IP externo</TableCell>
                                                <TableCell align="right">Rede</TableCell>
                                                <TableCell align="right">Provedor</TableCell>
                                                <TableCell align="right">Sinal</TableCell>
                                                <TableCell align="right">Porta proxy</TableCell>
                                                <TableCell align="right">Status proxy</TableCell>
                                                <TableCell align="right">Porta USB</TableCell>
                                                <TableCell align="right">Status porta USB</TableCell>
                                                <TableCell align="right">Tipo</TableCell>
                                                <TableCell align="right">Modelo</TableCell>
                                            </TableRow>
                                        </TableHead>
                                        <TableBody>
                                            {modems.map((row) => (
                                                <TableRow key={row.modem.id} sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
                                                    <TableCell component="th" scope="row">
                                                        {row.modem.id}
                                                    </TableCell>
                                                    <TableCell align="right">{row.is_connected ? 'ON' : 'OFF'}</TableCell>
                                                    <TableCell align="right">{row.external_ip ? row.external_ip : '-'}</TableCell>
                                                    <TableCell align="right"></TableCell>
                                                    <TableCell align="right"></TableCell>
                                                    <TableCell align="right"></TableCell>
                                                    <TableCell align="right">{row.proxy.port}</TableCell>
                                                    <TableCell align="right"></TableCell>
                                                    <TableCell align="right">{row.usb.port}</TableCell>
                                                    <TableCell align="right">{row.usb.status}</TableCell>
                                                    <TableCell align="right">{row.modem.device.type}</TableCell>
                                                    <TableCell align="right">{row.modem.device.model}</TableCell>
                                                </TableRow>
                                            ))}
                                        </TableBody>
                                    </Table>
                                </TableContainer>
                            </Grid>
                        </Grid>
                    </SubCard>
                </Grid>
            </Grid>
        </MainCard>
    );
};

export default Modems;
