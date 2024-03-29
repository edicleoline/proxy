import api from '..';

export function getModems() {
    return new Promise((resolve, reject) => {
        api.get('/modem').then(
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
        api.get(`/modem/${id}`).then(
            (response) => {
                resolve(response.data);
            },
            (error) => {
                reject(error);
            }
        );
    });
}

export function saveModem(modem) {
    return new Promise((resolve, reject) => {
        api.put(`/modem/${modem.id}`, modem).then(
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
        api.post(`/modem/${id}/reboot`, data).then(
            (response) => {
                resolve(response.data);
            },
            (error) => {
                reject(error);
            }
        );
    });
}

export function rotate(id, hardReset = false, ip_label = null, filters = null) {
    const data = {
        hard_reset: hardReset,
        ip_label: ip_label,
        filters: filters
    };
    return new Promise((resolve, reject) => {
        api.post(`/modem/${id}/rotate`, data).then(
            (response) => {
                resolve(response.data);
            },
            (error) => {
                reject(error);
            }
        );
    });
}

export function stopRotate(id) {
    return new Promise((resolve, reject) => {
        api.delete(`/modem/${id}/rotate`).then(
            (response) => {
                resolve(response.data);
            },
            (error) => {
                reject(error);
            }
        );
    });
}

export function scheduleAutoRotate(id) {
    return new Promise((resolve, reject) => {
        api.get(`/modem/${id}/schedule/auto-rotate`).then(
            (response) => {
                resolve(response.data);
            },
            (error) => {
                reject(error);
            }
        );
    });
}

export function diagnose(id) {
    return new Promise((resolve, reject) => {
        api.post(`/modem/${id}/diagnose`).then(
            (response) => {
                resolve(response.data);
            },
            (error) => {
                reject(error);
            }
        );
    });
}

export function stopDiagnose(id) {
    return new Promise((resolve, reject) => {
        api.delete(`/modem/${id}/diagnose`).then(
            (response) => {
                resolve(response.data);
            },
            (error) => {
                reject(error);
            }
        );
    });
}

export function postLockWizardStepResponse(modemId, lockId, stepId, response) {
    return new Promise((resolve, reject) => {
        api.post(`/modem/${modemId}/lock/${lockId}/wizard/step/${stepId}/response`, response).then(
            (response) => {
                resolve(response.data);
            },
            (error) => {
                reject(error);
            }
        );
    });
}
