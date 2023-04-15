import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import { useState, useEffect, useRef } from 'react';
import PropTypes from 'prop-types';
import * as React from 'react';

const DeviceSelector = ({ device, onChange }) => {
    const [loading, setLoading] = useState(false);
    const [devices, setDevices] = useState([]);

    const handleChange = (deviceId) => {
        console.log(deviceId);
        onChange(deviceId);
    };

    return (
        <React.Fragment>
            <InputLabel id="device-label">Dispositivo</InputLabel>
            <Select
                labelId="device-label"
                id="device-select"
                value={device ? device.id : ''}
                label="Dispositivo"
                onChange={(event) => {
                    handleChange(event.target.value);
                }}
            >
                {devices.map((device) => (
                    <MenuItem value={device.id} key={device.id}>
                        {device.name}
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
