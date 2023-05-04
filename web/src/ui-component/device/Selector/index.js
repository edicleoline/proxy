import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import { useState, useEffect, useRef } from 'react';
import PropTypes from 'prop-types';
import * as React from 'react';
import { getDevices } from 'services/api/device';

const DeviceSelector = ({ device, onChange }) => {
    const [loading, setLoading] = useState(false);
    const [devices, setDevices] = useState([]);

    useEffect(() => {
        setLoading(true);
        getDevices()
            .then(
                (response) => {
                    if (response.items) {
                        setDevices(response.items);
                    }
                },
                (err) => {
                    console.log('device/selector', err);
                }
            )
            .finally(() => {
                setLoading(false);
            });
    }, []);

    const handleChange = (deviceId) => {
        if (onChange) onChange(devices.find((device) => device.id === deviceId));
    };

    return (
        <React.Fragment>
            <InputLabel id="device-label">Modelo</InputLabel>
            <Select
                labelId="device-label"
                id="device-select"
                value={devices && devices.length > 0 && device ? device.id : ''}
                label="Modelo"
                onChange={(event) => {
                    handleChange(event.target.value);
                }}
            >
                {devices.map((device) => (
                    <MenuItem value={device.id} key={device.id}>
                        {device.model}
                    </MenuItem>
                ))}
            </Select>
        </React.Fragment>
    );
};

DeviceSelector.propTypes = {
    device: PropTypes.object,
    onChange: PropTypes.func
};

export default DeviceSelector;
