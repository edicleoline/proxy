import { Grid, Box, Card, Typography } from '@mui/material';
import SubCard from 'ui-component/cards/SubCard';
import MainCard from 'ui-component/cards/MainCard';
import SecondaryAction from 'ui-component/cards/CardSecondaryAction';

import { useEffect, useState, useRef } from 'react';

import { getServer } from 'services/api/server';
import { stopRotate } from 'services/api/modem';

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
import Popover from '@mui/material/Popover';
import { FormattedMessage } from 'react-intl';
import { IconDotsVertical } from '@tabler/icons';
import RotateDialog from 'ui-component/modem/Rotate';
import AutoRotateInfo from 'ui-component/modem/AutoRotateInfo';
import RebootDialog from 'ui-component/modem/Reboot';
import SettingsDialog from 'ui-component/modem/Settings';
import DiagnoseDialog from 'ui-component/modem/Diagnose';
import DockItemState from 'ui-component/Dock/DockItemState';
import { Dock } from 'ui-component/Dock';
import ModemLog from 'ui-component/ModemLog';
import cloneDeep from 'lodash/cloneDeep';
import { testProxyIPv4HTTP } from 'utils/proxy';

import config from 'config';
import styled from 'styled-components';

import ModemStatus from './ModemStatus';
import ModemAutoRotateFlag from './ModemAutoRotateFlag';
import ProxyConnection from './ProxyConnection';
import DataUsage from './DataUsage';
import SignalBar from './SignalBar';

