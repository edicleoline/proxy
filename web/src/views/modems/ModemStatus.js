import PropTypes from 'prop-types';
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
        const bgcolor = connected ? 'success.light' : 'orange.light';
        const color = connected ? '#428554' : '#916a45';
        const title = connected ? 'Conectado' : 'Desconectado';
        return <ModemStatusBox bgcolor={bgcolor} color={color} title={title} style={{ width: '100%' }} />;
    }

    let lockLabel = lock.task.name;
    if (lock.task.name === 'ROTATE') {
        lockLabel = 'Rotacionando';
    } else if (lock.task.name === 'REBOOT') {
        lockLabel = 'Reiniciando';
    } else if (lock.task.name === 'DIAGNOSE') {
        lockLabel = 'Diagnosticando';
    }

    return (
        <>
            <div>
                <ModemStatusBox bgcolor="#e8e1ff" color="#635493" title={lockLabel} />
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
    onStoppingTaskClick: PropTypes.func.isRequired,
    modem: PropTypes.object,
    lock: PropTypes.object
};

export default ModemStatus;
