import { REMOVE_NOTIFICATION } from './types';

const removeNotification = (notification) => {
    return {
        type: REMOVE_NOTIFICATION,
        notification: notification
    };
};

export default removeNotification;