import { useSelector } from 'react-redux';

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

    const _modems = useSelector((state) => state.modems);
    const _modemsDetails = useSelector((state) => state.modemsDetails);

    useEffect(() => {
        // console.log('UPDATED MODEMS ITEMS!', _modems);
        setModems(_modems.items);
    }, [_modems]);

    useEffect(() => {
        // console.log('UPDATED MODEMS___DETAILS ITEMS!', _modems);
        _modems.items.map((modem) => {
            _modemsDetails.items.forEach((modemDetail) => {
                if (modem.modem.id === modemDetail.modem.id) {
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
    }, [_modemsDetails]);

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
        /*const remodems = _modems.current.map(function (item) {
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
        setModems(_modems.current);*/
    };

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

    const [modemRotateDialog, setModemRotateDialog] = useState({
        open: false,
        modem: null
    });
    const handleModemRotateClick = (modem) => {
        setModemRotateDialog({
            open: true,
            modem: modem
        });
    };
    const handleModemRotateClose = () => {
        setModemRotateDialog({ ...modemRotateDialog, open: false });
    };

    const handleCancelModemRotateClick = (modem) => {
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
        const dockItemIndex = _dockLogItems.current.findIndex((item) => item.id == modem.modem.id);
        if (dockItemIndex > -1) {
            _dockLogItems.current[dockItemIndex].state = DockItemState.maximized;
            setDockLogItems(_dockLogItems.current);
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

    const [taskStoppingHelpDialog, setTaskStoppingHelpDialog] = useState({
        open: false,
        title: '',
        description: ''
    });

    const [autoRotateInfoAnchorEl, setAutoRotateInfoAnchorEl] = useState(null);

    const autoRotateInfoHandleClose = () => {
        setAutoRotateInfoAnchorEl(null);
    };
    const autoRotateInfoOpen = Boolean(autoRotateInfoAnchorEl);
    const autoRotateInfoPopoverId = autoRotateInfoOpen ? 'simple-popover' : undefined;

    const [autoRotateInfoModem, setAutoRotateInfoModem] = useState(null);

    const handleModemAutoRotateFlagClick = (modem) => (event) => {
        setAutoRotateInfoModem(modem);
        setAutoRotateInfoAnchorEl(event.currentTarget);
    };

    useEffect(() => {
        if (modems && autoRotateInfoModem) {
            setAutoRotateInfoModem(modems.find((modem) => modem.id == autoRotateInfoModem.id));
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
                                            {modems.map((modem) => (
                                                <TableRow
                                                    hover
                                                    key={modem.modem.id}
                                                    sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                                                >
                                                    <TableCell component="th" scope="row" sx={{ minWidth: '100px', position: 'relative' }}>
                                                        <Grid container justifyContent="flex-start" alignItems="center" direction="row">
                                                            <Grid item>
                                                                <IconButton
                                                                    id={`modem-button-${modem.modem.id}`}
                                                                    aria-label="Modem Options"
                                                                    size="small"
                                                                    aria-controls={`modem-menu-${modem.modem.id}`}
                                                                    aria-haspopup="true"
                                                                    onClick={handleModemOpenMenuClick(modem.modem.id)}
                                                                >
                                                                    <IconDotsVertical />
                                                                </IconButton>
                                                            </Grid>
                                                            <Grid item>
                                                                <ModemIdWrapper>
                                                                    {modem.auto_rotate == true ? (
                                                                        <ModemAutoRotateFlag
                                                                            modem={modem}
                                                                            onAutoRotateIconClick={handleModemAutoRotateFlagClick}
                                                                        />
                                                                    ) : null}
                                                                    &nbsp;&nbsp;{modem.modem.id}
                                                                </ModemIdWrapper>
                                                            </Grid>
                                                        </Grid>
                                                        <Menu
                                                            id={`modem-menu-${modem.modem.id}`}
                                                            anchorEl={anchorModemMenuEl}
                                                            open={openModemMenuElem === modem.modem.id}
                                                            onClose={handleModemCloseMenu}
                                                            MenuListProps={{
                                                                'aria-labelledby': `modem-button-${modem.modem.id}`
                                                            }}
                                                        >
                                                            {modem.lock != null && modem.lock.task && modem.lock.task.name == 'ROTATE' ? (
                                                                <MenuItem
                                                                    onClick={() => {
                                                                        handleCancelModemRotateClick(modem);
                                                                        handleModemCloseMenu();
                                                                    }}
                                                                    disabled={
                                                                        modem.lock && modem.lock.task && modem.lock.task.stopping == true
                                                                    }
                                                                >
                                                                    Cancelar rotacionamento
                                                                </MenuItem>
                                                            ) : (
                                                                <MenuItem
                                                                    onClick={() => {
                                                                        handleModemRotateClick(modem);
                                                                        handleModemCloseMenu();
                                                                    }}
                                                                    disabled={!modem.is_connected || modem.lock != null}
                                                                >
                                                                    Rotacionar IP
                                                                </MenuItem>
                                                            )}
                                                            <MenuItem
                                                                onClick={() => {
                                                                    handleModemRebootClick(modem);
                                                                    handleModemCloseMenu();
                                                                }}
                                                                disabled={modem.lock != null}
                                                            >
                                                                Reiniciar
                                                            </MenuItem>
                                                            <Divider />
                                                            <MenuItem
                                                                onClick={() => {
                                                                    handleModemDiagnoseClick(modem);
                                                                    handleModemCloseMenu();
                                                                }}
                                                                disabled={modem.lock != null}
                                                            >
                                                                Executar diagnóstico
                                                            </MenuItem>
                                                            <MenuItem
                                                                onClick={() => {
                                                                    handleModemCloseMenu();
                                                                    addDockLog(modem);
                                                                }}
                                                            >
                                                                Log
                                                            </MenuItem>
                                                            <MenuItem
                                                                onClick={() => {
                                                                    handleModemSettingsClick(modem);
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
                                                    <TableCell align="left">{modem.modem.device.model}</TableCell>
                                                    <TableCell align="left">{modem.usb.port}</TableCell>
                                                    <TableCell align="left" sx={{ position: 'relative' }}>
                                                        <ModemStatus
                                                            lock={modem.lock}
                                                            connected={modem.is_connected}
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
                                                    <TableCell align="left">{modem.external_ip ? modem.external_ip : '-'}</TableCell>
                                                    <TableCell align="right">
                                                        {modem.device_network_provider ? modem.device_network_provider : '-'}
                                                    </TableCell>
                                                    <TableCell align="right">
                                                        {modem.device_network_type ? modem.device_network_type : '-'}
                                                    </TableCell>
                                                    <TableCell align="center">
                                                        {modem.device_network_signalbar ? (
                                                            <SignalBar signal={modem.device_network_signalbar} />
                                                        ) : (
                                                            <SignalBar signal={0} />
                                                        )}
                                                    </TableCell>
                                                    <TableCell align="left">
                                                        {modem.external_ip && modem.proxy ? (
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
                                                                            port={modem.proxy.ipv4.http.port}
                                                                            status={modem.proxy.ipv4.http.status}
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
                                                                            port={modem.proxy.ipv4.socks.port}
                                                                            status={modem.proxy.ipv4.socks.status}
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
                                                        {modem.external_ip && modem.proxy ? (
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
                                                                            port={modem.proxy.ipv6.http.port}
                                                                            status={modem.proxy.ipv6.http.status}
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
                                                                            port={modem.proxy.ipv6.socks.port}
                                                                            status={modem.proxy.ipv6.socks.status}
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
                                                        {modem.data && modem.data.receive ? (
                                                            <DataUsage
                                                                download={modem.data.receive.formatted}
                                                                upload={modem.data.transmit.formatted}
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
                open={modemRotateDialog.open}
                modem={modemRotateDialog.modem}
                onClose={handleModemRotateClose}
                onConfirm={handleModemRotateClose}
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
            <Popover
                id={autoRotateInfoPopoverId}
                open={autoRotateInfoOpen}
                anchorEl={autoRotateInfoAnchorEl}
                onClose={autoRotateInfoHandleClose}
                anchorOrigin={{
                    vertical: 'bottom',
                    horizontal: 'left'
                }}
            >
                <AutoRotateInfo modem={autoRotateInfoModem} open={autoRotateInfoOpen} onClose={autoRotateInfoHandleClose} />
            </Popover>
        </MainCard>
    );
};

export default Modems;
