import api from '..';

export function getMiddlewares() {
    return new Promise((resolve, reject) => {
        api.get('/middlewares').then(
            (response) => {
                resolve(response.data);
            },
            (error) => {
                reject(error);
            }
        );
    });
}
