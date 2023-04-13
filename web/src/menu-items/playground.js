import { IconAdjustments, IconAccessPoint, IconDeviceMobileMessage, IconRouter } from '@tabler/icons';

const icons = {
    IconAdjustments,
    IconAccessPoint,

    IconRouter,
    IconDeviceMobileMessage
};

const playground = {
    id: 'configurations',
    title: 'Playground',
    caption: 'versão beta',
    type: 'group',
    children: [
        {
            id: 'modems',
            title: 'Modems',
            type: 'item',
            url: '/modems',
            icon: icons.IconRouter,
            breadcrumbs: false
        },
        {
            id: 'sms',
            title: 'SMS',
            type: 'item',
            url: '/sms',
            icon: icons.IconDeviceMobileMessage,
            breadcrumbs: false
        }
        // {
        //     id: 'settings',
        //     title: 'Configurações',
        //     type: 'collapse',
        //     icon: icons.IconAdjustments,

        //     children: [
        //         {
        //             id: 'login3',
        //             title: 'Login',
        //             type: 'item',
        //             url: '/login',
        //             target: true
        //         },
        //         {
        //             id: 'register3',
        //             title: 'Register',
        //             type: 'item',
        //             url: '/register',
        //             target: true
        //         }
        //     ]
        // }
    ]
};

export default playground;
