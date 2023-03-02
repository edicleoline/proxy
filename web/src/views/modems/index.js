import { Grid, Link } from '@mui/material';
import MuiTypography from '@mui/material/Typography';

// project imports
import SubCard from 'ui-component/cards/SubCard';
import MainCard from 'ui-component/cards/MainCard';
import SecondaryAction from 'ui-component/cards/CardSecondaryAction';
import { gridSpacing } from 'store/constant';

import { useEffect, useState } from 'react';

import { getModem } from 'services/api/server/modem';

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
        getModem().then(
            (items) => {
                console.log(items);
                setModems(items);
            },
            (error) => console.log('modem error', error)
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
                                                <TableCell align="right">Porta proxy</TableCell>
                                                <TableCell align="right">Porta USB</TableCell>
                                                <TableCell align="right">Status porta USB</TableCell>
                                            </TableRow>
                                        </TableHead>
                                        <TableBody>
                                            {modems.map((row) => (
                                                <TableRow key={row.modem.id} sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
                                                    <TableCell component="th" scope="row">
                                                        {row.modem.id}
                                                    </TableCell>
                                                    <TableCell align="right">{row.is_connected ? 'ON' : 'OFF'}</TableCell>
                                                    <TableCell align="right">{row.proxy.port}</TableCell>
                                                    <TableCell align="right">{row.proxy.port}</TableCell>
                                                    <TableCell align="right">{row.usb.port}</TableCell>
                                                    <TableCell align="right">{row.usb.status}</TableCell>
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
