import { ADD_DOCK, REMOVE_DOCK, UPDATE_DOCK_STATE } from './actions/types';

export const initialState = {
    docks: []
};

const dockerReducer = (state = initialState, action) => {
    switch (action.type) {
        case ADD_DOCK:
            return {
                ...state,
                docks: [...state.docks, action.dock]
            };
        case REMOVE_DOCK:
            return {
                ...state,
                docks: state.docks.filter((item) => item.dock.id !== action.id)
            };
        case UPDATE_DOCK_STATE:
            const newState = state.docks.map((item) => {
                if (item.dock.id === action.id) {
                    return {
                        ...item,
                        dock: {
                            ...item.dock,
                            state: action.state
                        }
                    };
                }

                return item;
            });

            return {
                ...state,
                docks: newState
            };
        default:
            return state;
    }
};

export default dockerReducer;
