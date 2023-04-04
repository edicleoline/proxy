import { SET_COMMANDS_CONTROL } from './types';

const setCommandsServerControl = (commands) => {
    return {
        type: SET_COMMANDS_CONTROL,
        command: commands
    };
};

export default setCommandsServerControl;
