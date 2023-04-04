import { ADD_COMMAND_CONTROL } from './types';

const addCommandServerControl = (command) => {
    return {
        type: ADD_COMMAND_CONTROL,
        command: command
    };
};

export default addCommandServerControl;
