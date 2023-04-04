import objectHash from 'object-hash';
import { SET_MODEMS_DETAILS_ITEMS } from './actions/types';

export const initialState = {
    items: [],
    hash: objectHash.MD5([])
};

const merge = (oldState, newItems = []) => {
    const newHash = newItems ? objectHash.MD5(newItems) : objectHash.MD5([]);
    const oldItems = oldState.items;

    if (oldItems && newItems && oldItems.length != newItems.length) {
        return {
            items: newItems,
            hash: newHash,
            updated: true
        };
    }

    const oldHash = oldState.hash;

    if (oldHash === newHash) {
        return {
            items: oldItems,
            hash: oldHash,
            updated: false
        };
    }

    return {
        items: newItems,
        hash: newHash,
        updated: true
    };
};

const modemsDetailsReducer = (state = initialState, action) => {
    switch (action.type) {
        case SET_MODEMS_DETAILS_ITEMS:
            const merged = merge(state, action.items);
            if (!merged.updated) {
                return state;
            }

            return {
                ...state,
                items: merged.items,
                hash: merged.hash
            };
        default:
            return state;
    }
};

export default modemsDetailsReducer;
