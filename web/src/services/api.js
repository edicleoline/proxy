import axios from 'axios';

const api = axios.default.create({
    baseURL: 'http://127.0.0.1:5000',
    timeout: 15000
});

api.interceptors.request.use(
    (config) => {
        console.log(config);

        config.headers['Authorization'] =
            'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNjc3NzIxNDE1LCJqdGkiOiJjMDI3NGEwYy1jY2EzLTRjYWMtYmFhNi01OGFkNzU4OGEwMDYiLCJ0eXBlIjoiYWNjZXNzIiwic3ViIjozLCJuYmYiOjE2Nzc3MjE0MTUsImV4cCI6MTY3NzcyMjMxNSwiaXNfYWRtaW4iOmZhbHNlfQ.tt0si7DXSjMMLvkYDZl41IZLHGL6WBvKhBzoFwVxsgc';

        return config;
    },
    (error) => {
        console.log(error);
        return Promise.reject(error);
    }
);

export default api;
