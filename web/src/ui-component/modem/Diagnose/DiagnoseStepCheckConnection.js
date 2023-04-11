import * as React from 'react';
import styled from 'styled-components';
import { Grid } from '@mui/material';
import Button from '@mui/material/Button';
import { diagnose } from 'services/api/modem';
import { BootstrapDialogTitle, BootstrapDialogActions } from 'ui-component/extended/BootstrapDialog';
import { FormattedMessage } from 'react-intl';
import { useEffect } from 'react';
import { useState } from 'react';
import * as animationAstronaut from 'assets/animation/astronaut';
import Lottie from 'react-lottie';
import { postLockWizardStepResponse } from 'services/api/modem';

const StepContainer = styled.div`
    position: relative;
    padding-top: 32px;
    padding-bottom: 32px;
`;

const DiagnoseStepCheckConnection = ({ modem, running, onStart, onStop }) => {
    const lottieDefaultOptions = {
        loop: true,
        autoplay: true,
        animationData: animationAstronaut,
        rendererSettings: {
            preserveAspectRatio: 'xMidYMid slice'
        }
    };

    const handleClickYes = () => {
        sendResponse(true);
    };

    const handleClickNo = () => {
        sendResponse(false);
    };

    const sendResponse = (resp) => {
        const steps = modem?.lock?.wizard?.steps;
        if (!steps) {
            return;
        }

        let step = null;
        for (const s of steps) if (s.type === 'CHECK_CONNECTION') step = s;

        const response = { confirm_modem_on: resp };

        postLockWizardStepResponse(modem.modem.id, modem.lock.id, step.id, response)
            .then(
                (response) => {
                    console.log(response);
                },
                (err) => {
                    const message =
                        err.response && err.response.data && err.response.data.error && err.response.data.error.message
                            ? err.response.data.error.message
                            : err.message;
                    console.log('diagnose error', err);
                }
            )
            .finally(() => {
                // setLoading(false);
            });
    };

    return (
        <React.Fragment>
            <StepContainer>
                <Grid container direction="column" sx={{ flex: '1 1 auto' }}>
                    <Grid item>
                        <Grid container direction="row" justifyContent="center" alignItems="center">
                            <Grid item sx={{ paddingRight: '16px' }}>
                                <Lottie options={lottieDefaultOptions} height={80} width={100} isStopped={false} isPaused={false} />
                            </Grid>
                            <Grid item>
                                <Grid container direction="column" justifyContent="center" alignItems="start">
                                    <Grid item sx={{ whiteSpace: 'pre-line' }}>
                                        <FormattedMessage
                                            id="app.components.modem.Diagnose.connection.check"
                                            values={{ modemId: modem.modem.id }}
                                        />
                                    </Grid>
                                    <Grid item sx={{ marginTop: '16px' }}>
                                        <Grid container direction="row" justifyContent="center" alignItems="start">
                                            <Grid item sx={{ paddingRight: '4px' }}>
                                                <Button variant="outlined" onClick={handleClickYes}>
                                                    <FormattedMessage id="app.labels.yes" />
                                                </Button>
                                            </Grid>
                                            <Grid item>
                                                <Button variant="text" onClick={handleClickNo}>
                                                    <FormattedMessage id="app.labels.no" />
                                                </Button>
                                            </Grid>
                                        </Grid>
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

export default DiagnoseStepCheckConnection;
