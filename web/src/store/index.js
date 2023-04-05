import { configureStore } from '@reduxjs/toolkit';
import customizationReducer from './customizationReducer';
import modemsDetailsReducer from './modemsDetailsReducer';
import modemsReducer from './modemsReducer';
import notificationsReducer from './notificationsReducer';
import serverControlReducer from './serverControlReducer';

const store = configureStore({
    reducer: {
        customization: customizationReducer,
        modems: modemsReducer,
        modemsDetails: modemsDetailsReducer,
        serverControl: serverControlReducer,
        notifications: notificationsReducer
    },
    middleware: (getDefaultMiddleware) =>
        getDefaultMiddleware({
            immutableCheck: false,
            serializableCheck: false
        })
});
const persister = 'Free';

export { store, persister };
