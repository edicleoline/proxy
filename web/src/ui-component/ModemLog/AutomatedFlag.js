import PropTypes from 'prop-types';
import styled from 'styled-components';
import IntlMessageFormat from 'intl-messageformat';
import { locale, messages } from 'i18n';
import Tooltip from '@mui/material/Tooltip';
import { IconRotateClockwise2 } from '@tabler/icons';

const AutomatedFlagContainer = styled.div`
    position: absolute;
    top: -10px;
    right: -10px;
    width: 22px;
    height: 24px;
    background: #f0f0f0;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
`;

const AutomatedFlag = ({ message }) => {
    const translatedDescription = new IntlMessageFormat(messages[locale()][message.description], locale());
    return (
        <AutomatedFlagContainer>
            <Tooltip title={translatedDescription.format()}>
                <div style={{ display: 'flex' }}>
                    <IconRotateClockwise2 size="18" />
                </div>
            </Tooltip>
        </AutomatedFlagContainer>
    );
};

AutomatedFlag.propTypes = {
    message: PropTypes.object
};

export default AutomatedFlag;
