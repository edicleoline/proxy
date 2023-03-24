import axios from 'axios';
import { getToken } from './auth';
import config from 'config';

const api = axios.create({
    baseURL: config.api.baseURL,
    headers: {
        'Content-Type': 'application/json',
        Accept: 'application/json'
    },
    timeout: 15000,
    requireAuth: true
});

api.interceptors.response.use(
    (response) => {
        return response;
    },
    (error) => {
        if (error.request._hasError === true && error.request._response.includes('connect')) {
            console.log('connect error');
        }

        if (error.config.requireAuth && error.response && error.response.status === 401) {
            window.location.replace('/login');
        }

        return Promise.reject(error);
    }
);

api.interceptors.request.use(
    (config) => {
        const token = getToken();
        if (token && token.access_token) {
            config.headers['Authorization'] = 'Bearer ' + token.access_token;
        }

        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

export default api;
