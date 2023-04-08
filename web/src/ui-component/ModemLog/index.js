import { Grid, Card, CardContent } from '@mui/material';
import Paper from '@mui/material/Paper';
import moment from 'moment';
import { useState, useEffect, createRef } from 'react';
import PropTypes from 'prop-types';

import { modemLog, bulkStoreModemLog } from 'storage/modem/log';
import { useLiveQuery } from 'dexie-react-hooks';
import { logs } from 'services/api/modem/log';
import Empty from './Empty';
import MessageLine from './MessageLine';
import { height } from '@mui/system';

const ModemLog = (props) => {
    const { modem, children } = props;

    const [containers, setContainers] = useState([]);

    const _makeContainers = (logs) => {
        if (!logs) {
            return false;
        }

        const containers = [];

        logs.forEach((log) => {
            const date = moment(moment(log.logged_at).format('YYYY-MM-DD')).calendar(null, {
                lastDay: '[Ontem]',
                sameDay: '[Hoje]',
                nextDay: '[Amanhã]',
                lastWeek: '[last] dddd',
                nextWeek: 'dddd',
                sameElse: 'L'
            });
            const existDate = containers.filter((p) => p.type == 'separator' && p.value == date);
            if (existDate.length < 1) {
                containers.push({
                    type: 'separator',
                    value: date,
                    isFirst: containers.length < 1 ? true : false
                });
            }
            containers.push({
                type: 'log',
                value: log
            });
        });

        setContainers(containers);
    };

    const [emptyLog, setEmptyLog] = useState(false);

    const _logs = useLiveQuery(() => modemLog.where({ modem_id: modem.id }).toArray());
    useEffect(() => {
        _makeContainers(_logs);

        if (_logs != undefined && _logs.length < 1) {
            //     console.log('empty logs!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!');
            //     _loadFromApi();
            setEmptyLog(true);
        }
    }, [_logs]);

    const _loadFromApi = () => {
        logs(modem.id, 0, 50, 'next', 'desc')
            .then(
                (response) => {
                    console.log(response);
                    bulkStoreModemLog(response);
                },
                (err) => {
                    const message =
                        err.response && err.response.data && err.response.data.error && err.response.data.error.message
                            ? err.response.data.error.message
                            : err.message;
                    console.log(message);
                }
            )
            .finally(() => {
                //console.log();
            });
    };

    const contentEndAnchor = createRef();

    const scrollToBottom = () => {
        contentEndAnchor.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [containers]);

    return (
        <Paper elevation={0} sx={{ borderRadius: 0 }} style={{ position: 'absolute', height: '100%', width: '100%' }}>
            <Card style={{ backgroundColor: '#f0f0f0', borderRadius: '0', position: 'relative', height: '100%', overflowY: 'auto' }}>
                <CardContent style={{ minHeight: '100%', display: 'flex' }}>
                    {emptyLog ? (
                        <Empty modem={modem} />
                    ) : containers != null ? (
                        <Grid container justifyContent="end" alignItems="end" direction="column" style={{ width: '100%' }}>
                            {containers.map((container, index) => (
                                <MessageLine key={index} container={container} />
                            ))}
                            <div style={{ float: 'left', clear: 'both' }} ref={contentEndAnchor}></div>
                        </Grid>
                    ) : null}
                    {children}
                </CardContent>
            </Card>
        </Paper>
    );
};

ModemLog.propTypes = {
    modem: PropTypes.object,
    children: PropTypes.any
};

export default ModemLog;
