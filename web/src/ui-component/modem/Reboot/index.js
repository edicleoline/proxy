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

import Snackbar from '@mui/material/Snackbar';
import IconButton from '@mui/material/IconButton';
import CloseIcon from '@mui/icons-material/Close';
import MuiAlert from '@mui/material/Alert';

import { IntlProvider, FormattedMessage, FormattedNumber } from 'react-intl';

import { reboot } from 'services/api/server/modem';

const Alert = React.forwardRef(function Alert(props, ref) {
    return <MuiAlert elevation={6} ref={ref} variant="filled" {...props} />;
});

const RebootDialog = (props) => {
    const { modem, open, onClose, onConfirm, ...other } = props;

    const handleConfirmClick = () => {
        reboot(modem.id).then(
            (response) => {
                console.log(response);
            },
            (err) => {
                const message =
                    err.response && err.response.data && err.response.data.error && err.response.data.error.message
                        ? err.response.data.error.message
                        : err.message;
                setError({ ...error, open: true, message: `Erro ao reiniciar modem ${modem.id} - ${message}` });
                console.log('reboot error', err);
            }
        );
        onClose();
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

    return (
        <div>
            <Dialog open={open} onClose={onClose} aria-labelledby="alert-dialog-title" aria-describedby="alert-dialog-description">
                <DialogTitle id="alert-dialog-title">
                    <Typography variant="h2" component="span" sx={{ fontWeight: '500' }}>
                        <FormattedMessage id="app.components.Reboot.modal.header.title" />
                        &nbsp;
                    </Typography>
                    <Typography variant="h4" component="span" sx={{ fontWeight: '500' }}>
                        modem {modem ? ' ' + modem.id : ''}
                    </Typography>
                </DialogTitle>
                <DialogContent>
                    <DialogContentText id="alert-dialog-description">
                        <FormattedMessage id="app.components.Reboot.modal.body.question" />
                        <br />
                        <FormattedMessage id="app.components.Reboot.modal.body.alert" />
                    </DialogContentText>
                </DialogContent>
                <DialogActions>
                    <Button onClick={onClose}>Não</Button>
                    <Button onClick={handleConfirmClick}>Reiniciar</Button>
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

RebootDialog.propTypes = {
    onClose: PropTypes.func.isRequired,
    onConfirm: PropTypes.func.isRequired
};

export default RebootDialog;
