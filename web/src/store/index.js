import { configureStore } from '@reduxjs/toolkit';
import customizationReducer from './customizationReducer';
import dockerReducer from './dockerReducer';
import modemsReducer from './modemsReducer';
import notificationsReducer from './notificationsReducer';
import serverControlReducer from './serverControlReducer';
import serverStateReducer from './serverStateReducer';

const persistedState = localStorage.getItem('reduxState') ? JSON.parse(localStorage.getItem('reduxState')) : {};

const store = configureStore({
    reducer: {
        customization: customizationReducer,
        modems: modemsReducer,
        serverControl: serverControlReducer,
        notifications: notificationsReducer,
        docker: dockerReducer,
        serverState: serverStateReducer
    },
    middleware: (getDefaultMiddleware) =>
        getDefaultMiddleware({
            immutableCheck: false,
            serializableCheck: false
        }),
    preloadedState: persistedState
});
store.subscribe(() => {
    localStorage.setItem('reduxState', JSON.stringify(store.getState()));
});
const persister = 'Free';

export { store, persister };
