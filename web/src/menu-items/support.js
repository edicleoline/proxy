import { IconLifebuoy, IconHelp, IconCode } from '@tabler/icons';

const icons = { IconLifebuoy, IconHelp, IconCode };

const support = {
    id: 'support',
    type: 'group',
    children: [
        {
            id: 'support',
            title: 'Suporte',
            type: 'item',
            url: '/support',
            icon: icons.IconLifebuoy,
            breadcrumbs: false
        },
        {
            id: 'support-documentation',
            title: 'Documentação',
            type: 'item',
            url: '/support/documentation',
            icon: icons.IconHelp,
            external: true,
            target: true
        },
        {
            id: 'support-developer',
            title: 'Desenvolvimento',
            type: 'item',
            url: '/support/dev',
            icon: icons.IconCode,
            external: true,
            target: true
        }
    ]
};

export default support;
