import * as React from 'react';
import { useState, useEffect } from 'react';
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
import FormGroup from '@mui/material/FormGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import Switch from '@mui/material/Switch';
import { FormattedMessage } from 'react-intl';
import { reboot } from 'services/api/modem';
import { BootstrapDialogTitle, BootstrapDialogActions } from 'ui-component/extended/BootstrapDialog';

const Alert = React.forwardRef(function Alert(props, ref) {
    return <MuiAlert elevation={6} ref={ref} variant="filled" {...props} />;
});

const RebootDialog = (props) => {
    const { modem, open, onClose, onConfirm, ...other } = props;

    const [isLoading, setLoading] = useState(false);
    const [hardReset, setHardReset] = useState(modem && !modem.is_connected ? true : false);
    const [disableHardResetCheckbox, setDisableHardResetCheckbox] = useState(modem && !modem.is_connected ? true : false);

    const handleConfirmClick = () => {
        setLoading(true);

        let _hardReset = !modem.is_connected ? true : hardReset;

        reboot(modem.modem.id, _hardReset)
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

    useEffect(() => {
        if (modem && !modem.is_connected) {
            setHardReset(true);
            setDisableHardResetCheckbox(true);
        } else if (modem && modem.is_connected) {
            setDisableHardResetCheckbox(false);
        }
    }, [open]);

    return (
        <div>
            <Dialog
                open={open}
                onClose={onClose}
                aria-labelledby="modem-reboot-dialog-title"
                aria-describedby="modem-reboot-dialog-description"
                fullWidth={true}
            >
                <BootstrapDialogTitle id="modem-reboot-dialog-title" onClose={onClose}>
                    <Typography variant="h4" component="span" sx={{ fontWeight: '500' }}>
                        <FormattedMessage id="app.components.modem.Reboot.modal.header.title" />
                    </Typography>
                </BootstrapDialogTitle>
                <DialogContent>
                    <DialogContentText id="modem-reboot-dialog-description">
                        <FormattedMessage
                            id="app.components.modem.Reboot.modal.body.question"
                            values={{ modemId: modem ? ' ' + modem.modem.id : '' }}
                        />
                        <br />
                        {modem && modem.is_connected === true ? (
                            <FormattedMessage id="app.components.modem.Reboot.modal.body.alert" />
                        ) : null}
                    </DialogContentText>
                    <FormGroup sx={{ marginTop: '16px' }}>
                        <FormControlLabel
                            control={<Switch checked={hardReset} />}
                            label="Ativar hard-reset"
                            onChange={(event) => {
                                setHardReset(event.target.checked);
                            }}
                            disabled={disableHardResetCheckbox}
                        />
                    </FormGroup>
                </DialogContent>
                <BootstrapDialogActions>
                    <Button onClick={handleConfirmClick} disabled={isLoading} variant="contained">
                        <FormattedMessage id="app.labels.reboot" />
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
