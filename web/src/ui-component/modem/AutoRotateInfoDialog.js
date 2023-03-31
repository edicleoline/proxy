import { Grid, Box, Card, Typography } from '@mui/material';
import Button from '@mui/material/Button';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import { BootstrapDialogTitle } from 'ui-component/extended/BootstrapDialog';
import { FormattedMessage } from 'react-intl';
import { useState, useEffect, useRef } from 'react';
import PropTypes from 'prop-types';
import LinearProgress from '@mui/material/LinearProgress';
import moment from 'moment';
import { scheduleAutoRotate } from 'services/api/modem';
import { toMoment, fromNow } from 'utils/calendar';

const AutoRotateInfoDialog = (props) => {
    const { modem, open, onClose, ...other } = props;

    const [autoRotateSchedule, setAutoRotateSchedule] = useState(null);
    const [runAtFormattedDateTime, setRunAtFormattedDateTime] = useState(null);

    useEffect(() => {
        if (open == true && modem) {
            if (!autoRotateSchedule || autoRotateSchedule.added_at != modem.schedule.added_at) {
                setAutoRotateSchedule(modem.schedule);
            }
        }
    }, [open, modem]);

    const formatRunAt = (value) => {
        return fromNow(toMoment(value));
    };

    const [progress, setProgress] = useState(100);

    useEffect(() => {
        if (!autoRotateSchedule) return;

        setRunAtFormattedDateTime(formatRunAt(autoRotateSchedule.run_at));

        const dateTimeAddedAt = moment(autoRotateSchedule.added_at);
        const dateTimeStart = moment(autoRotateSchedule.run_at);

        const total = dateTimeStart.diff(dateTimeAddedAt, 'seconds');
        let now = moment(autoRotateSchedule.now);

        const timer = setInterval(() => {
            const secondsLeftToRun = dateTimeStart.diff(now, 'seconds');

            if (secondsLeftToRun <= 0) {
                clearInterval(timer);
            }

            const percent = (100 * secondsLeftToRun) / total;
            setProgress(percent);

            setRunAtFormattedDateTime(formatRunAt(autoRotateSchedule.run_at));

            now = now.add(1, 'seconds');
        }, 1000);

        return () => {
            clearInterval(timer);
        };
    }, [autoRotateSchedule]);

    return (
        <Dialog
            open={open}
            onClose={onClose}
            aria-labelledby="modem-auto-rotate-dialog-info-title"
            aria-describedby="modem-auto-rotate-dialog-info-description"
            fullWidth={true}
        >
            <BootstrapDialogTitle id="modem-auto-rotate-dialog-info-title" onClose={onClose}>
                <Typography variant="h4" component="span" sx={{ fontWeight: '500' }}>
                    Rotacionamento automático
                </Typography>
            </BootstrapDialogTitle>
            <DialogContent sx={{ whiteSpace: 'pre-line' }}>
                <DialogContentText id="modem-auto-rotate-dialog-info-description">
                    <FormattedMessage
                        id="app.components.modem.rotate.automated.info.description"
                        values={{ modemId: modem?.id, formattedDateTime: runAtFormattedDateTime }}
                    />
                </DialogContentText>
                <Box sx={{ width: '100%', marginTop: '20px' }}>
                    <LinearProgress variant="determinate" value={progress} />
                </Box>
            </DialogContent>
        </Dialog>
    );
};

AutoRotateInfoDialog.propTypes = {
    onClose: PropTypes.func.isRequired
};

export default AutoRotateInfoDialog;
