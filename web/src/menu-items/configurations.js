import { IconTypography, IconPalette, IconShadow, IconWindmill } from '@tabler/icons';
import { IconDeviceMobile, IconArrowAutofitContent, IconAdjustments } from '@tabler/icons';

const icons = {
    IconTypography,
    IconPalette,
    IconShadow,
    IconWindmill,

    IconDeviceMobile,
    IconArrowAutofitContent,
    IconAdjustments
};

const configurations = {
    id: 'settings',
    title: 'Configurações',
    type: 'group',
    children: [
        {
            id: 'settings-devices',
            title: 'Dispositivos',
            type: 'item',
            url: '/settings/devices',
            icon: icons.IconDeviceMobile,
            breadcrumbs: false
        },
        {
            id: 'settings-middleware',
            title: 'Middlewares',
            type: 'item',
            url: '/settings/middlewares',
            icon: icons.IconArrowAutofitContent,
            breadcrumbs: false
        },
        {
            id: 'settings-general',
            title: 'Ajustes gerais',
            type: 'item',
            url: '/settings',
            icon: icons.IconAdjustments,
            breadcrumbs: false
        }
        // {
        //     id: 'icons',
        //     title: 'Icons',
        //     type: 'collapse',
        //     icon: icons.IconWindmill,
        //     children: [
        //         {
        //             id: 'tabler-icons',
        //             title: 'Tabler Icons',
        //             type: 'item',
        //             url: '/icons/tabler-icons',
        //             breadcrumbs: false
        //         },
        //         {
        //             id: 'material-icons',
        //             title: 'Material Icons',
        //             type: 'item',
        //             url: '/icons/material-icons',
        //             breadcrumbs: false
        //         }
        //     ]
        // }
    ]
};

export default configurations;
