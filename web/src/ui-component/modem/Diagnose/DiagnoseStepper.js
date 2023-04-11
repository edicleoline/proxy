import * as React from 'react';
import Box from '@mui/material/Box';
import Stepper from '@mui/material/Stepper';
import Step from '@mui/material/Step';
import StepLabel from '@mui/material/StepLabel';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import DiagnoseStepConnection from './DiagnoseStepConnection';
import DiagnoseStepCheckConnection from './DiagnoseStepCheckConnection';
import DiagnoseStepStart from './DiagnoseStepStart';
import DiagnoseStepSelectInterface from './DiagnoseStepSelectInterface';
import { useEffect, useState } from 'react';
import { diagnose, stopDiagnose } from 'services/api/modem';
import { BootstrapDialogTitle, BootstrapDialogActions } from 'ui-component/extended/BootstrapDialog';
import { FormattedMessage } from 'react-intl';

const steps = ['Select campaign settings', 'Create an ad group', 'Create an ad', 'Create an ad'];

const DiagnoseStepContent = ({ activeStep, modem, running, onStart, onStop }) => {
    switch (activeStep) {
        case 0:
            return <DiagnoseStepStart modem={modem} running={running} onStart={onStart} onStop={onStop} />;
        case 1:
            return <DiagnoseStepConnection modem={modem} running={running} onStart={onStart} onStop={onStop} />;
        case 2:
            return <DiagnoseStepCheckConnection modem={modem} running={running} onStart={onStart} onStop={onStop} />;
        case 3:
            return <DiagnoseStepSelectInterface modem={modem} running={running} onStart={onStart} onStop={onStop} />;
        default:
            break;
    }
};

const DiagnoseStepper = ({ modem }) => {
    // const [running, setRunning] = useState(modem);

    const [activeStep, setActiveStep] = React.useState(0);

    const [starting, setStarting] = useState(false);
    const [running, setRunning] = useState(false);

    const [enableCancel, setEnableCancel] = useState(true);

    useEffect(() => {
        setEnableCancel(modem && modem.lock && modem.lock.task && modem.lock.task.stopping);
    }, [modem]);

    useEffect(() => {
        setRunning(modem?.lock?.task?.name === 'DIAGNOSE');

        if (modem?.lock == null) {
            setActiveStep(0);
            setStarting(false);
        } else if (modem?.lock?.task?.name === 'DIAGNOSE') {
            if (modem?.lock?.wizard == null || modem?.lock?.wizard?.steps.length < 1) {
                setActiveStep(0);
            } else if (modem?.lock?.wizard?.steps[modem?.lock?.wizard?.steps.length - 1].type === 'CHECKING_CONNECTION') {
                setActiveStep(1);
            } else if (modem?.lock?.wizard?.steps[modem?.lock?.wizard?.steps.length - 1].type === 'CHECK_CONNECTION') {
                setActiveStep(2);
            } else if (modem?.lock?.wizard?.steps[modem?.lock?.wizard?.steps.length - 1].type === 'SELECT_INTERFACE') {
                setActiveStep(3);
            }
        }
    }, [modem]);

    const handleStart = () => {
        setStarting(true);
        diagnose(modem.modem.id)
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

    const handleStop = () => {
        stopDiagnose(modem.modem.id)
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

    const handleNext = () => {
        setActiveStep((prevActiveStep) => prevActiveStep + 1);
    };

    const handleBack = () => {
        setActiveStep((prevActiveStep) => prevActiveStep - 1);
    };

    const handleReset = () => {
        setActiveStep(0);
    };

    return (
        <Box sx={{ width: '100%' }}>
            {/* <Stepper activeStep={activeStep}>
                {steps.map((label, index) => {
                    const stepProps = {};
                    const labelProps = {};
                    if (isStepSkipped(index)) {
                        stepProps.completed = false;
                    }
                    return (
                        <Step key={label} {...stepProps}>
                            <StepLabel {...labelProps}>{label}</StepLabel>
                        </Step>
                    );
                })}
            </Stepper> */}
            {activeStep === steps.length ? (
                <React.Fragment>
                    <Typography sx={{ mt: 2, mb: 1 }}>All steps completed - you&apos;re finished</Typography>
                    <Box sx={{ display: 'flex', flexDirection: 'row', pt: 2 }}>
                        <Box sx={{ flex: '1 1 auto' }} />
                        <Button onClick={handleReset}>Reset</Button>
                    </Box>
                </React.Fragment>
            ) : (
                <React.Fragment>
                    <DiagnoseStepContent
                        activeStep={activeStep}
                        modem={modem}
                        running={running}
                        onStart={handleStart}
                        onStop={handleStop}
                    />
                    <BootstrapDialogActions>
                        {!running ? (
                            <Button onClick={handleStart} variant="outlined" disabled={starting}>
                                <FormattedMessage id="app.components.modem.Diagnose.start" />
                            </Button>
                        ) : (
                            <Button onClick={handleStop} variant="outlined" disabled={enableCancel}>
                                <FormattedMessage id="app.components.modem.Diagnose.stop" />
                            </Button>
                        )}
                    </BootstrapDialogActions>
                </React.Fragment>
            )}
        </Box>
    );
};

export default DiagnoseStepper;
