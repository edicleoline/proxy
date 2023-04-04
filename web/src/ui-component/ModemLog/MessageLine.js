import PropTypes from 'prop-types';
import styled from 'styled-components';
import { Grid } from '@mui/material';
import Message from './Message';
import AutomatedFlag from './AutomatedFlag';

const MessageSystemContainer = styled.div`
    border-radius: 4px 4px 4px 4px;
    position: relative;
    box-shadow: 1px 1px 1px rgb(0 0 0 / 5%);
    overflow: hidden;
    &:after {
        position: absolute;
        content: '';
        width: 0;
        height: 0;
        border-style: solid;
        border-width: 0px 10px 10px 0;
        border-color: transparent #ffffff transparent transparent;
        top: 0;
        left: -10px;
    }
`;

const MessageUserContainer = styled.div`
    background-color: #ede7f6;
    border-radius: 4px 4px 4px 4px;
    position: relative;
    box-shadow: -1px 1px 1px rgb(0 0 0 / 5%);
    overflow: hidden;
    &:after {
        position: absolute;
        content: '';
        width: 0;
        height: 0;
        border-style: solid;
        border-width: 0px 0 10px 10px;
        border-color: transparent transparent transparent #e1ffc7;
        top: 0;
        right: -10px;
    }
`;

const SeparatorDate = styled.span`
    display: inline-block;
    padding: 0 6px;
    position: relative;
    font-size: 0.8rem;
    background-color: #555;
    color: #fff;
    line-height: 1.4rem;
    border-radius: 4px;
`;

const MessageLine = ({ container }) => {
    if (container.type == 'separator') {
        const style = {
            width: '100%',
            marginBottom: '10px',
            marginTop: !container.isFirst ? '20px' : '0'
        };
        return (
            <Grid item style={style}>
                <Grid container justifyContent="center" alignItems="center" direction="column">
                    <Grid item>
                        <SeparatorDate>{container.value}</SeparatorDate>
                    </Grid>
                </Grid>
            </Grid>
        );
    }

    const message = container.value;
    return (
        <Grid item style={{ width: '100%', marginBottom: '10px' }}>
            <Grid
                container
                justifyContent="end"
                alignItems={message.owner == 'SYSTEM' ? 'flex-start' : 'flex-end'}
                direction="column"
                sx={{ position: 'relative' }}
            >
                <Grid item style={{ maxWidth: '85%' }}>
                    {message.owner == 'SYSTEM' ? (
                        <MessageSystemContainer>
                            <Message message={message} />
                        </MessageSystemContainer>
                    ) : (
                        <Grid container justifyContent="end" alignItems="flex-end" direction="column">
                            <Grid item>
                                <MessageUserContainer>
                                    <Message message={message} />
                                </MessageUserContainer>
                                {message.auto == true ? <AutomatedFlag message={message} /> : null}
                            </Grid>
                        </Grid>
                    )}
                </Grid>
            </Grid>
        </Grid>
    );
};

MessageLine.propTypes = {
    container: PropTypes.object
};

export default MessageLine;
