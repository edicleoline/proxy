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

socket.on('modems', (modems) => {
    const pendingReloads = pendingReloadModemsInQueue();
    const replaceItems = pendingReloads.map((replaceItem) => {
        return { modem: { id: replaceItem.data.modem.id } };
    });
    if (replaceItems && replaceItems.length > 0) {
        removeCommandsFromQueue(pendingReloads);
    }

    store.dispatch(setModemsItems(modems, replaceItems));
});

socket.on('modems_details', (modems) => {
    store.dispatch(setModemsDetailsItems(modems));
});

socket.on('server_control', (serverControl) => {
    addCommandInQueue(serverControl);
});

socket.on('modem_log', (message) => {
    storeModemLog(message);
});

socket.on('connect', () => {
    console.log('socket.io: connected');
});

socket.on('disconnect', () => {
    console.log('socket.io: disconnected');
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
