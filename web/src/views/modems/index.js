import * as React from 'react';

import { Grid, Box, Card, Typography } from '@mui/material';
import SubCard from 'ui-component/cards/SubCard';
import MainCard from 'ui-component/cards/MainCard';
import SecondaryAction from 'ui-component/cards/CardSecondaryAction';

import { useEffect, useState, useRef, useLayoutEffect, useMemo } from 'react';

import { getServer } from 'services/api/server';
import { stopRotate } from 'services/api/modem';

// import { bytesToSize } from 'utils/format';

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
import Badge from '@mui/material/Badge';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import cloneDeep from 'lodash/cloneDeep';

import PropTypes from 'prop-types';
import { FormattedMessage } from 'react-intl';

import { IconDotsVertical, IconAccessPoint, IconAccessPointOff } from '@tabler/icons';
import CloseIcon from '@mui/icons-material/Close';

import RotateDialog from 'ui-component/modem/Rotate';
import AutoRotateInfoDialog from 'ui-component/modem/AutoRotateInfoDialog';
import RebootDialog from 'ui-component/modem/Reboot';
import SettingsDialog from 'ui-component/modem/Settings';
import DiagnoseDialog from 'ui-component/modem/Diagnose';
import { Dock, DockItemState } from 'ui-component/Dockmodal';
import ModemLog from 'ui-component/ModemLog';

import { storeModemLog, modemLog } from 'storage/modem/log';
import { useLiveQuery } from 'dexie-react-hooks';

import { testProxyIPv4HTTP } from 'utils/proxy';

import io from 'socket.io-client';
import objectHash from 'object-hash';

import config from 'config';
import styled from 'styled-components';

import ModemStatus from 'views/modems/ModemStatus';
import ModemAutoRotateFlag from 'views/modems/ModemAutoRotateFlag';
import ProxyConnection from 'views/modems/ProxyConnection';
import DataUsage from 'views/modems/DataUsage';
import SignalBar from 'views/modems/SignalBar';

const ModemIdWrapper = styled.div`
    position: relative;
`;

