// assets
import { IconAdjustments, IconAccessPoint } from '@tabler/icons';

// constant
const icons = {
    IconAdjustments,
    IconAccessPoint
};

// ==============================|| EXTRA PAGES MENU ITEMS ||============================== //

const configurations = {
    id: 'configurations',
    title: 'Gerenciamento',
    caption: 'versão beta',
    type: 'group',
    children: [
        {
            id: 'modems',
            title: 'Modems',
            type: 'item',
            url: '/modems',
            icon: icons.IconAccessPoint,
            breadcrumbs: false
        },
        {
            id: 'settings',
            title: 'Configurações',
            type: 'collapse',
            icon: icons.IconAdjustments,

            children: [
                {
                    id: 'login3',
                    title: 'Login',
                    type: 'item',
                    url: '/login',
                    target: true
                },
                {
                    id: 'register3',
                    title: 'Register',
                    type: 'item',
                    url: '/register',
                    target: true
                }
            ]
        }
    ]
};

export default configurations;
