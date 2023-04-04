import config from 'config';
import * as types from './actions/types';

export const initialState = {
    isOpen: [],
    defaultId: 'default',
    fontFamily: config.fontFamily,
    borderRadius: config.borderRadius,
    opened: true
};

const customizationReducer = (state = initialState, action) => {
    let id;
    switch (action.type) {
        case types.MENU_OPEN:
            id = action.id;
            return {
                ...state,
                isOpen: [id]
            };
        case types.SET_MENU:
            return {
                ...state,
                opened: action.opened
            };
        case types.SET_FONT_FAMILY:
            return {
                ...state,
                fontFamily: action.fontFamily
            };
        case types.SET_BORDER_RADIUS:
            return {
                ...state,
                borderRadius: action.borderRadius
            };
        default:
            return state;
    }
};

export default customizationReducer;
