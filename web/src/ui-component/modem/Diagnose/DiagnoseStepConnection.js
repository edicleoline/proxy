import * as React from 'react';
import styled from 'styled-components';
import { Grid } from '@mui/material';
import Button from '@mui/material/Button';
import { diagnose } from 'services/api/modem';
import { BootstrapDialogTitle, BootstrapDialogActions } from 'ui-component/extended/BootstrapDialog';
import { FormattedMessage } from 'react-intl';
import { useEffect } from 'react';
import { useState } from 'react';
import * as checkingConnection from 'assets/animation/loading_connection';
import Lottie from 'react-lottie';

const StepContainer = styled.div`
    position: relative;
`;

const DiagnoseStepConnection = ({ modem, running, onStart, onStop }) => {
    const lottieDefaultOptions = {
        loop: true,
        autoplay: true,
        animationData: checkingConnection,
        rendererSettings: {
            preserveAspectRatio: 'xMidYMid slice'
        }
    };

    return (
        <React.Fragment>
            <StepContainer>
                <Grid container direction="column" sx={{ flex: '1 1 auto' }}>
                    <Grid item>
                        <Grid
                            container
                            direction="row"
                            justifyContent="center"
                            alignItems="center"
                            sx={{ flexWrap: 'initial', padding: '16px 36px' }}
                        >
                            <Grid item sx={{ paddingRight: '16px' }}>
                                <Lottie options={lottieDefaultOptions} height={80} width={100} isStopped={false} isPaused={false} />
                            </Grid>
                            <Grid item>
                                <Grid container direction="column" justifyContent="center" alignItems="start">
                                    <Grid item sx={{ whiteSpace: 'pre-line' }}>
                                        <FormattedMessage
                                            id="app.components.modem.Diagnose.connection.checking"
                                            values={{ modemId: modem.modem.id }}
                                        />
                                    </Grid>
                                </Grid>
                            </Grid>
                        </Grid>
                    </Grid>
                </Grid>
            </StepContainer>
        </React.Fragment>
    );
};

export default DiagnoseStepConnection;
