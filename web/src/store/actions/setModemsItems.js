import { SET_MODEMS_ITEMS } from './types';

const setModemsItems = (items = [], replaceItems = []) => {
    return {
        type: SET_MODEMS_ITEMS,
        items: items,
        replaceItems: replaceItems
    };
};

export default setModemsItems;
