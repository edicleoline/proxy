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

socket.on('modems', (modems) => {
    //console.log(modems);
    const pendingReloads = pendingReloadModemsInQueue();
    const replaceItems = pendingReloads.map((replaceItem) => {
        return { modem: { id: replaceItem.data.modem.id } };
    });
    if (replaceItems && replaceItems.length > 0) {
        removeCommandsFromQueue(pendingReloads);
    }

    store.dispatch(setModemsItems(modems, replaceItems));
    // store.dispatch(setModemsItems(modems, []));
});

// socket.on('modems_details', (modems) => {
//     store.dispatch(setModemsDetailsItems(modems));
// });

socket.on('server_control', (serverControl) => {
    addCommandInQueue(serverControl);
    console.log(serverControl);
});

socket.on('event', (event) => {
    console.log(event);
    if (event.type === SERVER_EVENT_TYPE.MODEM.LOG) {
        storeModemLog(event.data);
        return;
    }

    if (event.type === SERVER_EVENT_TYPE.MODEM.UNEXPECTED_DISCONNECT) {
        store.dispatch(
            addNotification({
                id: event.id,
                message: <FormattedMessage id={'app.notification.modem.unexpectedDisconnect'} values={{ modemId: event.data.modem.id }} />,
                props: {
                    open: true,
                    autoHideDuration: 15000,
                    alert: false
                },
                ref: event
            })
        );
        return;
    }

    if (event.type === SERVER_EVENT_TYPE.MODEM.CONNECT) {
        store.dispatch(
            addNotification({
                id: event.id,
                message: <FormattedMessage id={'app.notification.modem.connect'} values={{ modemId: event.data.modem.id }} />,
                props: {
                    open: true,
                    autoHideDuration: 15000,
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

const mapStateToProps = (state) => ({
    state: state
});

export default connect(mapStateToProps)(App);
