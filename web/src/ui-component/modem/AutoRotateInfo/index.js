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
import { toMoment, fromNow } from 'utils/calendar';
import styled from 'styled-components';

const AutoRotateInfoContent = styled.div`
    white-space: pre-line;
    padding: 16px;
`;

const AutoRotateInfoFooter = styled.div`
    padding: 0 16px 16px 16px;
`;

const AutoRotateInfo = (props) => {
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
        <Box>
            <Grid container>
                <Grid item>
                    <AutoRotateInfoContent>
                        <FormattedMessage
                            id="app.components.modem.rotate.automated.info.description"
                            values={{ modemId: modem?.modem?.id, formattedDateTime: runAtFormattedDateTime }}
                        />
                        <br></br>
                        <FormattedMessage
                            id="app.components.modem.rotate.automated.schedule.task.next"
                            values={{ modemId: modem?.id, formattedDateTime: runAtFormattedDateTime }}
                        />
                    </AutoRotateInfoContent>
                    <AutoRotateInfoFooter>
                        <LinearProgress variant="determinate" value={progress} />
                    </AutoRotateInfoFooter>
                </Grid>
            </Grid>
        </Box>
    );
};

AutoRotateInfo.propTypes = {
    onClose: PropTypes.func.isRequired
};

export default AutoRotateInfo;
