import * as React from 'react';
import styled from 'styled-components';
import { Grid } from '@mui/material';
import Button from '@mui/material/Button';
import { diagnose } from 'services/api/modem';
import { BootstrapDialogTitle, BootstrapDialogActions } from 'ui-component/extended/BootstrapDialog';
import { FormattedMessage } from 'react-intl';
import { useEffect } from 'react';
import { useState } from 'react';
import * as settingsReset from 'assets/animation/settings_reset.json';
import Lottie from 'react-lottie';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemAvatar from '@mui/material/ListItemAvatar';
import ListItemIcon from '@mui/material/ListItemIcon';
import Divider from '@mui/material/Divider';
import Avatar from '@mui/material/Avatar';
import ImageIcon from '@mui/icons-material/Image';
import InboxIcon from '@mui/icons-material/Inbox';
import WorkIcon from '@mui/icons-material/Work';
import SettingsRemoteIcon from '@mui/icons-material/SettingsRemote';

const StepContainer = styled.div`
    position: relative;
`;

const DiagnoseStepSelectInterface = ({ modem, running, onStart, onStop }) => {
    const lottieDefaultOptions = {
        loop: true,
        autoplay: true,
        animationData: settingsReset,
        rendererSettings: {
            preserveAspectRatio: 'xMidYMid slice'
        }
    };

    const [interfaces, setInterfaces] = useState([]);
    useEffect(() => {
        const steps = modem?.lock?.wizard?.steps;
        if (steps) {
            let step = null;
            for (const s of steps) if (s.type === 'SELECT_INTERFACE') step = s;
            if (step && step.data && step.data.interfaces) {
                setInterfaces(step.data.interfaces);
            }
        }
    }, [modem]);

    useEffect(() => {
        console.log(interfaces);
    }, [interfaces]);

    return (
        <React.Fragment>
            <StepContainer>
                <Grid container direction="column" sx={{ flex: '1 1 auto' }}>
                    <Grid item>
                        <Grid
                            container
                            direction="row"
                            justifyContent="center"
                            alignItems="start"
                            sx={{ flexWrap: 'initial', padding: '16px 36px' }}
                        >
                            <Grid item sx={{ paddingRight: '16px' }}>
                                <Lottie options={lottieDefaultOptions} height={80} width={100} isStopped={false} isPaused={false} />
                            </Grid>
                            <Grid item>
                                <Grid container direction="column" justifyContent="center" alignItems="start">
                                    <Grid item sx={{ whiteSpace: 'pre-line' }}>
                                        <FormattedMessage
                                            id="app.components.modem.Diagnose.connection.interface.select"
                                            values={{ modemId: modem.modem.id }}
                                        />
                                    </Grid>
                                </Grid>
                                <Grid item sx={{ marginTop: '16px' }}>
                                    <List component="nav" sx={{ width: '100%', maxWidth: 360 }}>
                                        {interfaces.map((iface, index) => (
                                            <ListItemButton key={index}>
                                                <ListItemIcon>
                                                    <SettingsRemoteIcon />
                                                </ListItemIcon>
                                                <ListItemText primary={iface.iface} secondary={iface.ifaddresses[0].addr} />
                                            </ListItemButton>
                                        ))}
                                    </List>
                                </Grid>
                            </Grid>
                        </Grid>
                    </Grid>
                </Grid>
            </StepContainer>
        </React.Fragment>
    );
};

export default DiagnoseStepSelectInterface;
