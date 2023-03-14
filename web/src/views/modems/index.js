import { Grid, Box, Card } from '@mui/material';

// project imports
import SubCard from 'ui-component/cards/SubCard';
import MainCard from 'ui-component/cards/MainCard';
import SecondaryAction from 'ui-component/cards/CardSecondaryAction';

import { useEffect, useState, useRef } from 'react';

import { getServer } from 'services/api/server';

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

import Tooltip from '@mui/material/Tooltip';

import PropTypes from 'prop-types';

import { IconDotsVertical, IconAccessPoint, IconAccessPointOff } from '@tabler/icons';
import { IconAntennaBars1, IconAntennaBars2, IconAntennaBars3, IconAntennaBars4, IconAntennaBars5 } from '@tabler/icons';
import { IconLink, IconUnlink, IconArrowUp, IconArrowDown } from '@tabler/icons';
import CloseIcon from '@mui/icons-material/Close';

import ChangeDialog from 'ui-component/modem/ip/Change';
import RebootDialog from 'ui-component/modem/Reboot';
import SettingsDialog from 'ui-component/modem/Settings';
import DiagnoseDialog from 'ui-component/modem/Diagnose';

import { testProxyIPv4HTTP } from 'utils/proxy';

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

    useEffect(() => {
        loadServer();
    }, []);

    const [modems, setModems] = useState([]);
    const _modems = useRef(null);
    const _modemsHash = useRef(null);

    const _modemsDetailsHash = useRef(null);

    const testProxies = (modem, ip) => {
        testModemProxyIPv4HTTP(modem, ip);

        // const remodems = _modems.current.map(function (item) {
        //     if (item.modem.id == modem.id) {
        //         item.proxy.ipv4.http.status = 'fail';
        //     }

        //     return item;
        // });

        // _modems.current = remodems;
        // setModems(_modems.current);
    };
    const testModemProxyIPv4HTTP = (modem, ip) => {
        console.log('lets test modem-ipv4');

        const remodems = _modems.current.map(function (item) {
            if (item.modem.id == modem.id) {
                if (item.modem.id == 5) {
                    item.proxy.ipv4.http.status = 'fail';
                } else {
                    item.proxy.ipv4.http.status = 'success';
                }
            }

            return item;
        });

        _modems.current = remodems;
        setModems(_modems.current);
    };

    const [socketConnected, setSocketConnected] = useState(false);

    useEffect(() => {
        const socket = io('http://192.168.15.20:5000');

        console.log('useeffect!!!!');

        socket.on('connect', () => {
            setSocketConnected(true);
            console.log('socket.io: connected');
        });

        socket.on('disconnect', () => {
            setSocketConnected(false);
            console.log('socket.io: disconnected');
        });

        socket.on('message', (message) => {
            console.log('socket.io server: message', message);
        });

        socket.on('my_response', (message) => {
            console.log('my_response', message);
        });

        socket.on('modems', (items) => {
            console.log('socket.io server: modems', items);
            const itemsHash = objectHash.MD5(items);

            if (!_modems.current) {
                _modems.current = items;
                _modemsHash.current = itemsHash;
                setModems(_modems.current);
            } else {
                if (_modemsHash.current !== itemsHash) {
                    let changed = false;
                    const remodems = _modems.current.map(function (modem) {
                        items.forEach((item) => {
                            if (modem.id !== item.id) {
                                return;
                            }

                            if (modem.is_connected !== item.is_connected) {
                                changed = true;
                                modem.is_connected = item.is_connected;

                                if (!modem.is_connected) {
                                    delete modem.external_ip;
                                    delete modem.device_network_type;
                                    delete modem.device_network_provider;
                                    delete modem.device_network_signalbar;
                                    delete modem.data;
                                }
                            }
                        });

                        return modem;
                    });

                    _modemsHash.current = itemsHash;
                    if (changed) {
                        _modems.current = remodems;
                        setModems(_modems.current);
                    }
                }
            }
        });

        socket.on('modems_details', (items) => {
            console.log('socket.io server: modems_details', items);
            const hash = objectHash.MD5(items);
            if (_modems.current && (!_modemsDetailsHash.current || _modemsDetailsHash.current !== hash)) {
                console.log('new modems_details hash', hash);
                _modemsDetailsHash.current = hash;

                const _remodems = _modems.current.map(function (modem) {
                    items.forEach((modemDetail) => {
                        if (modem.modem.id === modemDetail.modem.id) {
                            modem.is_connected = modemDetail.is_connected;
                        }
                    });
                    return modem;
                });
                _modemsHash.current = objectHash.MD5(_remodems);

                const remodems = _modems.current.map(function (modem) {
                    items.forEach((modemDetail) => {
                        if (modem.modem.id === modemDetail.modem.id) {
                            console.log('remodem', modemDetail);
                            modem.device_network_type = modemDetail.device_network_type;
                            modem.device_network_provider = modemDetail.device_network_provider;
                            modem.device_network_signalbar = modemDetail.device_network_signalbar;
                            modem.data = modemDetail.data;

                            if (modem.external_ip !== modemDetail.external_ip_through_device) {
                                testProxies(modem, modemDetail.external_ip_through_device);
                            }

                            modem.external_ip = modemDetail.external_ip_through_device;
                        }
                    });
                    return modem;
                });

                _modems.current = remodems;
                setModems(remodems);
            }
        });

        return () => {
            socket.off('connect');
            socket.off('disconnect');
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

    const ProxyConnection = ({ type, ip, port, status }) => {
        let icon = '';

        if (status === 'fail') {
            icon = (
                <Tooltip title="Desconectado">
                    <div>
                        <IconUnlink size={14} style={{ position: 'relative', top: 1, marginRight: 2, color: '#c62828' }} />
                    </div>
                </Tooltip>
            );
        } else if (status === 'success') {
            icon = (
                <Tooltip title="Conectado">
                    <div>
                        <IconLink size={14} style={{ position: 'relative', top: 1, marginRight: 2, color: '#00c853' }} />
                    </div>
                </Tooltip>
            );
        }

        return (
            <>
                <Grid container justifyContent="space-between" alignItems="end" direction="row" sx={{ p: 0.2, px: 0.8, borderRadius: 1 }}>
                    <Grid item>{icon}</Grid>
                    <Grid item>{type}</Grid>
                    <Grid item>/</Grid>
                    <Grid item>{ip}</Grid>
                    <Grid item>:</Grid>
                    <Grid item>{port}</Grid>
                </Grid>
            </>
        );
    };

    const DataUsage = ({ download, upload }) => {
        return (
            <>
                <Grid container justifyContent="space-between" alignItems="end" direction="column">
                    <Grid item>
                        <Grid container justifyContent="end" alignItems="end" direction="row" sx={{ p: 0.2, px: 0, borderRadius: 1 }}>
                            <Grid item>
                                <Tooltip title="Download">
                                    <div>
                                        <IconArrowDown size={14} style={{ position: 'relative', top: 1, marginRight: 2 }} />
                                    </div>
                                </Tooltip>
                            </Grid>
                            <Grid item>{bytesToSize(download)}</Grid>
                        </Grid>
                    </Grid>
                    <Grid item>
                        <Grid container justifyContent="end" alignItems="end" direction="row" sx={{ p: 0.2, px: 0, borderRadius: 1 }}>
                            <Grid item>
                                <Tooltip title="Upload">
                                    <div>
                                        <IconArrowUp size={14} style={{ position: 'relative', top: 1, marginRight: 2 }} />
                                    </div>
                                </Tooltip>
                            </Grid>
                            <Grid item>{bytesToSize(upload)}</Grid>
                        </Grid>
                    </Grid>
                </Grid>
            </>
        );
    };

    const SignalBar = ({ signal }) => {
        const icons = {
            ['0']: <span>-</span>,
            ['1']: <IconAntennaBars1 title={signal} />,
            ['2']: <IconAntennaBars2 title={signal} />,
            ['3']: <IconAntennaBars3 title={signal} />,
            ['4']: <IconAntennaBars4 title={signal} />,
            ['5']: <IconAntennaBars5 title={signal} />
        };

        return icons[signal];
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
                                                        {row.external_ip && row.proxy ? (
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
                                                                            status={row.proxy.ipv4.http.status}
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
                                                                            status={row.proxy.ipv4.socks.status}
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
                                                        {row.external_ip && row.proxy ? (
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
                                                                            status={row.proxy.ipv6.http.status}
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
                                                                            status={row.proxy.ipv6.socks.status}
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
                                                        {/* <Grid container justifyContent="space-between" alignItems="end" direction="column">
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
                                                        </Grid> */}
                                                        {row.data && row.data.receive ? (
                                                            <DataUsage download={row.data.receive.bytes} upload={row.data.transmit.bytes} />
                                                        ) : (
                                                            <span>-</span>
                                                        )}
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
