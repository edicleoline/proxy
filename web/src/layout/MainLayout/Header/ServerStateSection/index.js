import PropTypes from 'prop-types';
import { useState, useEffect } from 'react';
import { Box, Grid } from '@mui/material';
import { useSelector } from 'react-redux';
import { useTheme } from '@mui/material/styles';
import styled from 'styled-components';

const ProgressBar = styled.div`
    position: absolute;
    top: 0;
    left: 0;
    background-color: ${(props) => props.backgroundColor};
    width: ${(props) => props.width}%;
    height: 100%;
    z-index: 0;
    -webkit-transition: width 0.3s ease-in-out;
    -moz-transition: width 0.3s ease-in-out;
    -o-transition: width 0.3s ease-in-out;
    transition: width 0.3s ease-in-out;
`;

const ValueText = styled.div`
    position: relative;
    text-align: center;
    z-index: 1;
`;

const styledContainer = {
    // minWidth: '100px'
};

const labelContainer = {
    borderRadius: '32px 0 0 32px',
    padding: '6px 6px 6px 12px',
    borderRight: 'solid 1px #fff',
    zIndex: 1
};

const valueContainer = {
    borderRadius: '0 32px 32px 0',
    padding: '6px 12px 6px 6px',
    overflow: 'hidden',
    position: 'relative',
    zIndex: 1
};

const ServerStateSection = () => {
    const serverState = useSelector((state) => state.serverState.state);
    const theme = useTheme();

    return (
        <>
            <Box sx={{ ml: 2, mr: 3 }}>
                <Grid
                    container
                    justifyContent="flex-start"
                    alignItems="start"
                    direction="row"
                    sx={{ overflow: 'hidden', position: 'relative' }}
                >
                    <Grid item sx={{ mr: 1, overflow: 'hidden', position: 'relative', borderRadius: '32px' }}>
                        <Grid
                            container
                            justifyContent="flex-start"
                            alignItems="start"
                            direction="row"
                            sx={{ ...styledContainer, background: theme.palette.primary.light }}
                        >
                            <Grid item sx={{ ...labelContainer }}>
                                CPU
                            </Grid>
                            <Grid item sx={{ ...valueContainer, minWidth: '56px' }}>
                                <ProgressBar backgroundColor={theme.palette.secondary.light} width={serverState.cpu_percent} />
                                <ValueText>{serverState.cpu_percent}%</ValueText>
                            </Grid>
                        </Grid>
                    </Grid>
                    <Grid item sx={{ overflow: 'hidden', position: 'relative', borderRadius: '32px' }}>
                        <Grid
                            container
                            justifyContent="flex-start"
                            alignItems="start"
                            direction="row"
                            sx={{ ...styledContainer, background: theme.palette.primary.light }}
                        >
                            <Grid item sx={{ ...labelContainer }}>
                                RAM
                            </Grid>
                            <Grid item sx={{ ...valueContainer, minWidth: '56px' }}>
                                <ProgressBar backgroundColor={theme.palette.secondary.light} width={serverState.virtual_memory.percent} />
                                <ValueText>{serverState.virtual_memory.percent}%</ValueText>
                            </Grid>
                        </Grid>
                    </Grid>
                </Grid>
            </Box>
        </>
    );
};

export default ServerStateSection;
