import PropTypes from 'prop-types';
import { FormattedMessage } from 'react-intl';
import styled from 'styled-components';

import IconButton from '@mui/material/IconButton';
import Tooltip from '@mui/material/Tooltip';
import { IconAlertCircle } from '@tabler/icons';
import ModemStatusBox from 'views/modems/ModemStatusBox';

const StoppingContainer = styled.div`
    position: absolute;
    right: 6px;
    top: 6px;
    background-color: #ffffff;
    border-radius: 50%;
`;

const ModemStatus = ({ lock, connected, onStoppingTaskClick }) => {
    if (!lock) {
        const color = connected ? 'success.light' : 'orange.light';
        const title = connected ? 'Conectado' : 'Desconectado';
        return <ModemStatusBox bgcolor={color} title={title} dark style={{ width: '100%' }} />;
    }

    let lockLabel = lock.task.name;
    if (lock.task.name === 'ROTATE') {
        lockLabel = 'Rotacionando';
    } else if (lock.task.name === 'REBOOT') {
        lockLabel = 'Reiniciando';
    }

    return (
        <>
            <div>
                <ModemStatusBox bgcolor={'#e8e1ff'} title={lockLabel} dark />
                {lock.task.stopping == true ? (
                    <StoppingContainer>
                        <Tooltip title="Cancelando tarefa">
                            <IconButton
                                aria-label="close"
                                onClick={onStoppingTaskClick}
                                sx={{
                                    color: (theme) => theme.palette.grey[500]
                                }}
                                size="small"
                            >
                                <IconAlertCircle fontSize="inherit" />
                            </IconButton>
                        </Tooltip>
                    </StoppingContainer>
                ) : null}
            </div>
        </>
    );
};

ModemStatus.propTypes = {
    connected: PropTypes.bool.isRequired,
    onStoppingTaskClick: PropTypes.func.isRequired
};

export default ModemStatus;
