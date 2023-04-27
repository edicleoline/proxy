import { createRoot } from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import { Provider } from 'react-redux';
import * as serviceWorker from 'serviceWorker';
import App from 'App';
import { store } from 'store';
import 'assets/scss/style.scss';
import config from './config';
import { IntlProvider } from 'react-intl';
import { locale, messages } from 'i18n';
import { SnackbarProvider, useSnackbar } from 'notistack';

const container = document.getElementById('root');
const root = createRoot(container); // createRoot(container!) if you use TypeScript
root.render(
    <Provider store={store}>
        <BrowserRouter basename={config.basename}>
            <IntlProvider locale={locale()} messages={messages[locale()]}>
                <SnackbarProvider preventDuplicate anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}>
                    <App />
                </SnackbarProvider>
            </IntlProvider>
        </BrowserRouter>
    </Provider>
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
