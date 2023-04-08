import PropTypes from 'prop-types';
import styled from 'styled-components';
import { FormattedMessage } from 'react-intl';
import { Grid, Card, CardContent } from '@mui/material';
import Lottie from 'react-lottie';
import * as animationAstronaut from 'assets/animation/astronaut';

const MessageContainer = styled.div`
    word-wrap: break-word;
    white-space: pre-line;
`;

const Empty = ({ modem }) => {
    const lottieDefaultOptions = {
        loop: true,
        autoplay: true,
        animationData: animationAstronaut,
        rendererSettings: {
            preserveAspectRatio: 'xMidYMid slice'
        }
    };

    return (
        <Grid container direction="column" justifyContent="end" alignItems="center">
            <Grid item style={{ opacity: '0.2' }}>
                <Lottie options={lottieDefaultOptions} height={80} width={120} isStopped={false} isPaused={false} />
            </Grid>
            <Grid item sx={{ marginTop: '32px' }}>
                Até agora, nada por aqui
            </Grid>
        </Grid>
    );
};

Empty.propTypes = {
    modem: PropTypes.object
};

export default Empty;
