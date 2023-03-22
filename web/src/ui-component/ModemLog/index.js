import { Grid, Box, Card, Typography, CardContent } from '@mui/material';
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
import IconButton from '@mui/material/IconButton';
import CloseIcon from '@mui/icons-material/Close';
import { IconChevronUp } from '@tabler/icons';
import Paper from '@mui/material/Paper';

import { useState, useEffect, forwardRef, useImperativeHandle, useRef } from 'react';
import PropTypes from 'prop-types';
import { BootstrapDialogTitle } from 'ui-component/extended/BootstrapDialog';

const ModemLog = (props) => {
    const { modem, children, lines, ...other } = props;

    const handleWriteLine = (str) => {
        console.log(str);
    };

    return (
        <Paper elevation={0} sx={{ borderRadius: 0 }}>
            <Card>
                <CardContent>
                    <Grid
                        container
                        justifyContent="end"
                        alignItems="end"
                        direction="column"
                        style={{ minHeight: '240px', width: '100%', background: 'transparent' }}
                    >
                        {lines != null
                            ? lines.map((line, index) => (
                                  <Grid item key={index}>
                                      {line.message}
                                  </Grid>
                              ))
                            : null}
                    </Grid>
                    {children}
                </CardContent>
            </Card>
        </Paper>
    );
};

ModemLog.propTypes = {
    // onClose: PropTypes.func.isRequired,
    // onConfirm: PropTypes.func.isRequired
};

export default ModemLog;
