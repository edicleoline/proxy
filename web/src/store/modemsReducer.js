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
        for (let newItem of newItems) {
            if (oldItem.modem.id !== newItem.modem.id) {
                continue;
            }

            if (replaceItems) {
                const found = replaceItems.find((x) => x.modem.id === newItem.modem.id);
                if (found) {
                    updated = true;
                    oldItem = newItem;
                    continue;
                }
            }

            if (oldItem.is_connected !== newItem.is_connected) {
                updated = true;
                oldItem.is_connected = newItem.is_connected;
                if (!newItem.is_connected) {
                    oldItem.connectivity = null;
                }
            }

            const oldItemConnectivityHash = newItem.connectivity ? objectHash(newItem.connectivity) : objectHash({});
            const newItemConnectivityHash = oldItem.connectivity ? objectHash(oldItem.connectivity) : objectHash({});
            if (oldItemConnectivityHash !== newItemConnectivityHash) {
                updated = true;
                oldItem.connectivity = newItem.connectivity;
            }

            const oldItemLockHash = oldItem.lock != null ? objectHash(oldItem.lock) : objectHash({});
            const newItemLockHash = newItem.lock != null ? objectHash(newItem.lock) : objectHash({});
            if (oldItemLockHash !== newItemLockHash) {
                updated = true;
                oldItem.lock = newItem.lock;
            }

            const oldItemClientsHash = oldItem.clients != null ? objectHash(oldItem.clients) : objectHash({});
            const newItemClientsHash = newItem.clients != null ? objectHash(newItem.clients) : objectHash({});
            if (oldItemClientsHash !== newItemClientsHash) {
                updated = true;
                oldItem.clients = newItem.clients;
            }

            if (
                oldItem.modem.schedule != newItem.modem.schedule ||
                objectHash.MD5(oldItem.modem.schedule) != objectHash.MD5(newItem.modem.schedule)
            ) {
                if (
                    newItem.modem.schedule?.time_left_to_run <= config.options.autoRotateNotifyIn ||
                    oldItem.modem.schedule?.added_at != newItem.modem.schedule?.added_at
                ) {
                    oldItem.modem.schedule = newItem.modem.schedule;
                    updated = true;
                }
            }
        }

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
