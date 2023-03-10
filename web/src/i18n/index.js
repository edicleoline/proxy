import ptTranslationMessages from 'i18n/translations/pt';
import enTranslationMessages from 'i18n/translations/en';

const DEFAULT_LOCALE = 'pt';

const messages = {
    pt: ptTranslationMessages,
    en: enTranslationMessages
};

const locale = () => {
    return DEFAULT_LOCALE;
};

// const test = () => {
//     console.log(enTranslationMessages.test);
//     console.log('test function export');

//     const language = navigator.language.split(/[-_]/)[0];
//     console.log(language);
// };

// const test2 = () => {
//     console.log(ptTranslationMessages.test);
//     console.log('test function export 2');
// };

// export { test, test2 };
export { DEFAULT_LOCALE, locale, messages };
