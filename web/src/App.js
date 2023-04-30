import { useSelector } from 'react-redux';
import { connect } from 'react-redux';
import { ThemeProvider } from '@mui/material/styles';
import { CssBaseline, StyledEngineProvider } from '@mui/material';
import Routes from 'routes';
import themes from 'themes';
import NavigationScroll from 'layout/NavigationScroll';
import socket from 'services/socketio';
import { store } from 'store';
import setModemsItems from 'store/actions/setModemsItems';
import { pendingReloadModemsInQueue, addCommandInQueue, removeCommandsFromQueue } from 'services/server-control';
import setModemsDetailsItems from 'store/actions/setModemsDetailsItems';
import { storeModemLog } from 'storage/modem/log';
import { SERVER_EVENT_TYPE } from 'store/constant';
import addNotification from 'store/actions/addNotification';
import { FormattedMessage } from 'react-intl';
import IntlMessageFormat from 'intl-messageformat';
import { locale, messages } from 'i18n';
import { useEffect } from 'react';
import setServerState from 'store/actions/setServerState';
import { SET_MODEMS_ITEMS } from 'store/actions/types';

socket.on('modems', (modems) => {
    const pendingReloads = pendingReloadModemsInQueue();
    const replaceItems = pendingReloads.map((replaceItem) => {
        return { modem: { id: replaceItem.data.modem.id } };
    });
    if (replaceItems && replaceItems.length > 0) {
        removeCommandsFromQueue(pendingReloads);
    }

    store.dispatch(setModemsItems(modems, replaceItems));
    // store.dispatch({ type: SET_MODEMS_ITEMS, items: modems, replaceItems: replaceItems });
});

socket.on('server_state', (serverState) => {
    // console.log(serverState);
    store.dispatch(setServerState(serverState));
});

socket.on('server_control', (serverControl) => {
    console.log(serverControl);
    addCommandInQueue(serverControl);
});

socket.on('event', (event) => {
    console.log(event);
    let message = '';
    switch (event.type) {
        case SERVER_EVENT_TYPE.MODEM.LOG:
            storeModemLog(event.data);
            break;
        case SERVER_EVENT_TYPE.MODEM.UNEXPECTED_DISCONNECT:
            message = new IntlMessageFormat(messages[locale()]['app.notification.modem.unexpectedDisconnect'], locale()).format({
                modemId: event.data.modem.id
            });
            break;
        case SERVER_EVENT_TYPE.MODEM.CONNECT:
            message = new IntlMessageFormat(messages[locale()]['app.notification.modem.unexpectedDisconnect'], locale()).format({
                modemId: event.data.modem.id
            });
            break;
        default:
            break;
    }

    if (event.type === SERVER_EVENT_TYPE.MODEM.UNEXPECTED_DISCONNECT || event.type === SERVER_EVENT_TYPE.MODEM.CONNECT) {
        store.dispatch(
            addNotification({
                id: event.id,
                message: message,
                props: {
                    open: true,
                    autoHideDuration: 10000,
                    alert: false
                },
                ref: event
            })
        );
        return;
    }
});

socket.on('connect', () => {
    console.log('socketio: connected');
});

socket.on('disconnect', () => {
    console.log('socketio: disconnected');
});

const App = () => {
    const customization = useSelector((state) => state.customization);

    // useEffect(() => {
    //     store.dispatch(setModemsItems([], []));
    // }, []);

    return (
        <StyledEngineProvider injectFirst>
            <ThemeProvider theme={themes(customization)}>
                <CssBaseline />
                <NavigationScroll>
                    <Routes />
                </NavigationScroll>
            </ThemeProvider>
        </StyledEngineProvider>
    );
};

// const mapStateToProps = (state) => ({
//     state: state
// });

// export default connect(mapStateToProps)(App);
export default App;
