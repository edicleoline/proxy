import PropTypes from 'prop-types';
import styled from 'styled-components';
import { Grid } from '@mui/material';
import MessageParamItem from './MessageParamItem';

const ParamsContainer = styled.div`
    border-top: solid 1px #f0f0f0;
    padding: 8px 10px;
    clear: both;

    &.error {
        background-color: #f6b9b9a1;
        border-color: #f6b9b9a1;
    }
    ,
    &.success {
        background-color: #b9f6ca;
        border-color: #9ddfb15e;
    }
    ,
    &.info {
        background-color: #f9f9f9;
        border-color: #dddddd6e;
    }
    ,
    &.warning {
        background-color: #f6e3b9a1;
        border-color: #e3d1a078;
    }
`;

const messageClassName = (message) => {
    const classname = message.type.toLowerCase();
    return classname;
};

const MessageParams = ({ message }) => {
    if (!message || !('params' in message) || !message.params) {
        return null;
    }

    return (
        <ParamsContainer className={messageClassName(message)}>
            <Grid container justifyContent="end" alignItems="flex-start" direction="column">
                {Object.entries(message.params).map(([key, value], index) => (
                    <MessageParamItem key={index} pkey={key} pvalue={value} />
                ))}
            </Grid>
        </ParamsContainer>
    );
};

MessageParams.propTypes = {
    message: PropTypes.object
};

export default MessageParams;
