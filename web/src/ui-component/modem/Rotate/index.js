import * as React from 'react';
import { useState, useEffect } from 'react';

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
import Alert from '@mui/material/Alert';
import Snackbar from '@mui/material/Snackbar';
import IconButton from '@mui/material/IconButton';
import CloseIcon from '@mui/icons-material/Close';
import CircularProgress from '@mui/material/CircularProgress';

import { FormattedMessage } from 'react-intl';

import { rotate } from 'services/api/modem';
import { getProxyUsers, getProxyUserByUsername, getProxyUserFilters } from 'services/api/proxy-user';
import { BootstrapDialogTitle, BootstrapDialogActions } from 'ui-component/extended/BootstrapDialog';
import { IpFilter } from 'ui-component/IpFilter';

const RotateDialog = (props) => {
    const { modem, open, onClose, onConfirm, ...other } = props;

    const [isLoading, setLoading] = useState(false);
    const [proxyUser, setProxyUser] = useState(null);
    const [ipv4Filter, setIPv4Filter] = useState(null);
    const [hardReset, setHardReset] = useState(true);

    const handleConfirmClick = () => {
        setLoading(true);

        rotate(modem.id, hardReset, proxyUser, ipv4Filter)
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
                setIPv4Filter(null);
                setProxyUser(null);
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

    const [isProxyUsersLoading, setIsProxyUsersLoading] = useState(false);
    const [proxyUsers, setProxyUsers] = useState([]);
    useEffect(() => {
        if (open == true) {
            setIsProxyUsersLoading(true);
            getProxyUsers()
                .then(
                    (response) => {
                        if (response.items) {
                            setProxyUsers(response.items);
                        }
                    },
                    (err) => {
                        console.log('rotate error', err);
                    }
                )
                .finally(() => {
                    setIsProxyUsersLoading(false);
                });
        }
    }, [open]);

    const loadFilters = (username) => {
        if (!username) return;

        getProxyUserByUsername(username)
            .then(
                (response) => {
                    if (response && response.id) {
                        getProxyUserFilters(response.id, modem.id)
                            .then(
                                (response) => {
                                    if (response && response.items) {
                                        const filters = [];
                                        response.items.forEach((item) => {
                                            filters.push({
                                                type: item.type,
                                                value: item.value
                                            });
                                        });
                                        setIPv4Filter(filters);
                                    }
                                },
                                (err) => {
                                    console.log('getProxyUserFilters', err);
                                }
                            )
                            .finally(() => {
                                //console.log('end by-username');
                            });
                    }
                },
                (err) => {
                    console.log('getProxyUserByUsername error', err);
                }
            )
            .finally(() => {
                //console.log('end by-username');
            });
    };

    useEffect(() => {
        loadFilters(proxyUser);
    }, [proxyUser]);

    const handleIpv4FilterChange = (obj, str) => {
        setIPv4Filter(obj);
    };

    return (
        <div>
            <Dialog
                open={open}
                onClose={onClose}
                aria-labelledby="modem-dialog-rotate-title"
                aria-describedby="modem-dialog-rotate-description"
            >
                <BootstrapDialogTitle id="modem-dialog-rotate-title" onClose={onClose}>
                    <Typography variant="h4" component="span" sx={{ fontWeight: '500' }}>
                        Rotacionar IP
                    </Typography>
                </BootstrapDialogTitle>
                <DialogContent>
                    <Stack spacing={2.5} sx={{ paddingTop: 0.3 }}>
                        <Alert icon={false} severity="warning">
                            <FormattedMessage id="app.components.modem.Rotate.warning.inUse" values={{ modemId: modem ? modem.id : '' }} />
                        </Alert>
                        <Autocomplete
                            id="modem-ip-change-user"
                            freeSolo
                            options={proxyUsers.map((option) => option.username)}
                            autoHighlight
                            value={proxyUser}
                            onChange={(event, newValue) => {
                                setProxyUser(newValue);
                            }}
                            onInputChange={(event, newInputValue) => {
                                setProxyUser(newInputValue);
                            }}
                            renderInput={(params) => (
                                <TextField
                                    {...params}
                                    label="Usuário"
                                    variant="outlined"
                                    InputProps={{
                                        ...params.InputProps,
                                        endAdornment: (
                                            <React.Fragment>
                                                {isProxyUsersLoading ? <CircularProgress color="inherit" size={20} /> : null}
                                                {params.InputProps.endAdornment}
                                            </React.Fragment>
                                        )
                                    }}
                                />
                            )}
                            loading={true}
                        />
                        <IpFilter value={ipv4Filter} onChange={handleIpv4FilterChange} />
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
                <BootstrapDialogActions>
                    <Button onClick={handleConfirmClick} variant="outlined">
                        Rotacionar
                    </Button>
                </BootstrapDialogActions>
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
                <Alert onClose={handleCloseError} severity="error" sx={{ width: '100%' }} elevation={6}>
                    {error.message}
                </Alert>
            </Snackbar>
        </div>
    );
};

RotateDialog.propTypes = {
    onClose: PropTypes.func.isRequired,
    onConfirm: PropTypes.func.isRequired
};

export default RotateDialog;
