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
import styled from 'styled-components';
import moment from 'moment';

import { useState, useEffect, forwardRef, useImperativeHandle, useRef } from 'react';
import PropTypes from 'prop-types';
import { BootstrapDialogTitle } from 'ui-component/extended/BootstrapDialog';

const MessageWrapperSystem = styled.div`
    background-color: #ffffff;
    padding: 8px 10px;
    border-radius: 4px 4px 4px 4px;
    position: relative;
    box-shadow: 1px 1px 1px rgb(0 0 0 / 5%);
    overflow: hidden;
    &:after {
        position: absolute;
        content: '';
        width: 0;
        height: 0;
        border-style: solid;
        border-width: 0px 10px 10px 0;
        border-color: transparent #ffffff transparent transparent;
        top: 0;
        left: -10px;
    }
`;

const MessageWrapperUser = styled.div`
    background-color: #e1ffc7;
    padding: 8px 10px;
    border-radius: 4px 4px 4px 4px;
    position: relative;
    box-shadow: -1px 1px 1px rgb(0 0 0 / 5%);
    overflow: hidden;
    &:after {
        position: absolute;
        content: '';
        width: 0;
        height: 0;
        border-style: solid;
        border-width: 0px 0 10px 10px;
        border-color: transparent transparent transparent #e1ffc7;
        top: 0;
        right: -10px;
    }
`;

const MessageText = styled.div`
    word-wrap: break-word;
`;

const MessageMetadata = styled.span`
    display: inline-block;
    float: right;
    padding: 0 0 0 7px;
    position: relative;
    bottom: -4px;
    font-size: 0.7rem;
    opacity: 0.5;
`;

const ModemLog = (props) => {
    const { modem, children, lines, ...other } = props;

    const time = (dateTime) => {
        const dt = moment(dateTime);
        return dt.format('HH:mm');
    };

    const Message = ({ log }) => {
        return (
            <>
                <MessageText>
                    {log.message}
                    {/* <Params log={log} /> */}
                    <MessageMetadata>{time(log.logged_at)}</MessageMetadata>
                </MessageText>
            </>
        );
    };

    // const Params = ({ log }) => {
    //     console.log(log);
    //     if (!log.params) {
    //         return null;
    //     }

    //     return (
    //         <Grid container justifyContent="end" alignItems="flex-start" direction="column">
    //             <Grid item>test123</Grid>
    //         </Grid>
    //     );
    // };

    const line = (log) => {
        if (log.modem_id != modem.id) {
            return null;
        }

        return (
            <Grid item key={log.id} style={{ width: '100%', marginBottom: '10px' }}>
                <Grid container justifyContent="end" alignItems={log.owner == 'SYSTEM' ? 'flex-start' : 'flex-end'} direction="column">
                    <Grid item style={{ maxWidth: '85%' }}>
                        {log.owner == 'SYSTEM' ? (
                            <MessageWrapperSystem>
                                <Message log={log} />
                            </MessageWrapperSystem>
                        ) : (
                            <MessageWrapperUser>
                                <Message log={log} />
                            </MessageWrapperUser>
                        )}
                    </Grid>
                </Grid>
            </Grid>
        );
    };

    return (
        <Paper elevation={0} sx={{ borderRadius: 0 }}>
            <Card style={{ backgroundColor: '#f0f0f0', borderRadius: '0' }}>
                <CardContent>
                    <Grid
                        container
                        justifyContent="end"
                        alignItems="end"
                        direction="column"
                        style={{ minHeight: '240px', width: '100%', background: 'transparent' }}
                    >
                        {lines != null ? lines.map((logItem, index) => line(logItem)) : null}
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
