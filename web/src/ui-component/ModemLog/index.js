import { Grid, Box, Card, Typography, CardContent } from '@mui/material';
import Button from '@mui/material/Button';
import Paper from '@mui/material/Paper';
import styled from 'styled-components';
import moment from 'moment';

import { useState, useEffect, createRef } from 'react';
import PropTypes, { bool } from 'prop-types';

import { modemLog, bulkStoreModemLog } from 'storage/modem/log';
import { useLiveQuery } from 'dexie-react-hooks';

import { FormattedMessage } from 'react-intl';
import IntlMessageFormat from 'intl-messageformat';
import { locale, messages } from 'i18n';

import { logs } from 'services/api/modem/log';
import Tooltip from '@mui/material/Tooltip';

import MessageLine from './MessageLine';

const ModemLog = (props) => {
    const { modem, children, ...other } = props;

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

    const _logs = useLiveQuery(() => modemLog.where({ modem_id: modem.modem.id }).toArray());
    useEffect(() => {
        _makeContainers(_logs);

        // if (_logs != undefined && _logs.length < 1) {
        //     console.log('empty logs!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!');
        //     _loadFromApi();
        // }
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

    /*const [_firstRender, _setFirstRender] = useState(true);
    useEffect(() => {
        if (_firstRender) {
            console.log('firstttttttttttttttt render log');
            _setFirstRender(false);
        }
    }, [_firstRender]);*/

    return (
        <Paper elevation={0} sx={{ borderRadius: 0 }} style={{ position: 'absolute', height: '100%', width: '100%' }}>
            <Card style={{ backgroundColor: '#f0f0f0', borderRadius: '0', position: 'relative', height: '100%', overflowY: 'auto' }}>
                <CardContent>
                    <Grid container justifyContent="end" alignItems="end" direction="column" style={{ width: '100%' }}>
                        {containers != null
                            ? containers.map((container, index) => <MessageLine key={index} container={container} />)
                            : null}
                    </Grid>
                    {children}
                    <div style={{ float: 'left', clear: 'both' }} ref={contentEndAnchor}></div>
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
