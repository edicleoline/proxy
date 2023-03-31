const config = {
    // basename: only at build time to set, and Don't add '/' at end off BASENAME for breadcrumbs, also Don't put only '/' use blank('') instead,
    // like '/berry-material-react/react/default'
    basename: '/',
    defaultPath: '/dashboard/default',
    // fontFamily: `'Circular', 'Roboto', sans-serif`,
    fontFamily: `'Roboto', sans-serif`,
    borderRadius: 6,
    api: {
        baseURL: 'http://192.168.15.138:5000'
        // baseURL: 'http://192.168.15.10:5000'
    },
    socketio: {
        baseURL: 'http://192.168.15.138:5000'
        // baseURL: 'http://192.168.15.10:5000'
    }
};

export default config;
