import api from '../../../api';

export function logs(modemId, cursor, limit, direction, order) {
    return new Promise((resolve, reject) => {
        api.get(`modem/${modemId}/log?cursor=${cursor}&limit=${limit}&direction=${direction}&order=${order}`).then(
            (response) => {
                resolve(response.data.items);
            },
            (error) => {
                reject(error);
            }
        );
    });
}
