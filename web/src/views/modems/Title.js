import { Grid, Typography } from '@mui/material';
import Paper from '@mui/material/Paper';
import InputBase from '@mui/material/InputBase';
import SearchIcon from '@mui/icons-material/Search';
import Input from '@mui/material/Input';
import FilledInput from '@mui/material/FilledInput';
import OutlinedInput from '@mui/material/OutlinedInput';
import InputLabel from '@mui/material/InputLabel';
import InputAdornment from '@mui/material/InputAdornment';
import FormHelperText from '@mui/material/FormHelperText';
import FormControl from '@mui/material/FormControl';
import TextField from '@mui/material/TextField';

const Title = ({ modems }) => {
    return (
        <Grid container direction="column">
            <Grid item>
                <Grid container direction="row">
                    <Grid item>Modems&nbsp;</Grid>
                    <Grid item>
                        <Typography variant="subtitle1" sx={{ opacity: 0.5 }}>
                            ({modems.length})
                        </Typography>
                    </Grid>
                </Grid>
            </Grid>
            {/* <Grid item>
                <FormControl sx={{ mt: 1, width: '100%', maxWidth: '550px' }} variant="outlined">
                    <OutlinedInput
                        id="outlined-adornment-password"
                        type="text"
                        placeholder="Buscar dispositivo, IP, provedor, rede"
                        startAdornment={
                            <InputAdornment position="start">
                                <SearchIcon />
                            </InputAdornment>
                        }
                    />
                </FormControl>
            </Grid> */}
        </Grid>
    );
};

export default Title;
