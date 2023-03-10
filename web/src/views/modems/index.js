import { Grid, Box, Card, Typography } from '@mui/material';

// project imports
import SubCard from 'ui-component/cards/SubCard';
import MainCard from 'ui-component/cards/MainCard';
import SecondaryAction from 'ui-component/cards/CardSecondaryAction';

import { useEffect, useState } from 'react';

import { getServer } from 'services/api/server';
import { getModem, getModems, reboot } from 'services/api/server/modem';

import { bytesToSize } from 'utils/format';

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
import Divider from '@mui/material/Divider';
import IconButton from '@mui/material/IconButton';

import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import PropTypes from 'prop-types';

import { IconDotsVertical, IconAccessPoint, IconAccessPointOff } from '@tabler/icons';
import { IconAntennaBars1, IconAntennaBars2, IconAntennaBars3, IconAntennaBars4, IconAntennaBars5 } from '@tabler/icons';
import CloseIcon from '@mui/icons-material/Close';

import ChangeDialog from 'ui-component/modem/ip/Change';
import RebootDialog from 'ui-component/modem/Reboot';
import SettingsDialog from 'ui-component/modem/Settings';
import DiagnoseDialog from 'ui-component/modem/Diagnose';

import io from 'socket.io-client';
import objectHash from 'object-hash';

