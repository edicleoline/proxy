import PropTypes from 'prop-types';
import styled from 'styled-components';
import { FormattedMessage } from 'react-intl';
import { Grid, Card, CardContent, Typography } from '@mui/material';
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
        <Grid container direction="column" justifyContent="center" alignItems="center">
            {/* <Grid item style={{ opacity: '0.2' }}>
                <Lottie options={lottieDefaultOptions} height={80} width={120} isStopped={false} isPaused={false} />
            </Grid> */}
            <Grid item sx={{ opacity: '0.5', whiteSpace: 'pre-line', textAlign: 'center', maxWidth: '90% !important' }}>
                <FormattedMessage id="app.log.modem.empty" values={{ modemId: modem.id }} />
            </Grid>
        </Grid>
    );
};

Empty.propTypes = {
    modem: PropTypes.object
};

export default Empty;
