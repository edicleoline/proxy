import { Grid, Box, Card, Typography } from '@mui/material';
import Button from '@mui/material/Button';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import TextField from '@mui/material/TextField';
import Stack from '@mui/material/Stack';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import Switch from '@mui/material/Switch';
import FormControlLabel from '@mui/material/FormControlLabel';
import FormGroup from '@mui/material/FormGroup';
import InputAdornment from '@mui/material/InputAdornment';
import FormHelperText from '@mui/material/FormHelperText';
import Visibility from '@mui/icons-material/Visibility';
import VisibilityOff from '@mui/icons-material/VisibilityOff';
import OutlinedInput from '@mui/material/OutlinedInput';
import Divider from '@mui/material/Divider';
import { useState, useEffect, useRef } from 'react';
import PropTypes from 'prop-types';
import { BootstrapDialogTitle, BootstrapDialogActions } from 'ui-component/extended/BootstrapDialog';
import { IpFilter } from 'ui-component/IpFilter';
import { saveModem } from 'services/api/modem';
import cloneDeep from 'lodash/cloneDeep';
import objectHash from 'object-hash';
import DeviceSelector from 'ui-component/device/Selector';
import ModemPortSelector from 'ui-component/modem-port/Selector';

const SettingsDialog = (props) => {
    const { modem, open, onClose, onConfirm, ...other } = props;

    const [_modem, _setModem] = useState(cloneDeep(modem));
    const [_originalModemHash, _setOriginalModemHash] = useState(null);
    const [_modemChanged, _setModemChanged] = useState(false);

    useEffect(() => {
        const m = cloneDeep(modem);
        _setModem(m);

        _setOriginalModemHash(objectHash.MD5(m));
        _setModemChanged(false);
    }, [modem]);

    const handleChangeProxyIpv4Http = (port) => {
        const http = { ..._modem.proxy.ipv4.http };
        http.port = parseInt(port);
        const cloned = cloneDeep(_modem);
        cloned.proxy.ipv4.http = http;
        _setModem(cloned);
    };

    const handleChangeProxyIpv4Socks = (port) => {
        const socks = { ..._modem.proxy.ipv4.socks };
        socks.port = parseInt(port);
        const cloned = cloneDeep(_modem);
        cloned.proxy.ipv4.socks = socks;
        _setModem(cloned);
    };

    const handleChangeModemAddrId = (addrId) => {
        const modem = { ..._modem.modem };
        modem.addr_id = addrId;
        const cloned = cloneDeep(_modem);
        cloned.modem = modem;
        _setModem(cloned);
    };

    const handleChangePort = (port) => {
        const modem = { ..._modem.modem };
        modem.usb = { id: port.id };
        const cloned = cloneDeep(_modem);
        cloned.usb = modem.usb;
        _setModem(cloned);
    };

    const handleChangePreventSameIPUsers = (enabled) => {
        const cloned = cloneDeep(_modem);
        cloned.prevent_same_ip_users = enabled;
        _setModem(cloned);
    };

    const handleChangeAutoRotate = (enabled) => {
        const cloned = cloneDeep(_modem);
        cloned.auto_rotate = enabled;
        _setModem(cloned);
    };

    const handleChangeAutoRotateTime = (time) => {
        const cloned = cloneDeep(_modem);
        cloned.auto_rotate_time = time ? parseInt(time) : null;
        _setModem(cloned);
    };

    const handleChangeAutoRotateHardReset = (enabled) => {
        const cloned = cloneDeep(_modem);
        cloned.auto_rotate_hard_reset = enabled;
        _setModem(cloned);
    };

    const [autoRotateFilter, setAutoRotateFilter] = useState(null);
    const handleChangeAutoRotateFilter = (value) => {
        setAutoRotateFilter(value);
        if (_modem) {
            const cloned = cloneDeep(_modem);
            cloned.auto_rotate_filter = value;
            _setModem(cloned);
        }
    };

    useEffect(() => {
        if (_modem) {
            setAutoRotateFilter(_modem.auto_rotate_filter);
            if (objectHash.MD5(_modem) !== _originalModemHash) {
                _setModemChanged(true);
            } else {
                _setModemChanged(false);
            }
        }
        console.log(_modem);
    }, [_modem]);

    const handleApplyClick = () => {
        saveModem(_modem)
            .then(
                (response) => {
                    console.log(response);
                    _setOriginalModemHash(objectHash.MD5(_modem));
                    _setModemChanged(false);
                },
                (err) => {
                    const message =
                        err.response && err.response.data && err.response.data.error && err.response.data.error.message
                            ? err.response.data.error.message
                            : err.message;
                    console.log('saveModem error', err);
                }
            )
            .finally(() => {
                // setLoading(false);
                // onClose();
            });
    };

    const handleChangeDevice = (device) => {
        const modem = { ..._modem.modem };
        modem.modem.device = { id: device.id };
        const cloned = cloneDeep(_modem);
        cloned.device = modem.device;
        _setModem(cloned);
    };

    return (
        <Dialog
            open={open}
            onClose={onClose}
            aria-labelledby="modem-dialog-settings-title"
            aria-describedby="modem-dialog-settings-description"
            fullWidth={true}
        >
            <BootstrapDialogTitle id="modem-dialog-settings-title" onClose={onClose}>
                <Typography variant="h4" component="span" sx={{ fontWeight: '500' }}>
                    Configurações
                </Typography>
            </BootstrapDialogTitle>
            <DialogContent>
                <Stack spacing={2.5} sx={{ paddingTop: 0 }}>
                    <FormControl sx={{ maxWidth: 160 }}>
                        <ModemPortSelector port={_modem?.usb} onChange={handleChangePort} />
                    </FormControl>
                    <TextField
                        sx={{ maxWidth: 250 }}
                        id="ip-id"
                        label="IP-ID"
                        variant="outlined"
                        value={_modem ? _modem.modem?.addr_id : ''}
                        onChange={(event) => {
                            handleChangeModemAddrId(event.target.value);
                        }}
                    />
                    <FormControl sx={{ maxWidth: 250 }}>
                        <DeviceSelector device={_modem?.modem.device} onChange={handleChangeDevice} />
                    </FormControl>
                    <Divider />
                    <Typography variant="h4" component="span" sx={{ fontWeight: '500' }}>
                        Proxy
                    </Typography>
                    <TextField
                        sx={{ maxWidth: 250 }}
                        id="proxy-ipv4-http-port"
                        label="Porta HTTP/HTTPS"
                        variant="outlined"
                        value={_modem ? _modem.proxy?.ipv4?.http?.port : ''}
                        onChange={(event) => {
                            handleChangeProxyIpv4Http(event.target.value);
                        }}
                    />
                    <TextField
                        sx={{ maxWidth: 250 }}
                        id="proxy-ipv4-http-socks"
                        label="Porta SOCKS"
                        variant="outlined"
                        value={_modem ? _modem.proxy?.ipv4?.socks?.port : ''}
                        onChange={(event) => {
                            handleChangeProxyIpv4Socks(event.target.value);
                        }}
                    />
                    <Divider />
                    <Typography variant="h4" component="span" sx={{ fontWeight: '500' }}>
                        Rotacionamento
                    </Typography>
                    <FormGroup style={{ marginBottom: '-16px' }}>
                        <FormControlLabel
                            control={<Switch checked={_modem ? _modem.prevent_same_ip_users : false} />}
                            label="Evitar mesmo IP para diferentes usuários"
                            onChange={(event) => {
                                handleChangePreventSameIPUsers(event.target.checked);
                            }}
                        />
                    </FormGroup>
                    <FormGroup style={{ marginBottom: '-16px' }}>
                        <FormControlLabel
                            control={<Switch checked={_modem ? _modem.auto_rotate : false} />}
                            label="Rotacionamento automático"
                            onChange={(event) => {
                                handleChangeAutoRotate(event.target.checked);
                            }}
                        />
                    </FormGroup>
                    {_modem && _modem.auto_rotate == true ? (
                        <Box sx={{ maxWidth: 350 }}>
                            <FormGroup style={{ marginBottom: '16px' }}>
                                <FormControlLabel
                                    control={<Switch checked={_modem ? _modem.auto_rotate_hard_reset : false} />}
                                    label="Ativar hard-reset"
                                    onChange={(event) => {
                                        handleChangeAutoRotateHardReset(event.target.checked);
                                    }}
                                />
                            </FormGroup>
                            <FormControl sx={{ maxWidth: 250 }} style={{ marginBottom: '20px' }} variant="outlined">
                                <TextField
                                    id="auto-rotate-value"
                                    InputProps={{
                                        endAdornment: <InputAdornment position="end">segundos</InputAdornment>
                                    }}
                                    aria-describedby="auto-rotate-value-helper-text"
                                    inputProps={{
                                        'aria-label': 'segundos'
                                    }}
                                    label="Intervalo"
                                    type="number"
                                    value={_modem && _modem.auto_rotate_time != null ? _modem.auto_rotate_time : ''}
                                    onChange={(event) => {
                                        handleChangeAutoRotateTime(event.target.value);
                                    }}
                                />
                            </FormControl>
                            <IpFilter value={autoRotateFilter} onChange={handleChangeAutoRotateFilter} />
                        </Box>
                    ) : (
                        <></>
                    )}
                </Stack>
            </DialogContent>
            <BootstrapDialogActions>
                <Button onClick={handleApplyClick} variant="outlined" disabled={!_modemChanged}>
                    Aplicar
                </Button>
            </BootstrapDialogActions>
        </Dialog>
    );
};

SettingsDialog.propTypes = {
    onClose: PropTypes.func.isRequired,
    onConfirm: PropTypes.func.isRequired
};

export default SettingsDialog;
