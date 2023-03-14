import * as React from 'react';
import { useState } from 'react';
import PropTypes from 'prop-types';

import { Typography } from '@mui/material';
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

import { FormattedMessage } from 'react-intl';

import { reboot } from 'services/api/server/modem';

const Alert = React.forwardRef(function Alert(props, ref) {
    return <MuiAlert elevation={6} ref={ref} variant="filled" {...props} />;
});

const RebootDialog = (props) => {
    const { modem, open, onClose, onConfirm, ...other } = props;

    const [isLoading, setLoading] = useState(false);

    const handleConfirmClick = () => {
        setLoading(true);

        let hard_reset = modem.is_connected != true;

        reboot(modem.id, hard_reset)
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
                        message: <FormattedMessage id="app.components.modem.Reboot.error" values={{ modemId: modem.id, error: message }} />
                    });
                    console.log('reboot error', err);
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

    return (
        <div>
            <Dialog open={open} onClose={onClose} aria-labelledby="alert-dialog-title" aria-describedby="alert-dialog-description">
                <DialogTitle id="alert-dialog-title">
                    <Typography variant="h3" component="span" sx={{ fontWeight: '500' }}>
                        <FormattedMessage id="app.components.modem.Reboot.modal.header.title" />
                        &nbsp;
                    </Typography>
                    <Typography variant="h4" component="span" sx={{ fontWeight: '500' }}>
                        <FormattedMessage
                            id="app.components.modem.Reboot.modal.header.subtitle"
                            values={{ modemId: modem ? ' ' + modem.id : '' }}
                        />
                    </Typography>
                </DialogTitle>
                <DialogContent>
                    <DialogContentText id="alert-dialog-description">
                        <FormattedMessage id="app.components.modem.Reboot.modal.body.question" />
                        <br />
                        {modem && modem.is_connected === true ? (
                            <FormattedMessage id="app.components.modem.Reboot.modal.body.alert" />
                        ) : (
                            <></>
                        )}
                    </DialogContentText>
                </DialogContent>
                <DialogActions>
                    <Button onClick={onClose} disabled={isLoading}>
                        <FormattedMessage id="app.labels.no" />
                    </Button>
                    <Button onClick={handleConfirmClick} disabled={isLoading}>
                        <FormattedMessage id="app.labels.reboot" />
                    </Button>
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
