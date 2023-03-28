import { useState, useEffect } from 'react';
import TextField from '@mui/material/TextField';
import PropTypes from 'prop-types';

export function IpFilter(props) {
    const _objectToString = (value) => {
        if (!value) return '';

        let filtersExp = '';
        value.forEach((item) => {
            filtersExp += item.value + ', ';
        });

        return filtersExp.slice(0, -2);
    };

    const _stringToObject = (value) => {
        let filters = null;
        const ipv4FilterArray = value ? value.split(',') : null;
        if (ipv4FilterArray) {
            filters = [];
            ipv4FilterArray.forEach((ipv4Filter) => {
                ipv4Filter = ipv4Filter.replace(/\s/g, '');
                filters.push({
                    type: 'ip',
                    value: ipv4Filter
                });
            });
        }

        return filters;
    };

    const [_ipFilterStr, _setIpFilterStr] = useState('');

    const handleChange = (value) => {
        _setIpFilterStr(value);
        props.onChange(_stringToObject(value), value);
    };

    useEffect(() => {
        if (props.value != _ipFilterStr) {
            _setIpFilterStr(_objectToString(props.value));
        }
    }, [props]);

    const onKeyUp = (e) => {
        if (e.keyCode === 8) {
            if (e.target.value.slice(-2) == ', ') {
                handleChange(e.target.value.slice(0, -2));
            }
        }
    };

    return (
        <div>
            <TextField
                id="modem-ip-filter"
                label="Filtro IPv4"
                variant="outlined"
                helperText="Você pode informar mais de um filtro, separados por vírgula."
                value={_ipFilterStr}
                onChange={(event) => {
                    handleChange(event.target.value);
                }}
                onKeyUp={onKeyUp}
                sx={{ width: '100%' }}
            />
        </div>
    );
}

IpFilter.propTypes = {
    onChange: PropTypes.func.isRequired,
    value: PropTypes.any
};
