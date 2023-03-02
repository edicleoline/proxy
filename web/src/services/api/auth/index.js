import api from '../../api';

const saveToken = async (token) => {
    localStorage.setItem('token', JSON.stringify(token));
};

export function getToken() {
    const token = localStorage.getItem('token');
    return token ? JSON.parse(token) : token;
}

export function login(username, password) {
    const credentials = {
        username: username,
        password: password
    };

    const req = api.post('/login', credentials, {
        requireAuth: false
    });
    req.then(
        (response) => {
            const data = response.data;
            saveToken(data);
            console.log(data);
        },
        (error) => {
            console.log('TODO: log fail login', error);
        }
    );
    return req;
}
