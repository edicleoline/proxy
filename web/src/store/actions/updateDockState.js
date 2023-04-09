import { UPDATE_DOCK_STATE } from './types';

const updateDockState = (id, state) => {
    return {
        type: UPDATE_DOCK_STATE,
        id: id,
        state: state
    };
};

export default updateDockState;
