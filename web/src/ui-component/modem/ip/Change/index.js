import * as React from 'react';
import { useState } from 'react';

import PropTypes from 'prop-types';

import { Grid, Box, Card, Typography } from '@mui/material';
import Button from '@mui/material/Button';

import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';

import TextField from '@mui/material/TextField';
import Stack from '@mui/material/Stack';
import Autocomplete from '@mui/material/Autocomplete';
import Link from '@mui/material/Link';
import FormGroup from '@mui/material/FormGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import Switch from '@mui/material/Switch';
import MuiAlert from '@mui/material/Alert';
import Snackbar from '@mui/material/Snackbar';
import IconButton from '@mui/material/IconButton';
import CloseIcon from '@mui/icons-material/Close';

import { FormattedMessage } from 'react-intl';

import { rotate } from 'services/api/server/modem';

const Alert = React.forwardRef(function Alert(props, ref) {
    return <MuiAlert elevation={6} ref={ref} variant="filled" {...props} />;
});

const ChangeDialog = (props) => {
    const { modem, open, onClose, onConfirm, ...other } = props;

    const [isLoading, setLoading] = useState(false);
    const [proxyUser, setProxyUser] = useState(null);
    const [ipv4Filter, setIPv4Filter] = useState('');
    const [hardReset, setHardReset] = useState(true);

    const handleConfirmClick = () => {
        setLoading(true);

        let filters = null;
        const ipv4FilterArray = ipv4Filter ? ipv4Filter.split(',') : null;
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

        rotate(modem.id, hardReset, null, filters)
            .then(
                (response) => {
                    console.log(response);
                },
                (err) => {
                    const message =
                        err.response && err.response.data && err.response.data.error && err.response.data.error.message
                            ? err.response.data.error.message
                            : err.message;
                    setError({
                        ...error,
                        open: true,
                        message: <FormattedMessage id="app.components.modem.Rotate.error" values={{ modemId: modem.id, error: message }} />
                    });
                    console.log('rotate error', err);
                }
            )
            .finally(() => {
                setLoading(false);
                onClose();
            });
    };

    const [error, setError] = useState({
        open: false,
        message: ''
    });
    const handleCloseError = (event, reason) => {
        if (reason === 'clickaway') {
            return;
        }

        setError({ ...error, open: false });
    };

    const top100Films = [
        { id: 1, name: 'João' },
        { id: 2, name: 'Maria' }
    ];

    return (
        <div>
            <Dialog open={open} onClose={onClose} aria-labelledby="alert-dialog-title" aria-describedby="alert-dialog-description">
                <DialogTitle id="alert-dialog-title">
                    <Typography variant="h3" component="span" sx={{ fontWeight: '500' }}>
                        Rotacionar IP&nbsp;
                    </Typography>
                    <Typography variant="h4" component="span" sx={{ fontWeight: '500' }}>
                        modem {modem ? ' ' + modem.id : ''}
                    </Typography>
                </DialogTitle>
                <DialogContent>
                    <DialogContentText id="alert-dialog-description" sx={{ marginBottom: 2.5 }}>
                        Antes de continuar, considere pausar quaiquer serviços que estiverem usando-o como proxy.
                    </DialogContentText>
                    <Stack spacing={2.5} sx={{ paddingTop: 0.3 }}>
                        <Autocomplete
                            id="modem-ip-change-user"
                            freeSolo
                            options={top100Films.map((option) => option.name)}
                            autoHighlight
                            value={proxyUser}
                            onChange={(event, newValue) => {
                                setProxyUser(newValue);
                                console.log(newValue);
                            }}
                            onInputChange={(event, newInputValue) => {
                                setProxyUser(newInputValue);
                                console.log(newInputValue);
                            }}
                            renderInput={(params) => <TextField {...params} label="Usuário" variant="outlined" />}
                        />
                        <TextField
                            id="modem-ip-change-filter"
                            label="Filtro IPv4"
                            variant="outlined"
                            helperText="Você pode informar mais de um filtro, separados por vírgula."
                            onChange={(event) => {
                                setIPv4Filter(event.target.value);
                            }}
                        />
                        <FormGroup>
                            <FormControlLabel
                                control={<Switch checked={hardReset} />}
                                label="Ativar hard-reset"
                                onChange={(event) => {
                                    setHardReset(event.target.checked);
                                }}
                            />
                        </FormGroup>
                    </Stack>
                </DialogContent>
                <DialogActions>
                    <Button onClick={onClose}>Não</Button>
                    <Button onClick={handleConfirmClick}>Rotacionar</Button>
                </DialogActions>
            </Dialog>
            <Snackbar
                anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
                open={error.open}
                autoHideDuration={6000}
                onClose={handleCloseError}
                message={error.message}
                action={
                    <React.Fragment>
                        <IconButton aria-label="close" color="inherit" sx={{ p: 0.5 }} onClick={handleCloseError}>
                            <CloseIcon />
                        </IconButton>
                    </React.Fragment>
                }
            >
                <Alert onClose={handleCloseError} severity="error" sx={{ width: '100%' }}>
                    {error.message}
                </Alert>
            </Snackbar>
        </div>
    );
};

ChangeDialog.propTypes = {
    onClose: PropTypes.func.isRequired,
    onConfirm: PropTypes.func.isRequired
};

export default ChangeDialog;
