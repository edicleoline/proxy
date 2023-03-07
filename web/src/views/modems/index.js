import { Grid, Link, Box, Card, Typography } from '@mui/material';
import MuiTypography from '@mui/material/Typography';

// project imports
import SubCard from 'ui-component/cards/SubCard';
import MainCard from 'ui-component/cards/MainCard';
import SecondaryAction from 'ui-component/cards/CardSecondaryAction';
import { gridSpacing } from 'store/constant';

import { useEffect, useState } from 'react';

import { getModem, getModems } from 'services/api/server/modem';

import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';

import Button from '@mui/material/Button';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import Divider from '@mui/material/Divider';
import IconButton from '@mui/material/IconButton';
import { IconDotsVertical, IconAccessPoint, IconAccessPointOff } from '@tabler/icons';
import { IconAntennaBars1, IconAntennaBars2, IconAntennaBars3, IconAntennaBars4, IconAntennaBars5 } from '@tabler/icons';
// import { IconSignal4gPlus, IconSignal3g, IconSignal4g, IconSignal5g } from '@tabler/icons';
import { green, grey } from '@mui/material/colors';

const Modems = () => {
    // const [isLoading, setLoading] = useState(true);
    const [modems, setModems] = useState([]);
    const [modemsDetails, setModemsDetails] = useState([]);

    const loadModems = () => {
        getModems().then(
            (items) => {
                console.log(items);
                setModems(items);
                loadModemsDetails(items);
            },
            (error) => console.log('modems error', error)
        );
    };

    const loadModemsDetails = (items) => {
        const modemsDetails = [];

        items.map(function (item) {
            getModem(item.modem.id).then(
                (modem) => {
                    const remodems = items.map(function (m) {
                        if (m.modem.id == modem.modem.id) {
                            m.external_ip = modem.external_ip_through_device;
                            m.device_network_type = modem.device_network_type;
                            m.device_network_provider = modem.device_network_provider;
                            m.device_network_signalbar = modem.device_network_signalbar;
                        }
                        return m;
                    });
                    setModems(remodems);
                    console.log(item.modem.id, remodems);
                },
                (error) => console.log('modem error', error)
            );
        });
    };

    useEffect(() => {
        loadModems();
    }, []);

    const [anchorEl, setAnchorEl] = useState(null);
    const open = Boolean(anchorEl);
    const handleClick = (event) => {
        setAnchorEl(event.currentTarget);
    };
    const handleClose = () => {
        setAnchorEl(null);
    };

    const ColorBox = ({ bgcolor, title, dark }) => (
        <>
            <Card sx={{ mb: 0 }}>
                <Box
                    sx={{
                        display: 'flex',
                        justifyContent: 'center',
                        alignItems: 'center',
                        py: 1,
                        bgcolor,
                        color: dark ? 'grey.800' : '#ffffff'
                    }}
                >
                    {title}
                </Box>
            </Card>
        </>
    );

    const SignalBar = (data) => {
        const icons = {
            ['0']: <Typography variant="subtitle2">-</Typography>,
            ['1']: <IconAntennaBars1 title={data.signal} />,
            ['2']: <IconAntennaBars2 title={data.signal} />,
            ['3']: <IconAntennaBars3 title={data.signal} />,
            ['4']: <IconAntennaBars4 title={data.signal} />,
            ['5']: <IconAntennaBars5 title={data.signal} />
        };

        return icons[data.signal];
    };

    return (
        <MainCard title="Modems" secondary={<SecondaryAction link="https://next.material-ui.com/system/typography/" />}>
            <Grid container spacing={0}>
                <Grid item xs={12} sm={12}>
                    <SubCard>
                        <Grid container direction="column" spacing={0}>
                            <Grid item>
                                <TableContainer component={Paper}>
                                    <Table sx={{ minWidth: 650 }} aria-label="modems table">
                                        <TableHead>
                                            <TableRow>
                                                <TableCell>Modem</TableCell>
                                                <TableCell align="left">Status</TableCell>
                                                <TableCell align="right">IP externo</TableCell>
                                                <TableCell align="right">Provedor</TableCell>
                                                <TableCell align="right">Rede</TableCell>
                                                <TableCell align="center">Sinal</TableCell>
                                                <TableCell align="right">Porta proxy</TableCell>
                                                <TableCell align="right">Status proxy</TableCell>
                                                <TableCell align="right">Porta USB</TableCell>
                                                <TableCell align="right">Tipo</TableCell>
                                                <TableCell align="right">Modelo</TableCell>
                                            </TableRow>
                                        </TableHead>
                                        <TableBody>
                                            {modems.map((row) => (
                                                <TableRow
                                                    hover
                                                    key={row.modem.id}
                                                    sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                                                >
                                                    <TableCell component="th" scope="row">
                                                        <IconButton
                                                            id="basic-button"
                                                            aria-label="expand row"
                                                            size="small"
                                                            aria-controls={open ? 'basic-menu' : undefined}
                                                            aria-haspopup="true"
                                                            aria-expanded={open ? 'true' : undefined}
                                                            onClick={handleClick}
                                                        >
                                                            <IconDotsVertical />
                                                        </IconButton>
                                                        <Menu
                                                            id="basic-menu"
                                                            anchorEl={anchorEl}
                                                            open={open}
                                                            onClose={handleClose}
                                                            MenuListProps={{
                                                                'aria-labelledby': 'basic-button'
                                                            }}
                                                        >
                                                            <MenuItem onClick={handleClose}>Profile</MenuItem>
                                                            <MenuItem onClick={handleClose}>My account</MenuItem>
                                                            <Divider />
                                                            <MenuItem onClick={handleClose}>Configurações</MenuItem>
                                                        </Menu>
                                                        &nbsp;&nbsp;{row.modem.id}
                                                    </TableCell>
                                                    <TableCell align="left">
                                                        {row.is_connected ? (
                                                            <ColorBox bgcolor={'success.light'} title="Conectado" dark />
                                                        ) : (
                                                            <ColorBox bgcolor={'orange.light'} title="Desconectado" dark />
                                                        )}
                                                    </TableCell>
                                                    <TableCell align="right">{row.external_ip ? row.external_ip : '-'}</TableCell>
                                                    <TableCell align="right">
                                                        {row.device_network_provider ? row.device_network_provider : '-'}
                                                    </TableCell>
                                                    <TableCell align="right">
                                                        {row.device_network_type ? row.device_network_type : '-'}
                                                    </TableCell>
                                                    <TableCell align="center">
                                                        {row.device_network_signalbar ? (
                                                            <SignalBar signal={row.device_network_signalbar} />
                                                        ) : (
                                                            <SignalBar signal={0} />
                                                        )}
                                                    </TableCell>
                                                    <TableCell align="right">{row.proxy.port}</TableCell>
                                                    <TableCell align="right"></TableCell>
                                                    <TableCell align="right">{row.usb.port}</TableCell>
                                                    <TableCell align="right">{row.modem.device.type}</TableCell>
                                                    <TableCell align="right">{row.modem.device.model}</TableCell>
                                                </TableRow>
                                            ))}
                                        </TableBody>
                                    </Table>
                                </TableContainer>
                            </Grid>
                        </Grid>
                    </SubCard>
                </Grid>
            </Grid>
        </MainCard>
    );
};

export default Modems;
