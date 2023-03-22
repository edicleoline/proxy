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

import { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import { BootstrapDialogTitle } from 'ui-component/extended/BootstrapDialog';

import { getUSBPorts } from 'services/api/server';

const SettingsDialog = (props) => {
    const { modem, open, onClose, onConfirm, ...other } = props;

    const handleApplyClick = () => {
        onClose();
    };

    const [isUSBPortsLoading, setIsUSBPortsLoading] = useState(false);
    const [usbPorts, setUSBPorts] = useState([]);

    const [general, setGeneral] = useState({
        addrId: '',
        usbPort: ''
    });

    const [rotate, setRotate] = useState({
        autoRotate: false,
        preventSameIPUsers: true
    });

    const [proxy, setProxy] = useState({
        ipv4HTTPPort: '',
        ipv4SocksPort: ''
    });

    useEffect(() => {
        if (open == true) {
            setProxy({
                ...proxy,
                ipv4HTTPPort: modem && modem.proxy && modem.proxy.ipv4 ? modem.proxy.ipv4.http.port : '',
                ipv4SocksPort: modem && modem.proxy && modem.proxy.ipv4 ? modem.proxy.ipv4.socks.port : ''
            });
            setGeneral({
                ...general,
                addrId: modem && modem.modem ? modem.modem.addr_id : ''
            });

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

    useEffect(() => {
        setGeneral({ ...general, usbPort: modem && modem.usb ? modem.usb.id : '' });
    }, [usbPorts]);

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
                            value={general.usbPort}
                            label="Porta USB"
                            onChange={(event) => {
                                setGeneral({ ...general, usbPort: event.target.value });
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
                        value={general.addrId}
                        onChange={(event) => {
                            setGeneral({ ...general, addrId: event.target.value });
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
                        value={proxy.ipv4HTTPPort}
                        onChange={(event) => {
                            setProxy({ ...proxy, ipv4HTTPPort: event.target.value });
                        }}
                    />
                    <TextField
                        sx={{ maxWidth: 250 }}
                        id="proxy-ipv4-http-socks"
                        label="Porta SOCKS"
                        variant="outlined"
                        value={proxy.ipv4SocksPort}
                        onChange={(event) => {
                            setProxy({ ...proxy, ipv4SocksPort: event.target.value });
                        }}
                    />
                    <Divider />
                    <Typography variant="h4" component="span" sx={{ fontWeight: '500' }}>
                        Rotacionamento
                    </Typography>
                    <FormGroup style={{ marginBottom: '-16px' }}>
                        <FormControlLabel
                            control={<Switch checked={rotate.preventSameIPUsers} />}
                            label="Evitar mesmo IP para diferentes usuários"
                            onChange={(event) => {
                                setRotate({ ...rotate, preventSameIPUsers: event.target.checked });
                            }}
                        />
                    </FormGroup>
                    <FormGroup style={{ marginBottom: '-10px' }}>
                        <FormControlLabel
                            control={<Switch checked={rotate.autoRotate} />}
                            label="Rotacionamento automático"
                            onChange={(event) => {
                                setRotate({ ...rotate, autoRotate: event.target.checked });
                            }}
                        />
                    </FormGroup>
                    {rotate.autoRotate ? (
                        <FormControl sx={{ m: 1, maxWidth: 250 }} variant="outlined">
                            <TextField
                                id="auto-rotate-value"
                                InputProps={{
                                    endAdornment: <InputAdornment position="end">minutos</InputAdornment>
                                }}
                                aria-describedby="auto-rotate-value-helper-text"
                                inputProps={{
                                    'aria-label': 'minutos'
                                }}
                                label="Intervalo"
                                type="number"
                            />
                        </FormControl>
                    ) : (
                        <></>
                    )}
                </Stack>
            </DialogContent>
            <DialogActions>
                <Button onClick={handleApplyClick}>Aplicar</Button>
            </DialogActions>
        </Dialog>
    );
};

SettingsDialog.propTypes = {
    onClose: PropTypes.func.isRequired,
    onConfirm: PropTypes.func.isRequired
};

export default SettingsDialog;
