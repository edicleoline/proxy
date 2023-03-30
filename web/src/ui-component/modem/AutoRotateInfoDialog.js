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

const AutoRotateInfoDialog = (props) => {
    const { modem, open, onClose, ...other } = props;

    const [autoRotateSchedule, setAutoRotateSchedule] = useState(null);
    const [runAtFormattedDateTime, setRunAtFormattedDateTime] = useState(null);

    useEffect(() => {
        if (open == true) {
            scheduleAutoRotate(modem.id)
                .then(
                    (response) => {
                        console.log(response);
                        setAutoRotateSchedule(response);

                        const runAtTime = moment(response.run_at).fromNow();
                        setRunAtFormattedDateTime(runAtTime);
                    },
                    (err) => {
                        const message =
                            err.response && err.response.data && err.response.data.error && err.response.data.error.message
                                ? err.response.data.error.message
                                : err.message;
                        console.log('reboot error', err);
                    }
                )
                .finally(() => {
                    // setLoading(false);
                });

            // setAutoRotateSchedule({
            //     now: '2023-03-29 22:01:40.710990',
            //     added_at: '2023-03-29 22:01:00.710990',
            //     run_at: '2023-03-29 22:06:00.710990'
            // });
        }
    }, [open]);

    const [progress, setProgress] = useState(100);

    useEffect(() => {
        if (!autoRotateSchedule) return;

        const dateTimeNow = moment(autoRotateSchedule.now);
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

            const runAtTime = moment(autoRotateSchedule.run_at).fromNow();
            setRunAtFormattedDateTime(runAtTime);

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
