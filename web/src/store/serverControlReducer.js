import { ADD_COMMAND_CONTROL, SET_COMMANDS_CONTROL } from './actions/types';

export const initialState = {
    commands: []
};

export const commandStatus = {
    pending: 'PENDING',
    success: 'SUCCESS',
    error: 'ERROR'
};

const serverControlReducer = (state = initialState, action) => {
    switch (action.type) {
        case ADD_COMMAND_CONTROL:
            return {
                ...state,
                commands: [
                    ...state.commands,
                    {
                        id: action.command.id,
                        action: action.command.action,
                        data: action.command.data,
                        status: commandStatus.pending
                    }
                ]
            };
        case SET_COMMANDS_CONTROL:
            return {
                ...state,
                commands: action.commands ? action.commands : []
            };
        default:
            return state;
    }
};

export default serverControlReducer;
