import PropTypes from 'prop-types';
import styled from 'styled-components';
import { FormattedMessage } from 'react-intl';
import moment from 'moment';
import MessageParams from './MessageParams';

const MessageContainer = styled.div`
    word-wrap: break-word;
    white-space: pre-line;
`;

const MessageText = styled.div`
    word-wrap: break-word;
    white-space: pre-line;
    padding: 8px 10px;
    background-color: #ffffff;
    overflow: hidden;

    &.error {
        background-color: #f6b9b969;
    }
    ,
    &.success {
        background-color: #b9f6ca8c;
    }
    ,
    &.info {
        background-color: #ffffff;
    }
    ,
    &.warning {
        background-color: #f6e6b969;
    }
`;

const MessageMetadata = styled.span`
    display: inline-block;
    float: right;
    padding: 0 0 0 7px;
    position: relative;
    bottom: -4px;
    font-size: 0.7rem;
    opacity: 0.5;
`;

const messageClassName = (message) => {
    const classname = message.type.toLowerCase();
    return classname;
};

const time = (dateTime) => {
    const dt = moment(dateTime);
    return dt.format('HH:mm');
};

const Message = ({ message }) => {
    return (
        <MessageContainer>
            <MessageText className={messageClassName(message)}>
                <FormattedMessage id={message.message} values={message.params} />
                <MessageMetadata>{time(message.logged_at)}</MessageMetadata>
            </MessageText>
            <MessageParams message={message} />
        </MessageContainer>
    );
};

Message.propTypes = {
    message: PropTypes.object
};

export default Message;
