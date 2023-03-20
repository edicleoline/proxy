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

import { useState } from 'react';
import PropTypes from 'prop-types';
import { BootstrapDialogTitle } from 'ui-component/extended/BootstrapDialog';

const SettingsDialog = (props) => {
    const { modem, open, onClose, onConfirm, ...other } = props;

    const handleApplyClick = () => {
        onClose();
    };

    const [port, setPort] = useState('');

    const handleChangePort = (event) => {
        setPort(event.target.value);
    };

    const [autoRotate, setAutoRotate] = useState(false);
    const [preventSameIPUsers, setPreventSameIPUsers] = useState(true);

    return (
        <Dialog
            open={open}
            onClose={onClose}
            aria-labelledby="alert-dialog-title"
            aria-describedby="alert-dialog-description"
            fullWidth={true}
        >
            <BootstrapDialogTitle id="customized-dialog-title" onClose={onClose}>
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
                            value={port}
                            label="Porta USB"
                            onChange={handleChangePort}
                        >
                            <MenuItem value={10}>1</MenuItem>
                            <MenuItem value={20}>2</MenuItem>
                            <MenuItem value={30}>3</MenuItem>
                        </Select>
                    </FormControl>
                    <TextField
                        sx={{ maxWidth: 300 }}
                        id="ip-id"
                        label="IP-ID"
                        variant="outlined"
                        //onChange={(event) => {
                        //    setIPv4Filter(event.target.value);
                        //}}
                    />
                    <Divider />
                    <Typography variant="h4" component="span" sx={{ fontWeight: '500' }}>
                        Proxy
                    </Typography>
                    <TextField
                        sx={{ maxWidth: 300 }}
                        id="proxy-ipv4-http-port"
                        label="Porta HTTP/HTTPS"
                        variant="outlined"
                        //onChange={(event) => {
                        //    setIPv4Filter(event.target.value);
                        //}}
                    />
                    <TextField
                        sx={{ maxWidth: 300 }}
                        id="proxy-ipv4-http-socks"
                        label="Porta SOCKS"
                        variant="outlined"
                        //onChange={(event) => {
                        //    setIPv4Filter(event.target.value);
                        //}}
                    />
                    <Divider />
                    <Typography variant="h4" component="span" sx={{ fontWeight: '500' }}>
                        Rotacionamento
                    </Typography>
                    <FormGroup style={{ marginBottom: '-16px' }}>
                        <FormControlLabel
                            control={<Switch checked={preventSameIPUsers} />}
                            label="Evitar mesmo IP para diferentes usuários"
                            onChange={(event) => {
                                setPreventSameIPUsers(event.target.checked);
                            }}
                        />
                    </FormGroup>
                    <FormGroup style={{ marginBottom: '-10px' }}>
                        <FormControlLabel
                            control={<Switch checked={autoRotate} />}
                            label="Rotacionamento automático"
                            onChange={(event) => {
                                setAutoRotate(event.target.checked);
                            }}
                        />
                    </FormGroup>
                    {autoRotate ? (
                        <FormControl sx={{ m: 1, maxWidth: 350 }} variant="outlined">
                            <TextField
                                id="auto-rotate-value"
                                InputProps={{
                                    endAdornment: <InputAdornment position="end">minutos</InputAdornment>
                                }}
                                aria-describedby="outlined-weight-helper-text"
                                inputProps={{
                                    'aria-label': 'weight'
                                }}
                                label="Intervalo de rotacionamento"
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
