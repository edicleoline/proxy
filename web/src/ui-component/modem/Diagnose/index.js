import { Grid, Box, Card, Typography } from '@mui/material';
import Button from '@mui/material/Button';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import DiagnoseStepper from './DiagnoseStepper';
import { BootstrapDialogTitle, BootstrapDialogActions } from 'ui-component/extended/BootstrapDialog';
import PropTypes from 'prop-types';
import { FormattedMessage } from 'react-intl';
import { useSelector } from 'react-redux';
import { useEffect, useState } from 'react';
import cloneDeep from 'lodash/cloneDeep';

const DiagnoseDialog = (props) => {
    const { modem, open, onClose } = props;

    const _modems = useSelector((state) => state.modems);
    const [_modem, _setModem] = useState(modem);

    useEffect(() => {
        if (modem) {
            for (const m of _modems.items) {
                if (m.modem.id == modem.modem.id) {
                    _setModem(cloneDeep(m));
                    break;
                }
            }
        }
    }, [_modems, modem]);

    useEffect(() => {
        console.log('modem_diagnose', _modem);
    }, [_modem]);

    return (
        <Dialog
            open={open}
            onClose={onClose}
            aria-labelledby="dialog-diagnose-title"
            aria-describedby="dialog-diagnose-description"
            fullWidth={true}
        >
            <BootstrapDialogTitle id="modem-reboot-dialog-title" onClose={onClose}>
                <Typography variant="h4" component="span" sx={{ fontWeight: '500' }}>
                    <FormattedMessage id="app.components.modem.Diagnose.modal.header.title" />
                </Typography>
            </BootstrapDialogTitle>
            <DialogContent sx={{ padding: '0' }}>
                <DiagnoseStepper modem={_modem} />
            </DialogContent>
        </Dialog>
    );
};

DiagnoseDialog.propTypes = {
    onClose: PropTypes.func.isRequired,
    open: PropTypes.bool.isRequired,
    modem: PropTypes.object
};

export default DiagnoseDialog;
