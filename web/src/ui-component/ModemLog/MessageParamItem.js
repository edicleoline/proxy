import PropTypes from 'prop-types';
import styled from 'styled-components';
import { FormattedMessage } from 'react-intl';
import IntlMessageFormat from 'intl-messageformat';
import { locale, messages } from 'i18n';
import { Grid } from '@mui/material';

const MessageParamItem = ({ pkey, pvalue }) => {
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

MessageParamItem.propTypes = {};

export default MessageParamItem;
