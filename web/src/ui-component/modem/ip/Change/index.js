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

const ChangeDialog = (props) => {
    const { modem, open, onClose, onConfirm, ...other } = props;

    const handleConfirmClick = () => {
        console.log('confirm change', modem);
        onClose();
    };

    const top100Films = [
        { title: 'The Shawshank Redemption', year: 1994 },
        { title: 'The Godfather', year: 1972 },
        { title: 'The Godfather: Part II', year: 1974 },
        { title: 'The Dark Knight', year: 2008 },
        { title: '12 Angry Men', year: 1957 },
        { title: "Schindler's List", year: 1993 },
        { title: 'Pulp Fiction', year: 1994 }
    ];

    return (
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
                <Stack spacing={2} sx={{ paddingTop: 0.5 }}>
                    <Autocomplete
                        id="free-solo-demo"
                        freeSolo
                        options={top100Films.map((option) => option.title)}
                        renderInput={(params) => (
                            <TextField
                                {...params}
                                label="Usuário"
                                variant="standard"
                                helperText={
                                    <span>
                                        <span>Ficou confuso?</span>&nbsp;
                                        <Link href="#">Aqui</Link>&nbsp;
                                        <span>segue uma explicação.</span>
                                    </span>
                                }
                            />
                        )}
                    />
                    <TextField
                        id="standard-basic"
                        label="Filtrar IPv4"
                        variant="standard"
                        helperText="Você pode informar mais de um filtro, separados por vírgula."
                    />
                </Stack>
            </DialogContent>
            <DialogActions>
                <Button onClick={onClose}>Não</Button>
                <Button onClick={handleConfirmClick}>Rotacionar</Button>
            </DialogActions>
        </Dialog>
    );
};

ChangeDialog.propTypes = {
    onClose: PropTypes.func.isRequired,
    onConfirm: PropTypes.func.isRequired
};

export default ChangeDialog;
