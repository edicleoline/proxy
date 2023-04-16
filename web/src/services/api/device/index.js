import api from '../../api';

export function getDevices() {
    return new Promise((resolve, reject) => {
        api.get('/devices').then(
            (response) => {
                resolve(response.data);
            },
            (error) => {
                reject(error);
            }
        );
    });
}
