import objectHash from 'object-hash';
import { SET_MODEMS_ITEMS } from './actions/types';
import config from 'config';
import cloneDeep from 'lodash/cloneDeep';

export const initialState = {
    items: [],
    hash: objectHash.MD5([])
};

const merge = (oldState, newItems = [], replaceItems = []) => {
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

    let updated = false;

    const items = oldItems.map(function (oldItem) {
        newItems.forEach((newItem) => {
            if (oldItem.id !== newItem.id) {
                return;
            }

            if (replaceItems) {
                const found = replaceItems.find((x) => x.modem.id === newItem.modem.id);
                if (found) {
                    updated = true;
                    const oldItemCloned = cloneDeep(oldItem);
                    oldItem = newItem;
                    if ('external_ip' in oldItemCloned) oldItem.external_ip = oldItemCloned.external_ip;
                    if ('device_network_type' in oldItemCloned) oldItem.device_network_type = oldItemCloned.device_network_type;
                    if ('device_network_provider' in oldItemCloned) oldItem.device_network_provider = oldItemCloned.device_network_provider;
                    if ('device_network_signalbar' in oldItemCloned)
                        oldItem.device_network_signalbar = oldItemCloned.device_network_signalbar;
                    if ('data' in oldItemCloned) oldItem.data = oldItemCloned.data;
                    return;
                }
            }

            if (oldItem.is_connected !== newItem.is_connected) {
                updated = true;
                oldItem.is_connected = newItem.is_connected;

                if (!newItem.is_connected) {
                    delete oldItem.external_ip;
                    delete oldItem.device_network_type;
                    delete oldItem.device_network_provider;
                    delete oldItem.device_network_signalbar;
                    delete oldItem.data;
                }
            }

            const oldItemLockHash = oldItem.lock != null ? objectHash(oldItem.lock) : objectHash({});
            const newItemLockHash = newItem.lock != null ? objectHash(newItem.lock) : objectHash({});
            if (oldItemLockHash !== newItemLockHash) {
                updated = true;
                oldItem.lock = newItem.lock;
            }

            if (oldItem.schedule != newItem.schedule || objectHash.MD5(oldItem.schedule) != objectHash.MD5(newItem.schedule)) {
                if (
                    newItem.schedule?.time_left_to_run <= config.options.autoRotateNotifyIn ||
                    oldItem.schedule?.added_at != newItem.schedule?.added_at
                ) {
                    oldItem.schedule = newItem.schedule;
                    updated = true;
                }
            }
        });

        return oldItem;
    });

    return {
        items: items,
        hash: objectHash.MD5(items),
        updated: updated
    };
};

const modemsReducer = (state = initialState, action) => {
    switch (action.type) {
        case SET_MODEMS_ITEMS:
            const merged = merge(state, action.items, action.replaceItems);
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

export default modemsReducer;