const Modems = () => {
    // const [isLoading, setLoading] = useState(true);

    const [server, setServer] = useState([]);
    const loadServer = () => {
        getServer().then(
            (response) => {
                setServer(response);
            },
            (error) => console.log('server error', error)
        );
    };

    const [tableMaxHeight, setTableMaxHeight] = useState(null);
    const _resizeTable = () => {
        const mainElHeight = window.innerHeight;
        const max = mainElHeight - 205;
        setTableMaxHeight(max);
    };

    useEffect(() => {
        loadServer();
        _resizeTable();

        window.addEventListener('resize', _resizeTable);

        return () => {
            window.removeEventListener('resize', _resizeTable);
        };
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
        // console.log('lets test modem-ipv4');

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

    const _serverControl = useRef(null);

    useEffect(() => {
        const socket = io(config.socketio.baseURL);

        socket.on('connect', () => {
            setSocketConnected(true);
            console.log('socket.io: connected');
        });

        socket.on('disconnect', () => {
            setSocketConnected(false);
            console.log('socket.io: disconnected');
        });

        socket.on('modem_log', (message) => {
            // console.log('socket.io server: message', message);
            handleStoreModemLog(message);
        });

        socket.on('server_control', (serverControl) => {
            // console.log(serverControl);
            _serverControl.current = serverControl;
        });

        socket.on('modems', (items) => {
            // console.log('socket.io server: modems', items);
            const itemsHash = objectHash.MD5(items);

            if (!_modems.current || (_serverControl.current && _serverControl.current.action === 'reload_modems')) {
                _modems.current = items;
                _modemsHash.current = itemsHash;
                setModems(_modems.current);
                if (_serverControl.current && _serverControl.current.action === 'reload_modems') {
                    _serverControl.current = null;
                }
            } else {
                if (_modemsHash.current !== itemsHash) {
                    let changed = false;
                    const remodems = _modems.current.map(function (modem) {
                        items.forEach((item) => {
                            if (modem.id !== item.id) {
                                return;
                            }

                            if (
                                _serverControl.current &&
                                _serverControl.current.action === 'reload_modem' &&
                                _serverControl.current.id == item.id
                            ) {
                                _serverControl.current = null;
                                modem = item;
                                changed = true;
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

                            if (modem.lock !== item.lock) {
                                changed = true;
                                modem.lock = item.lock;
                            }

                            if (
                                (!modem.schedule && item.schedule) ||
                                (modem.schedule && !item.schedule) ||
                                objectHash.MD5(modem.schedule) != objectHash.MD5(item.schedule)
                            ) {
                                if (item.schedule?.time_left_to_run <= 30 || item.schedule?.added_at != modem.schedule?.added_at) {
                                    modem.schedule = item.schedule;
                                    changed = true;
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
                // console.log('new modems_details hash', hash);
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
                            // console.log('remodem', modemDetail);
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

    const handleCancelModemChangeIPClick = (modem) => {
        stopRotate(modem.id)
            .then(
                (response) => {
                    console.log(response);
                },
                (err) => {
                    const message =
                        err.response && err.response.data && err.response.data.error && err.response.data.error.message
                            ? err.response.data.error.message
                            : err.message;
                    /*setError({
                        ...error,
                        open: true,
                        message: <FormattedMessage id="app.components.modem.Rotate.error" values={{ modemId: modem.id, error: message }} />
                    });*/
                }
            )
            .finally(() => {
                //console.log();
            });
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

    // const dockLog = useMemo(() => <Dock items={dockLogItems} />, []);
    const _dockLogItems = useRef([]);

    const addDockLog = (modem) => {
        const index = _dockLogItems.current.map((item) => item.id).indexOf(modem.modem.id);
        if (index > -1) {
            return false;
        }

        _dockLogItems.current.push({
            id: modem.modem.id,
            title: `Log modem ${modem.modem.id}`,
            content: <ModemLog modem={modem} />,
            state: DockItemState.maximized
        });
        setDockLogItems(_dockLogItems.current);

        return true;
    };

    const handleCloseDock = (item) => {
        const copy = [..._dockLogItems.current];
        const index = copy.map((item) => item.id).indexOf(item.id);
        copy.splice(index, 1);
        _dockLogItems.current = copy;
        setDockLogItems(copy);
    };

    const [dockLogItems, setDockLogItems] = useState(_dockLogItems.current);

    const handleStoreModemLog = (log) => {
        storeModemLog(log);
    };

    const [taskStoppingHelpDialog, setTaskStoppingHelpDialog] = useState({
        open: false,
        title: '',
        description: ''
    });

    const [autoRotateInfoModem, setAutoRotateInfoModem] = useState(null);
    const [autoRotateInfoOpen, setAutoRotateInfoOpen] = useState(false);

    const handleModemAutoRotateFlagClick = (modem) => (event) => {
        setAutoRotateInfoModem(modem);
        setAutoRotateInfoOpen(true);
    };

    const handleAutoRotateInfoOnClose = () => {
        setAutoRotateInfoOpen(false);
        setAutoRotateInfoModem(null);
    };

    useEffect(() => {
        if (modems && autoRotateInfoModem) {
            modems.forEach((modem) => {
                if (modem.id === autoRotateInfoModem.id) {
                    setAutoRotateInfoModem(cloneDeep(modem));
                    return false;
                }
            });
        }
    }, [modems]);

    return (
        <MainCard
            title="Modems"
            contentClass={'test'}
            secondary={<SecondaryAction link="https://next.material-ui.com/system/typography/" />}
            contentSX={{ padding: '0 !important' }}
            sx={{ maxHeight: '900px' }}
            id="modems-main-paper"
        >
            <Grid container spacing={0}>
                <Grid item xs={12} sm={12}>
                    <SubCard contentSX={{ padding: '0 !important' }} sx={{ border: 'none 0', borderRadius: '0' }}>
                        <Grid container direction="column" spacing={0}>
                            <Grid item sx={{ maxWidth: '100% !important' }}>
                                <TableContainer component={Paper} sx={{ borderRadius: '0', maxHeight: tableMaxHeight }}>
                                    <Table stickyHeader sx={{ minWidth: 650 }} aria-label="modems table">
                                        <TableHead>
                                            <TableRow>
                                                <TableCell>Modem</TableCell>
                                                <TableCell align="left">Modelo</TableCell>
                                                <TableCell align="left">Porta</TableCell>
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
                                                    <TableCell component="th" scope="row" sx={{ minWidth: '100px', position: 'relative' }}>
                                                        <Grid container justifyContent="flex-start" alignItems="center" direction="row">
                                                            <Grid item>
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
                                                            </Grid>
                                                            <Grid item>
                                                                <ModemIdWrapper>
                                                                    {row.auto_rotate == true ? (
                                                                        <ModemAutoRotateFlag
                                                                            modem={row}
                                                                            onAutoRotateIconClick={handleModemAutoRotateFlagClick}
                                                                        />
                                                                    ) : null}
                                                                    &nbsp;&nbsp;{row.modem.id}
                                                                </ModemIdWrapper>
                                                            </Grid>
                                                        </Grid>
                                                        <Menu
                                                            id={`modem-menu-${row.modem.id}`}
                                                            anchorEl={anchorModemMenuEl}
                                                            open={openModemMenuElem === row.modem.id}
                                                            onClose={handleModemCloseMenu}
                                                            MenuListProps={{
                                                                'aria-labelledby': `modem-button-${row.modem.id}`
                                                            }}
                                                        >
                                                            {row.lock != null && row.lock.task && row.lock.task.name == 'ROTATE' ? (
                                                                <MenuItem
                                                                    onClick={() => {
                                                                        handleCancelModemChangeIPClick(row);
                                                                        handleModemCloseMenu();
                                                                    }}
                                                                    disabled={row.lock && row.lock.task && row.lock.task.stopping == true}
                                                                >
                                                                    Cancelar rotacionamento
                                                                </MenuItem>
                                                            ) : (
                                                                <MenuItem
                                                                    onClick={() => {
                                                                        handleModemChangeIPClick(row);
                                                                        handleModemCloseMenu();
                                                                    }}
                                                                    disabled={!row.is_connected || row.lock != null}
                                                                >
                                                                    Rotacionar IP
                                                                </MenuItem>
                                                            )}
                                                            <MenuItem
                                                                onClick={() => {
                                                                    handleModemRebootClick(row);
                                                                    handleModemCloseMenu();
                                                                }}
                                                                disabled={row.lock != null}
                                                            >
                                                                Reiniciar
                                                            </MenuItem>
                                                            <Divider />
                                                            <MenuItem
                                                                onClick={() => {
                                                                    handleModemDiagnoseClick(row);
                                                                    handleModemCloseMenu();
                                                                }}
                                                                disabled={row.lock != null}
                                                            >
                                                                Executar diagnóstico
                                                            </MenuItem>
                                                            <MenuItem
                                                                onClick={() => {
                                                                    handleModemCloseMenu();
                                                                    addDockLog(row);
                                                                }}
                                                            >
                                                                Log
                                                            </MenuItem>
                                                            <MenuItem
                                                                onClick={() => {
                                                                    handleModemSettingsClick(row);
                                                                    handleModemCloseMenu();
                                                                }}
                                                            >
                                                                Configurações
                                                            </MenuItem>
                                                            <Divider />
                                                            <MenuItem
                                                                onClick={() => {
                                                                    console.log('modem turn off');
                                                                    handleModemCloseMenu();
                                                                }}
                                                            >
                                                                Desligar
                                                            </MenuItem>
                                                        </Menu>
                                                    </TableCell>
                                                    <TableCell align="left">{row.modem.device.model}</TableCell>
                                                    <TableCell align="left">{row.usb.port}</TableCell>
                                                    <TableCell align="left" sx={{ position: 'relative' }}>
                                                        <ModemStatus
                                                            lock={row.lock}
                                                            connected={row.is_connected}
                                                            onStoppingTaskClick={() => {
                                                                setTaskStoppingHelpDialog({
                                                                    ...taskStoppingHelpDialog,
                                                                    open: true,
                                                                    title: (
                                                                        <FormattedMessage id="app.components.modem.Task.help.stopping.title" />
                                                                    ),
                                                                    description: (
                                                                        <FormattedMessage id="app.components.modem.Task.help.stopping.description" />
                                                                    )
                                                                });
                                                            }}
                                                        />
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
                                                                justifyContent="flex-start"
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
                                                                justifyContent="flex-start"
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
                                                        {row.data && row.data.receive ? (
                                                            <DataUsage
                                                                download={row.data.receive.formatted}
                                                                upload={row.data.transmit.formatted}
                                                            />
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
            <RotateDialog
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
            <Dialog
                open={taskStoppingHelpDialog.open}
                onClose={() => {
                    setTaskStoppingHelpDialog({
                        ...taskStoppingHelpDialog,
                        open: false
                    });
                }}
                aria-labelledby="dialog-stopping-task"
                aria-describedby="dialog-stopping-task-description"
                fullWidth={true}
            >
                <DialogTitle id="dialog-stopping-task-title">
                    <Typography variant="h3" component="span" sx={{ fontWeight: '500' }}>
                        {taskStoppingHelpDialog.title}
                    </Typography>
                </DialogTitle>
                <DialogContent>
                    <DialogContentText id="dialog-stopping-task-description" sx={{ whiteSpace: 'pre-line' }}>
                        {taskStoppingHelpDialog.description}
                    </DialogContentText>
                </DialogContent>
                <DialogActions>
                    <Button
                        onClick={() => {
                            setTaskStoppingHelpDialog({
                                ...taskStoppingHelpDialog,
                                open: false
                            });
                        }}
                    >
                        OK
                    </Button>
                </DialogActions>
            </Dialog>
            <Dock items={dockLogItems} onClose={handleCloseDock} />
            {/* {dockLog} */}
            <AutoRotateInfoDialog modem={autoRotateInfoModem} open={autoRotateInfoOpen} onClose={handleAutoRotateInfoOnClose} />
        </MainCard>
    );
};

export default Modems;
