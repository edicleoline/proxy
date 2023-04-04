import { SET_MODEMS_DETAILS_ITEMS } from './types';

const setModemsDetailsItems = (items = []) => {
    return {
        type: SET_MODEMS_DETAILS_ITEMS,
        items: items
    };
};

export default setModemsDetailsItems;
