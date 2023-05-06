import api from '..';

export function getIpLabels() {
    return new Promise((resolve, reject) => {
        api.get('/ip-labels').then(
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
        api.get(`/ip-label/by-label/${label}`).then(
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
        api.get(`/ip-label/${ipLabelId}/modem/${modemId}/filters`).then(
            (response) => {
                resolve(response.data);
            },
            (error) => {
                reject(error);
            }
        );
    });
}
