import { IconDeviceMobileMessage, IconRouter, IconAccessPoint, IconGitBranch, IconUsers } from '@tabler/icons';

const icons = {
    IconRouter,
    IconDeviceMobileMessage,
    IconAccessPoint,
    IconGitBranch,
    IconUsers
};

const playground = {
    id: 'configurations',
    title: 'Playground',
    caption: 'versão beta',
    type: 'group',
    children: [
        {
            id: 'playground-proxy',
            title: 'Proxy',
            type: 'collapse',
            icon: icons.IconGitBranch,
            children: [
                {
                    id: 'playground-proxy-modems',
                    title: 'Modems',
                    type: 'item',
                    icon: icons.IconRouter,
                    url: '/proxy/modems',
                    target: false
                },
                {
                    id: 'playground-proxy-users',
                    title: 'Usuários',
                    type: 'item',
                    icon: icons.IconUsers,
                    url: '/proxy/users',
                    target: false
                }
            ]
        },
        {
            id: 'sms',
            title: 'SMS',
            type: 'item',
            url: '/sms',
            icon: icons.IconDeviceMobileMessage,
            breadcrumbs: false,
            badge: '3'
        }
    ]
};

export default playground;
