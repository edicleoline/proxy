import api from '../../../api';

export function getModems() {
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

export function getModem(id) {
    return new Promise((resolve, reject) => {
        api.get('/server/modem/' + id).then(
            (response) => {
                resolve(response.data);
            },
            (error) => {
                reject(error);
            }
        );
    });
}
