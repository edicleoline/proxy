import { Grid } from '@mui/material';
import MainCard from 'ui-component/cards/MainCard';
import SubCard from 'ui-component/cards/SubCard';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import { useState, useEffect, useRef } from 'react';
import PropTypes from 'prop-types';
import * as React from 'react';
import { getDevices } from 'services/api/device';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import IconButton from '@mui/material/IconButton';
import { IconDotsVertical } from '@tabler/icons';
import ProxyUsersActions from './actions';

const ProxyUsers = () => {
    const [tableMaxHeight, setTableMaxHeight] = useState(null);
    const _resizeTable = () => {
        const mainElHeight = window.innerHeight;
        const max = mainElHeight - 205;
        setTableMaxHeight(max);
    };

    useEffect(() => {
        _resizeTable();

        window.addEventListener('resize', _resizeTable);

        return () => {
            window.removeEventListener('resize', _resizeTable);
        };
    }, []);

    const [loading, setLoading] = useState(false);
    const [devices, setDevices] = useState([]);

    const loadDevices = () => {
        setLoading(true);
        getDevices()
            .then(
                (response) => {
                    if (response.items) {
                        setDevices(response.items);
                    }
                },
                (err) => {
                    console.log('settings/device', err);
                }
            )
            .finally(() => {
                setLoading(false);
            });
    };

    useEffect(() => {
        loadDevices();
    }, []);

    const [anchorDeviceMenuEl, setAnchorDeviceMenuEl] = useState(null);
    const [openDeviceMenuElem, setOpenDeviceMenuElem] = useState(null);
    const handleDeviceOpenMenuClick = (elem) => (event) => {
        setAnchorDeviceMenuEl(event.currentTarget);
        setOpenDeviceMenuElem(elem);
    };
    const handleDeviceCloseMenu = () => {
        setAnchorDeviceMenuEl(null);
        setOpenDeviceMenuElem(null);
    };

    return (
        <MainCard title="Usuários" contentSX={{ padding: '0 !important' }} secondary={<ProxyUsersActions />}>
            <Grid container spacing={0}>
                <Grid item xs={12} sm={12}>
                    <SubCard contentSX={{ padding: '0 !important' }} sx={{ border: 'none 0', borderRadius: '0' }}>
                        <Grid container direction="column" spacing={0}>
                            <Grid item sx={{ maxWidth: '100% !important' }}>
                                <TableContainer component={Paper} sx={{ borderRadius: '0', maxHeight: tableMaxHeight }}>
                                    <Table stickyHeader sx={{ minWidth: 650 }} aria-label="devices table">
                                        <TableHead>
                                            <TableRow>
                                                <TableCell>Id</TableCell>
                                                <TableCell align="left">Nome</TableCell>
                                                <TableCell align="left">Login</TableCell>
                                                <TableCell align="left">Senha</TableCell>
                                            </TableRow>
                                        </TableHead>
                                        <TableBody>
                                            {devices.map((device) => (
                                                <TableRow hover key={device.id} sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
                                                    <TableCell component="th" scope="row" sx={{ minWidth: '100px', position: 'relative' }}>
                                                        <Grid container justifyContent="flex-start" alignItems="center" direction="row">
                                                            <Grid item>
                                                                <IconButton
                                                                    id={`device-button-${device.id}`}
                                                                    aria-label="Device Options"
                                                                    size="small"
                                                                    aria-controls={`device-menu-${device.id}`}
                                                                    aria-haspopup="true"
                                                                    onClick={handleDeviceOpenMenuClick(device.id)}
                                                                >
                                                                    <IconDotsVertical />
                                                                </IconButton>
                                                            </Grid>
                                                            <Grid item>{device.id}</Grid>
                                                        </Grid>
                                                        <Menu
                                                            id={`device-menu-${device.id}`}
                                                            anchorEl={anchorDeviceMenuEl}
                                                            open={openDeviceMenuElem === device.id}
                                                            onClose={handleDeviceCloseMenu}
                                                            MenuListProps={{
                                                                'aria-labelledby': `device-button-${device.id}`
                                                            }}
                                                        >
                                                            <MenuItem>Alterar</MenuItem>
                                                            <MenuItem>Excluir</MenuItem>
                                                        </Menu>
                                                    </TableCell>
                                                    <TableCell align="left">{device.model}</TableCell>
                                                    <TableCell align="left">{device.type}</TableCell>
                                                    <TableCell align="left">{device?.middleware?.name}</TableCell>
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

export default ProxyUsers;
