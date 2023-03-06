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

import Button from '@mui/material/Button';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import IconButton from '@mui/material/IconButton';

const Modems = () => {
    // const [isLoading, setLoading] = useState(true);
    const [modems, setModems] = useState([]);

    const loadModems = () => {
        getModems().then(
            (items) => {
                console.log(items);
                setModems(items);

                items.map(function (item) {
                    if (item.id == 2 || item.id == 5 || true) {
                        getModem(item.modem.id).then(
                            (modem) => {
                                const remodems = items.map(function (m) {
                                    if (m.modem.id == modem.modem.id) {
                                        m.external_ip = modem.external_ip_through_device;
                                        m.device_network_type = modem.device_network_type;
                                        m.device_network_provider = modem.device_network_provider;
                                        m.device_network_signalbar = modem.device_network_signalbar;
                                    }
                                    return m;
                                });
                                setModems(remodems);
                            },
                            (error) => console.log('modem error', error)
                        );
                    }
                });
            },
            (error) => console.log('modems error', error)
        );
    };

    useEffect(() => {
        loadModems();
    }, []);

    const [anchorEl, setAnchorEl] = useState(null);
    const open = Boolean(anchorEl);
    const handleClick = (event) => {
        setAnchorEl(event.currentTarget);
    };
    const handleClose = () => {
        setAnchorEl(null);
    };

    return (
        <MainCard title="Modems" secondary={<SecondaryAction link="https://next.material-ui.com/system/typography/" />}>
            <Grid container spacing={0}>
                <Grid item xs={12} sm={12}>
                    <SubCard>
                        <Grid container direction="column" spacing={0}>
                            <Grid item>
                                <TableContainer component={Paper}>
                                    <Table sx={{ minWidth: 650 }} aria-label="modems table">
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
                                                        <IconButton
                                                            id="basic-button"
                                                            aria-label="expand row"
                                                            size="small"
                                                            aria-controls={open ? 'basic-menu' : undefined}
                                                            aria-haspopup="true"
                                                            aria-expanded={open ? 'true' : undefined}
                                                            onClick={handleClick}
                                                        >
                                                            <KeyboardArrowDownIcon />
                                                        </IconButton>
                                                        <Menu
                                                            id="basic-menu"
                                                            anchorEl={anchorEl}
                                                            open={open}
                                                            onClose={handleClose}
                                                            MenuListProps={{
                                                                'aria-labelledby': 'basic-button'
                                                            }}
                                                        >
                                                            <MenuItem onClick={handleClose}>Profile</MenuItem>
                                                            <MenuItem onClick={handleClose}>My account</MenuItem>
                                                            <MenuItem onClick={handleClose}>Logout</MenuItem>
                                                        </Menu>
                                                        &nbsp;{row.modem.id}
                                                    </TableCell>
                                                    <TableCell align="right">{row.is_connected ? 'ON' : 'OFF'}</TableCell>
                                                    <TableCell align="right">{row.external_ip ? row.external_ip : '-'}</TableCell>
                                                    <TableCell align="right">
                                                        {row.device_network_type ? row.device_network_type : '-'}
                                                    </TableCell>
                                                    <TableCell align="right">
                                                        {row.device_network_provider ? row.device_network_provider : '-'}
                                                    </TableCell>
                                                    <TableCell align="right">
                                                        {row.device_network_signalbar ? row.device_network_signalbar : '-'}
                                                    </TableCell>
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
