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
    padding-top: 32px;
    padding-bottom: 32px;
`;

const DiagnoseStepStart = ({ modem, running, onStart, onStop }) => {
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
                        <Grid container direction="column" justifyContent="center" alignItems="center">
                            {/* <Grid item>
                                <Lottie options={lottieDefaultOptions} height={80} width={120} isStopped={false} isPaused={false} />
                            </Grid> */}
                            <Grid item sx={{ marginTop: '16px' }}>
                                start?
                            </Grid>
                        </Grid>
                    </Grid>
                </Grid>
            </StepContainer>
        </React.Fragment>
    );
};

export default DiagnoseStepStart;
