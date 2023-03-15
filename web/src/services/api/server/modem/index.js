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

export function reboot(id, hardReset = false) {
    const data = {
        hard_reset: hardReset
    };
    return new Promise((resolve, reject) => {
        api.post('/server/modem/' + id + '/reboot', data).then(
            (response) => {
                resolve(response.data);
            },
            (error) => {
                reject(error);
            }
        );
    });
}

export function rotate(id, hardReset = false, user = null, ipv4Filter = null) {
    const data = {
        hard_reset: hardReset,
        user: user,
        ipv4_filter: ipv4Filter
    };
    return new Promise((resolve, reject) => {
        api.post('/server/modem/' + id + '/rotate', data).then(
            (response) => {
                resolve(response.data);
            },
            (error) => {
                reject(error);
            }
        );
    });
}
