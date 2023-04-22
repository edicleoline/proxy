import { SET_SERVER_STATE } from './types';

const setServerState = (state) => {
    return {
        type: SET_SERVER_STATE,
        state: state
    };
};

export default setServerState;
