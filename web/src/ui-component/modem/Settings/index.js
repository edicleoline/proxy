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

import { getUSBPorts } from 'services/api/server';
import { saveModem } from 'services/api/modem';
import cloneDeep from 'lodash/cloneDeep';

const SettingsDialog = (props) => {
    const { modem, open, onClose, onConfirm, ...other } = props;

    const [_modem, _setModem] = useState(cloneDeep(modem));

    useEffect(() => {
        _setModem(cloneDeep(modem));
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

    const handleChangeUSBPort = (portId) => {
        const modem = { ..._modem.modem };
        modem.usb = { id: portId };
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

    const [autoRotateFilter, setAutoRotateFilter] = useState('');

    const handleChangeAutoRotateFilter = (value) => {
        setAutoRotateFilter(value);

        let filters = null;
        const ipv4FilterArray = value ? value.split(',') : null;
        if (ipv4FilterArray) {
            filters = [];
            ipv4FilterArray.forEach((ipv4Filter) => {
                ipv4Filter = ipv4Filter.replace(/\s/g, '');
                filters.push({
                    type: 'ip',
                    value: ipv4Filter
                });
            });
        }

        if (_modem) {
            const cloned = cloneDeep(_modem);
            cloned.auto_rotate_filter = filters;
            _setModem(cloned);
        }
    };

    const handleApplyClick = () => {
        saveModem(_modem)
            .then(
                (response) => {
                    console.log(response);
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

    useEffect(() => {
        if (_modem && _modem.auto_rotate_filter) {
            let filtersExp = '';
            _modem.auto_rotate_filter.forEach((item) => {
                filtersExp += item.value + ', ';
            });
            setAutoRotateFilter(filtersExp.slice(0, -2));
        } else {
            setAutoRotateFilter('');
        }
    }, [_modem]);

    const [isUSBPortsLoading, setIsUSBPortsLoading] = useState(false);
    const [usbPorts, setUSBPorts] = useState([]);

    useEffect(() => {
        if (open == true) {
            setIsUSBPortsLoading(true);
            getUSBPorts()
                .then(
                    (response) => {
                        if (response.items) {
                            setUSBPorts(response.items);
                        }
                    },
                    (err) => {
                        console.log('ServerUSBPorts', err);
                    }
                )
                .finally(() => {
                    setIsUSBPortsLoading(false);
                });
        }
    }, [open]);

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
                        <InputLabel id="modem-setting-port-label">Porta USB</InputLabel>
                        <Select
                            labelId="modem-setting-port-label"
                            id="modem-setting-port-select"
                            value={_modem ? _modem.usb?.id : ''}
                            label="Porta USB"
                            onChange={(event) => {
                                handleChangeUSBPort(event.target.value);
                            }}
                        >
                            {usbPorts.map((usbPort) => (
                                <MenuItem value={usbPort.id} key={usbPort.id}>
                                    {usbPort.port}
                                </MenuItem>
                            ))}
                        </Select>
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
                            <FormControl sx={{ maxWidth: 250 }} variant="outlined">
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
                            <TextField
                                style={{ marginTop: '20px' }}
                                id="modem-settings-filter"
                                label="Filtro IPv4"
                                variant="outlined"
                                helperText="Você pode informar mais de um filtro, separados por vírgula."
                                value={autoRotateFilter}
                                onChange={(event) => {
                                    handleChangeAutoRotateFilter(event.target.value);
                                }}
                            />
                        </Box>
                    ) : (
                        <></>
                    )}
                </Stack>
            </DialogContent>
            <BootstrapDialogActions>
                <Button onClick={handleApplyClick} variant="outlined">
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
