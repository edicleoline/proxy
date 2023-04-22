import { SET_SERVER_STATE } from './actions/types';

export const initialState = {
    state: null
};

const serverStateReducer = (state = initialState, action) => {
    switch (action.type) {
        case SET_SERVER_STATE:
            return {
                ...state,
                state: action.state
            };
        default:
            return state;
    }
};

export default serverStateReducer;
