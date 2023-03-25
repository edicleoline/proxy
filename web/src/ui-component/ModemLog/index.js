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

const MessageWrapperSystem = styled.div`
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
    background-color: #ede7f6;
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

const MessageWrapper = styled.div`
    word-wrap: break-word;
    white-space: pre-line;
`;

const MessageText = styled.div`
    word-wrap: break-word;
    white-space: pre-line;
    padding: 8px 10px;
    background-color: #ffffff;
    overflow: hidden;

    &.error {
        background-color: #f6b9b969;
    }
    ,
    &.success {
        background-color: #b9f6ca8c;
    }
    ,
    &.info {
        background-color: #ffffff;
    }
    ,
    &.warning {
        background-color: #f6e6b969;
    }
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

const SeparatorDate = styled.span`
    display: inline-block;
    padding: 0 6px;
    position: relative;
    font-size: 0.8rem;
    background-color: #555;
    color: #fff;
    line-height: 1.4rem;
    border-radius: 4px;
`;

const ParamsWrapper = styled.div`
    border-top: solid 1px #f0f0f0;
    padding: 8px 10px;
    clear: both;

    &.error {
        background-color: #f6b9b9a1;
        border-color: #f6b9b9a1;
    }
    ,
    &.success {
        background-color: #b9f6ca;
        border-color: #9ddfb15e;
    }
    ,
    &.info {
        background-color: #f9f9f9;
        border-color: #dddddd6e;
    }
    ,
    &.warning {
        background-color: #f6e3b9a1;
        border-color: #e3d1a078;
    }
`;

const logClassName = (message) => {
    const classname = message.type.toLowerCase();
    return classname;
};

const ModemLog = (props) => {
    const { modem, children, ...other } = props;

    const time = (dateTime) => {
        const dt = moment(dateTime);
        return dt.format('HH:mm');
    };

    const Message = ({ message }) => {
        return (
            <MessageWrapper>
                <MessageText className={logClassName(message)}>
                    <FormattedMessage id={message.message} values={message.params} />
                    <MessageMetadata>{time(message.logged_at)}</MessageMetadata>
                </MessageText>
                <Params log={message} />
            </MessageWrapper>
        );
    };

    const ParamItem = ({ pkey, pvalue }) => {
        if (pvalue instanceof Array) {
            if (pkey == 'filters') {
                let v = '';
                pvalue.map((value) => {
                    const translatedType = new IntlMessageFormat(messages[locale()][`app.log.modem.params.${value.type}`], locale());
                    v += translatedType.format() + '/' + value.value + ', ';
                });
                pvalue = v.length > 2 ? v.slice(0, -2) : v;
            } else {
                pvalue = JSON.stringify(pvalue);
            }
        }

        let translateValue = false;

        if (typeof pvalue === 'boolean') {
            pvalue = pvalue == true ? `app.log.modem.params.${pkey}.true` : `app.log.modem.params.${pkey}.false`;
            translateValue = true;
        }

        if (pvalue == null) {
            pvalue = 'app.log.modem.params.value.none';
            translateValue = true;
        }

        return (
            <Grid container justifyContent="start" alignItems="flex-start" direction="row">
                <Grid item>
                    <FormattedMessage id={`app.log.modem.params.${pkey}`} />
                    :&nbsp;
                </Grid>
                {translateValue ? (
                    <Grid item>
                        <FormattedMessage id={pvalue} />
                    </Grid>
                ) : (
                    <Grid item>{pvalue}</Grid>
                )}
            </Grid>
        );
    };

    const Params = ({ log }) => {
        if (!log || !('params' in log) || !log.params) {
            return null;
        }

        return (
            <ParamsWrapper className={logClassName(log)}>
                <Grid container justifyContent="end" alignItems="flex-start" direction="column">
                    {Object.entries(log.params).map(([key, value], index) => (
                        <ParamItem key={index} pkey={key} pvalue={value} />
                    ))}
                </Grid>
            </ParamsWrapper>
        );
    };

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

        if (_logs != undefined && _logs.length < 1) {
            console.log('empty logs!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!');
            _loadFromApi();
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

    /*const [_firstRender, _setFirstRender] = useState(true);
    useEffect(() => {
        if (_firstRender) {
            console.log('firstttttttttttttttt render log');
            _setFirstRender(false);
        }
    }, [_firstRender]);*/

    const Line = ({ container }) => {
        if (container.type == 'separator') {
            const style = {
                width: '100%',
                marginBottom: '10px',
                marginTop: !container.isFirst ? '20px' : '0'
            };
            return (
                <Grid item style={style}>
                    <Grid container justifyContent="center" alignItems="center" direction="column">
                        <Grid item>
                            <SeparatorDate>{container.value}</SeparatorDate>
                        </Grid>
                    </Grid>
                </Grid>
            );
        }

        const message = container.value;
        return (
            <Grid item style={{ width: '100%', marginBottom: '10px' }}>
                <Grid container justifyContent="end" alignItems={message.owner == 'SYSTEM' ? 'flex-start' : 'flex-end'} direction="column">
                    <Grid item style={{ maxWidth: '85%' }}>
                        {message.owner == 'SYSTEM' ? (
                            <MessageWrapperSystem>
                                <Message message={message} />
                            </MessageWrapperSystem>
                        ) : (
                            <MessageWrapperUser>
                                <Message message={message} />
                            </MessageWrapperUser>
                        )}
                    </Grid>
                </Grid>
            </Grid>
        );
    };

    return (
        <Paper elevation={0} sx={{ borderRadius: 0 }} style={{ position: 'absolute', height: '100%', width: '100%' }}>
            <Card style={{ backgroundColor: '#f0f0f0', borderRadius: '0', position: 'relative', height: '100%', overflowY: 'auto' }}>
                <CardContent>
                    <Grid container justifyContent="end" alignItems="end" direction="column" style={{ width: '100%' }}>
                        {containers != null ? containers.map((container, index) => <Line key={index} container={container} />) : null}
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
