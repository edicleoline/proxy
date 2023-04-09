import { ADD_DOCK } from './types';

const addDock = (dock) => {
    return {
        type: ADD_DOCK,
        dock: dock
    };
};

export default addDock;
