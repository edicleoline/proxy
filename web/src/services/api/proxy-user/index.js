import api from '../../api';

export function getProxyUsers() {
    return new Promise((resolve, reject) => {
        api.get('/proxy-users').then(
            (response) => {
                resolve(response.data);
            },
            (error) => {
                reject(error);
            }
        );
    });
}

export function getProxyUserByUsername(username) {
    return new Promise((resolve, reject) => {
        api.get(`/proxy-user/by-username/${username}`).then(
            (response) => {
                resolve(response.data);
            },
            (error) => {
                reject(error);
            }
        );
    });
}

export function getProxyUserFilters(proxyUserId, modemId) {
    return new Promise((resolve, reject) => {
        api.get(`proxy-user/${proxyUserId}/modem/${modemId}/filters`).then(
            (response) => {
                resolve(response.data);
            },
            (error) => {
                reject(error);
            }
        );
    });
}
