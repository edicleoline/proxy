import { Grid, Box, Card, Typography } from '@mui/material';
import Button from '@mui/material/Button';

import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';

import PropTypes from 'prop-types';

import { reboot } from 'services/api/server/modem';

const RebootDialog = (props) => {
    const { modem, open, onClose, onConfirm, ...other } = props;

    const handleConfirmClick = () => {
        reboot(modem.id).then(
            (response) => {
                console.log(response);
            },
            (error) => console.log('reboot error', error)
        );
        onClose();
    };

    return (
        <Dialog open={open} onClose={onClose} aria-labelledby="alert-dialog-title" aria-describedby="alert-dialog-description">
            <DialogTitle id="alert-dialog-title">
                <Typography variant="h2" component="span" sx={{ fontWeight: '500' }}>
                    Reiniciar&nbsp;
                </Typography>
                <Typography variant="h4" component="span" sx={{ fontWeight: '500' }}>
                    modem {modem ? ' ' + modem.id : ''}
                </Typography>
            </DialogTitle>
            <DialogContent>
                <DialogContentText id="alert-dialog-description">
                    Tem certeza de que deseja reiniciar este modem?
                    <br />
                    Considere pausar quaiquer serviços que estiverem usando-o como proxy antes de continuar.
                </DialogContentText>
            </DialogContent>
            <DialogActions>
                <Button onClick={onClose}>Não</Button>
                <Button onClick={handleConfirmClick}>Reiniciar</Button>
            </DialogActions>
        </Dialog>
    );
};

RebootDialog.propTypes = {
    onClose: PropTypes.func.isRequired,
    onConfirm: PropTypes.func.isRequired
};

export default RebootDialog;
