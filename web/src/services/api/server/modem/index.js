import api from '../../../api';

export function getModem() {
    return new Promise((resolve, reject) => {
        api.get('/server/modem').then(
            (response) => {
                resolve(response.data.items);
            },
            (error) => {
                reject(error);
            }
        );
    });
}
