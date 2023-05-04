import { useState, useEffect, useRef } from 'react';
import PropTypes from 'prop-types';
import TextField from '@mui/material/TextField';
import IntlMessageFormat from 'intl-messageformat';
import { locale, messages } from 'i18n';
import cloneDeep from 'lodash/cloneDeep';
import * as React from 'react';
import Stack from '@mui/material/Stack';

const MiddlewareParam = ({ param, value, onChange }) => {
    const handleChange = (v) => {
        if (onChange) {
            onChange(param, v);
        }
    };

    if (!param || param.value == undefined) {
        return null;
    }

    const translatedName = new IntlMessageFormat(messages[locale()][`app.middleware.params.${param.name_translate}`], locale());

    return (
        <TextField
            fullWidth
            id={`middleware-param-${param.id}`}
            label={translatedName.format()}
            variant="outlined"
            value={param.value}
            onChange={(event) => {
                handleChange(event.target.value);
            }}
        />
    );
};

const MiddlewareParams = ({ params, onChange }) => {
    useEffect(() => {
        if (params) {
            params.map((param) => {
                if (!('value' in param) || !param.value) {
                    param.value = '';
                }
                return param;
            });
        }
    }, [params]);

    const handleParamValueChange = (p, v) => {
        p.value = v;
        if (onChange) {
            onChange(params);
        }
    };

    return (
        <React.Fragment>
            <Stack spacing={2.5} sx={{ paddingTop: 0 }}>
                {params?.map((param) => (
                    <MiddlewareParam key={param.id} param={param} value={param.value} onChange={handleParamValueChange} />
                ))}
            </Stack>
        </React.Fragment>
    );
};

export default MiddlewareParams;
