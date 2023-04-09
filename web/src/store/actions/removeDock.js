import { REMOVE_DOCK } from './types';

const removeDock = (id) => {
    return {
        type: REMOVE_DOCK,
        id: id
    };
};

export default removeDock;
