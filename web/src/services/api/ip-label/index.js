import api from '..';

export function getIpLabels() {
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

export function getIpLabel(label) {
    return new Promise((resolve, reject) => {
        api.get(`/proxy-user/by-username/${label}`).then(
            (response) => {
                resolve(response.data);
            },
            (error) => {
                reject(error);
            }
        );
    });
}

export function getIpLabelFilters(ipLabelId, modemId) {
    return new Promise((resolve, reject) => {
        api.get(`proxy-user/${ipLabelId}/modem/${modemId}/filters`).then(
            (response) => {
                resolve(response.data);
            },
            (error) => {
                reject(error);
            }
        );
    });
}
