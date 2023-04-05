import { ADD_NOTIFICATION, REMOVE_NOTIFICATION } from './actions/types';

export const initialState = {
    items: []
};

const notificationsReducer = (state = initialState, action) => {
    switch (action.type) {
        case ADD_NOTIFICATION:
            return {
                ...state,
                items: [...state.items, action.notification]
            };
        case REMOVE_NOTIFICATION:
            return {
                ...state,
                items: state.items.filter((item) => item.id !== action.notification.id)
            };
        default:
            return state;
    }
};

export default notificationsReducer;
