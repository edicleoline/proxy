import Select from '@mui/material/Select';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import { useState, useEffect, useRef } from 'react';
import PropTypes from 'prop-types';
import * as React from 'react';
import { getUSBPorts } from 'services/api/server';

const ModemPortSelector = ({ port, onChange }) => {
    const [loading, setLoading] = useState(false);
    const [ports, setPorts] = useState([]);

    useEffect(() => {
        setLoading(true);
        getUSBPorts()
            .then(
                (response) => {
                    if (response.items) {
                        setPorts(response.items);
                    }
                },
                (err) => {
                    console.log('modem-port/selector', err);
                }
            )
            .finally(() => {
                setLoading(false);
            });
    }, []);

    const handleChange = (portId) => {
        if (onChange) onChange(ports.find((port) => port.id === portId));
    };

    return (
        <React.Fragment>
            <InputLabel id="modem-port-label">Porta</InputLabel>
            <Select
                labelId="modem-port-label"
                id="modem-port-select"
                value={ports && ports.length > 0 && port ? port.id : ''}
                label="Porta"
                onChange={(event) => handleChange(event.target.value)}
            >
                {ports.map((port) => (
                    <MenuItem value={port.id} key={port.id}>
                        {port.port}
                    </MenuItem>
                ))}
            </Select>
        </React.Fragment>
    );
};

ModemPortSelector.propTypes = {
    port: PropTypes.object,
    onChange: PropTypes.func
};

export default ModemPortSelector;