const Modems = () => {
    // const [isLoading, setLoading] = useState(true);

    const [server, setServer] = useState([]);
    const loadServer = () => {
        getServer().then(
            (response) => {
                console.log(response);
                setServer(response);
            },
            (error) => console.log('server error', error)
        );
    };

    // const [modems, setModems] = useState([]);
    // const loadModems = () => {
    //     getModems().then(
    //         (items) => {
    //             // console.log(items);
    //             setModems(items);
    //             loadModemsDetails(items);
    //         },
    //         (error) => console.log('modems error', error)
    //     );
    // };

    // const loadModemsDetails = (items) => {
    //     items.map(function (item) {
    //         getModem(item.modem.id).then(
    //             (modem) => {
    //                 const remodems = items.map(function (m) {
    //                     if (m.modem.id == modem.modem.id) {
    //                         m.external_ip = modem.external_ip_through_device;
    //                         m.device_network_type = modem.device_network_type;
    //                         m.device_network_provider = modem.device_network_provider;
    //                         m.device_network_signalbar = modem.device_network_signalbar;
    //                         m.data = modem.data;
    //                     }
    //                     return m;
    //                 });
    //                 setModems(remodems);
    //                 // console.log(item.modem.id, remodems);
    //             },
    //             (error) => console.log('modem error', error)
    //         );
    //     });
    // };

    useEffect(() => {
        loadServer();
        // loadModems();
    }, []);

    const [modems, setModems] = useState([]);
    let modemsHash = null;

    const socket = io('http://127.0.0.1:5000');
    const [socketConnected, setSocketConnected] = useState(socket.connected);
    // const [lastPong, setLastPong] = useState(null);

    useEffect(() => {
        socket.on('connect', () => {
            setSocketConnected(true);
            console.log('socket.io: connected');
        });

        socket.on('disconnect', () => {
            setSocketConnected(false);
            console.log('socket.io: disconnected');
        });

        // socket.on('pong', () => {
        //     setLastPong(new Date().toISOString());
        // });

        socket.on('message', (message) => {
            console.log('socket.io server: message', message);
        });

        socket.on('modems', (items) => {
            // console.log('socket.io server: modems', items);
            const hash = objectHash.MD5(items);
            if (!modemsHash || modemsHash !== hash) {
                console.log('new modems hash', hash);
                modemsHash = hash;
                setModems(items);
            }
        });

        socket.on('modems_details', (items) => {
            console.log('socket.io server: modems_details', items);
            // const hash = objectHash.MD5(items);
            // if (!modemsHash || modemsHash !== hash) {
            //     console.log('new modems hash', hash);
            //     modemsHash = hash;
            //     setModems(items);
            // }
        });

        return () => {
            socket.off('connect');
            socket.off('disconnect');
            socket.off('pong');
        };
    }, []);

    const [anchorModemMenuEl, setAnchorModemMenuEl] = useState(null);
    const [openModemMenuElem, setOpenModemMenuElem] = useState(null);
    const handleModemOpenMenuClick = (elem) => (event) => {
        setAnchorModemMenuEl(event.currentTarget);
        setOpenModemMenuElem(elem);
    };
    const handleModemCloseMenu = () => {
        setAnchorModemMenuEl(null);
        setOpenModemMenuElem(null);
    };

    const [modemRebootDialog, setModemRebootDialog] = useState({
        open: false,
        modem: null
    });
    const handleModemRebootClick = (modem) => {
        setModemRebootDialog({
            open: true,
            modem: modem
        });
    };
    const handleModemRebootClose = () => {
        setModemRebootDialog({ ...modemRebootDialog, open: false });
    };

    const [modemChangeIPDialog, setModemChangeIPDialog] = useState({
        open: false,
        modem: null
    });
    const handleModemChangeIPClick = (modem) => {
        setModemChangeIPDialog({
            open: true,
            modem: modem
        });
    };
    const handleModemChangeIPClose = () => {
        setModemChangeIPDialog({ ...modemChangeIPDialog, open: false });
    };

    const [modemSettingsDialog, setModemSettingsDialog] = useState({
        open: false,
        modem: null
    });
    const handleModemSettingsClick = (modem) => {
        console.log(modem);
        setModemSettingsDialog({
            open: true,
            modem: modem
        });
    };
    const handleModemSettingsClose = () => {
        setModemSettingsDialog({ ...modemSettingsDialog, open: false });
    };

    const [modemDiagnoseDialog, setModemDiagnoseDialog] = useState({
        open: false,
        modem: null
    });
    const handleModemDiagnoseClick = (modem) => {
        console.log(modem);
        setModemDiagnoseDialog({
            open: true,
            modem: modem
        });
    };
    const handleModemDiagnoseClose = () => {
        setModemDiagnoseDialog({ ...modemDiagnoseDialog, open: false });
    };

    const ColorBox = ({ bgcolor, title, dark }) => (
        <>
            <Card sx={{ mb: 0 }}>
                <Box
                    sx={{
                        display: 'flex',
                        justifyContent: 'center',
                        alignItems: 'center',
                        p: 1,
                        bgcolor,
                        color: dark ? 'grey.800' : '#ffffff'
                    }}
                >
                    {title}
                </Box>
            </Card>
        </>
    );

    const ProxyConnection = ({ type, ip, port }) => (
        <>
            <div>
                <span>{type}</span>
                <span>/</span>
                <span>{ip}</span>
                <span>:</span>
                <span>{port}</span>
            </div>
        </>
    );

    const SignalBar = (data) => {
        const icons = {
            ['0']: <span>-</span>,
            ['1']: <IconAntennaBars1 title={data.signal} />,
            ['2']: <IconAntennaBars2 title={data.signal} />,
            ['3']: <IconAntennaBars3 title={data.signal} />,
            ['4']: <IconAntennaBars4 title={data.signal} />,
            ['5']: <IconAntennaBars5 title={data.signal} />
        };

        return icons[data.signal];
    };

    return (
        <MainCard
            title="Modems"
            contentClass={'test'}
            secondary={<SecondaryAction link="https://next.material-ui.com/system/typography/" />}
        >
            <Grid container spacing={0}>
                <Grid item xs={12} sm={12}>
                    <SubCard contentSX={{ padding: '0 !important' }}>
                        <Grid container direction="column" spacing={0}>
                            <Grid item>
                                <TableContainer component={Paper}>
                                    <Table sx={{ minWidth: 650 }} aria-label="modems table">
                                        <TableHead>
                                            <TableRow>
                                                <TableCell>Modem</TableCell>
                                                <TableCell align="left">Modelo</TableCell>
                                                <TableCell align="left">IMEI</TableCell>
                                                <TableCell align="left">Status</TableCell>
                                                <TableCell align="left">IP externo</TableCell>
                                                <TableCell align="right">Provedor</TableCell>
                                                <TableCell align="right">Rede</TableCell>
                                                <TableCell align="center">Sinal</TableCell>
                                                <TableCell align="left">Proxy IPv4</TableCell>
                                                <TableCell align="left">Proxy IPv6</TableCell>
                                                <TableCell align="right">Uso de dados</TableCell>
                                            </TableRow>
                                        </TableHead>
                                        <TableBody>
                                            {modems.map((row) => (
                                                <TableRow
                                                    hover
                                                    key={row.modem.id}
                                                    sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                                                >
                                                    <TableCell component="th" scope="row">
                                                        <IconButton
                                                            id={`modem-button-${row.modem.id}`}
                                                            aria-label="Modem Options"
                                                            size="small"
                                                            aria-controls={`modem-menu-${row.modem.id}`}
                                                            aria-haspopup="true"
                                                            onClick={handleModemOpenMenuClick(row.modem.id)}
                                                        >
                                                            <IconDotsVertical />
                                                        </IconButton>
                                                        <Menu
                                                            id={`modem-menu-${row.modem.id}`}
                                                            anchorEl={anchorModemMenuEl}
                                                            open={openModemMenuElem === row.modem.id}
                                                            onClose={handleModemCloseMenu}
                                                            MenuListProps={{
                                                                'aria-labelledby': `modem-button-${row.modem.id}`
                                                            }}
                                                        >
                                                            <MenuItem
                                                                onClick={() => {
                                                                    handleModemChangeIPClick(row);
                                                                    handleModemCloseMenu();
                                                                }}
                                                                disabled={row.is_connected}
                                                            >
                                                                Alterar IP
                                                            </MenuItem>
                                                            <MenuItem
                                                                onClick={() => {
                                                                    handleModemRebootClick(row);
                                                                    handleModemCloseMenu();
                                                                }}
                                                                disabled={false}
                                                            >
                                                                Reiniciar
                                                            </MenuItem>
                                                            <MenuItem
                                                                onClick={() => {
                                                                    handleModemDiagnoseClick(row);
                                                                    handleModemCloseMenu();
                                                                }}
                                                            >
                                                                Executar diagnóstico
                                                            </MenuItem>
                                                            <Divider />
                                                            <MenuItem
                                                                onClick={() => {
                                                                    handleModemSettingsClick(row);
                                                                    handleModemCloseMenu();
                                                                }}
                                                            >
                                                                Configurações
                                                            </MenuItem>
                                                        </Menu>
                                                        &nbsp;&nbsp;{row.modem.id}
                                                    </TableCell>
                                                    <TableCell align="left">{row.modem.device.model}</TableCell>
                                                    <TableCell align="left">{row.modem.imei}</TableCell>
                                                    <TableCell align="left">
                                                        {row.is_connected ? (
                                                            <ColorBox bgcolor={'success.light'} title="Conectado" dark />
                                                        ) : (
                                                            <ColorBox bgcolor={'orange.light'} title="Desconectado" dark />
                                                        )}
                                                    </TableCell>
                                                    <TableCell align="left">{row.external_ip ? row.external_ip : '-'}</TableCell>
                                                    <TableCell align="right">
                                                        {row.device_network_provider ? row.device_network_provider : '-'}
                                                    </TableCell>
                                                    <TableCell align="right">
                                                        {row.device_network_type ? row.device_network_type : '-'}
                                                    </TableCell>
                                                    <TableCell align="center">
                                                        {row.device_network_signalbar ? (
                                                            <SignalBar signal={row.device_network_signalbar} />
                                                        ) : (
                                                            <SignalBar signal={0} />
                                                        )}
                                                    </TableCell>
                                                    <TableCell align="left">
                                                        {row.proxy ? (
                                                            <Grid
                                                                container
                                                                justifyContent="space-between"
                                                                alignItems="start"
                                                                direction="column"
                                                            >
                                                                <Grid item>
                                                                    {server ? (
                                                                        <ProxyConnection
                                                                            type={'http'}
                                                                            ip={server.external_ip}
                                                                            port={row.proxy.ipv4.http.port}
                                                                        />
                                                                    ) : (
                                                                        <span>-</span>
                                                                    )}
                                                                </Grid>
                                                                <Grid item>
                                                                    {server ? (
                                                                        <ProxyConnection
                                                                            type={'socks'}
                                                                            ip={server.external_ip}
                                                                            port={row.proxy.ipv4.socks.port}
                                                                        />
                                                                    ) : (
                                                                        <span>-</span>
                                                                    )}
                                                                </Grid>
                                                            </Grid>
                                                        ) : (
                                                            <span>-</span>
                                                        )}
                                                    </TableCell>
                                                    <TableCell align="left">
                                                        {row.proxy ? (
                                                            <Grid
                                                                container
                                                                justifyContent="space-between"
                                                                alignItems="start"
                                                                direction="column"
                                                            >
                                                                <Grid item>
                                                                    {server ? (
                                                                        <ProxyConnection
                                                                            type={'http'}
                                                                            ip={server.external_ip}
                                                                            port={row.proxy.ipv6.http.port}
                                                                        />
                                                                    ) : (
                                                                        <span>-</span>
                                                                    )}
                                                                </Grid>
                                                                <Grid item>
                                                                    {server ? (
                                                                        <ProxyConnection
                                                                            type={'socks'}
                                                                            ip={server.external_ip}
                                                                            port={row.proxy.ipv6.socks.port}
                                                                        />
                                                                    ) : (
                                                                        <span>-</span>
                                                                    )}
                                                                </Grid>
                                                            </Grid>
                                                        ) : (
                                                            <span>-</span>
                                                        )}
                                                    </TableCell>
                                                    <TableCell align="right">
                                                        <Grid container justifyContent="space-between" alignItems="end" direction="column">
                                                            <Grid item>
                                                                {row.data && row.data.receive ? (
                                                                    <span>
                                                                        <span>Download&nbsp;</span>
                                                                        <span>{bytesToSize(row.data.receive.bytes)}</span>
                                                                    </span>
                                                                ) : (
                                                                    <span>-</span>
                                                                )}
                                                            </Grid>
                                                            <Grid item>
                                                                {row.data && row.data.transmit ? (
                                                                    <span>
                                                                        <span>Upload&nbsp;</span>
                                                                        <span>{bytesToSize(row.data.transmit.bytes)}</span>
                                                                    </span>
                                                                ) : (
                                                                    <span>-</span>
                                                                )}
                                                            </Grid>
                                                        </Grid>
                                                    </TableCell>
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
            <SettingsDialog
                open={modemSettingsDialog.open}
                modem={modemSettingsDialog.modem}
                onClose={handleModemSettingsClose}
                onConfirm={handleModemSettingsClose}
            />
            <ChangeDialog
                open={modemChangeIPDialog.open}
                modem={modemChangeIPDialog.modem}
                onClose={handleModemChangeIPClose}
                onConfirm={handleModemChangeIPClose}
            />
            <RebootDialog
                open={modemRebootDialog.open}
                modem={modemRebootDialog.modem}
                onClose={handleModemRebootClose}
                onConfirm={handleModemRebootClose}
            />
            <DiagnoseDialog
                open={modemDiagnoseDialog.open}
                modem={modemDiagnoseDialog.modem}
                onClose={handleModemDiagnoseClose}
                onConfirm={handleModemDiagnoseClose}
            />
        </MainCard>
    );
};

export default Modems;
