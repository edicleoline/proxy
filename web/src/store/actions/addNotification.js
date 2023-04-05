import { ADD_NOTIFICATION } from './types';

const addNotification = (notification) => {
    return {
        type: ADD_NOTIFICATION,
        notification: notification
    };
};

export default addNotification;
