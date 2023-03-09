import api from '../../api';

export function getServer() {
    return new Promise((resolve, reject) => {
        api.get('/server').then(
            (response) => {
                resolve(response.data);
            },
            (error) => {
                reject(error);
            }
        );
    });
}
