import PropTypes from 'prop-types';
import styled from 'styled-components';

import IconButton from '@mui/material/IconButton';
import Tooltip from '@mui/material/Tooltip';
import { IconRotateClockwise2 } from '@tabler/icons';

import IntlMessageFormat from 'intl-messageformat';
import { locale, messages } from 'i18n';
import config from 'config';

const AutomatedFlagContainer = styled.div`
    position: absolute;
    top: -3px;
    width: 24px;
    height: 24px;
    border-radius: 50%;
    display: flex;
    -webkit-box-align: center;
    align-items: center;
    -webkit-box-pack: center;
    justify-content: center;
    margin-left: 24px;
`;

const AutomatedFlagIconWrapper = styled.div`
    position: relative;
    width: 24px;
    height: 24px;
    // background: #ede7f6;
    background: transparent;
    border-radius: 50%;
    display: flex;
    -webkit-box-align: center;
    align-items: center;
    -webkit-box-pack: center;
    justify-content: center;
`;

const AutomatedFlagBadgeWrapper = styled.span`
    display: flex;
    flex-flow: row wrap;
    -webkit-box-pack: center;
    place-content: center;
    -webkit-box-align: center;
    align-items: center;
    position: absolute;
    box-sizing: border-box;
    font-weight: 500;
    font-size: 0.75rem;
    min-width: 20px;
    line-height: 1;
    padding: 0px 6px;
    height: 20px;
    border-radius: 10px;
    z-index: 1;
    transition: transform 225ms cubic-bezier(0.4, 0, 0.2, 1) 0ms;
    background-color: rgb(156, 39, 176);
    color: rgb(255, 255, 255);
    top: 1px;
    margin-left: 0px;
    transform: scale(1) translate(50%, -50%);
    transform-origin: 100% 0%;
`;

const ModemAutoRotateFlag = ({ modem, onAutoRotateIconClick }) => {
    const title = new IntlMessageFormat(messages[locale()][`app.components.modem.rotate.automated.tooltip`], locale());
    return (
        <AutomatedFlagContainer>
            <AutomatedFlagIconWrapper>
                <Tooltip title={title.format()}>
                    <IconButton color="secondary" onClick={onAutoRotateIconClick(modem)}>
                        <IconRotateClockwise2 size="18" />
                    </IconButton>
                </Tooltip>
            </AutomatedFlagIconWrapper>
            {!modem.lock &&
            modem.schedule?.time_left_to_run <= config.options.autoRotateNotifyIn &&
            modem.schedule?.time_left_to_run > 0 ? (
                <AutomatedFlagBadgeWrapper>{modem.schedule?.time_left_to_run}</AutomatedFlagBadgeWrapper>
            ) : null}
        </AutomatedFlagContainer>
    );
};

ModemAutoRotateFlag.propTypes = {
    onAutoRotateIconClick: PropTypes.func.isRequired,
    modem: PropTypes.object
};

export default ModemAutoRotateFlag;
