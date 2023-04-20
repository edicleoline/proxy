import { lazy } from 'react';

import MainLayout from 'layout/MainLayout';
import Loadable from 'ui-component/Loadable';

const DashboardDefault = Loadable(lazy(() => import('views/dashboard/Default')));

const Modems = Loadable(lazy(() => import('views/modems')));
const ProxyUsers = Loadable(lazy(() => import('views/proxy/users')));

const Sms = Loadable(lazy(() => import('views/sms')));

const Devices = Loadable(lazy(() => import('views/settings/devices')));
const Middlewares = Loadable(lazy(() => import('views/settings/middlewares')));
const GeneralSettings = Loadable(lazy(() => import('views/settings/general')));

const UtilsColor = Loadable(lazy(() => import('views/utilities/Color')));
const UtilsShadow = Loadable(lazy(() => import('views/utilities/Shadow')));
const UtilsMaterialIcons = Loadable(lazy(() => import('views/utilities/MaterialIcons')));
const UtilsTablerIcons = Loadable(lazy(() => import('views/utilities/TablerIcons')));

// ==============================|| MAIN ROUTING ||============================== //

const MainRoutes = {
    path: '/',
    element: <MainLayout />,
    children: [
        {
            path: '/',
            element: <DashboardDefault />
        },
        {
            path: 'dashboard',
            children: [
                {
                    path: 'default',
                    element: <DashboardDefault />
                }
            ]
        },
        {
            path: 'proxy',
            children: [
                {
                    path: 'modems',
                    element: <Modems />
                }
            ]
        },
        {
            path: 'proxy',
            children: [
                {
                    path: 'users',
                    element: <ProxyUsers />
                }
            ]
        },
        {
            path: '/',
            children: [
                {
                    path: 'sms',
                    element: <Sms />
                }
            ]
        },
        {
            path: '/',
            children: [
                {
                    path: 'settings',
                    element: <GeneralSettings />
                }
            ]
        },
        {
            path: 'settings',
            children: [
                {
                    path: 'modems',
                    element: <Modems />
                }
            ]
        },
        {
            path: 'settings',
            children: [
                {
                    path: 'devices',
                    element: <Devices />
                }
            ]
        },
        {
            path: 'settings',
            children: [
                {
                    path: 'middlewares',
                    element: <Middlewares />
                }
            ]
        },
        {
            path: 'icons',
            children: [
                {
                    path: 'tabler-icons',
                    element: <UtilsTablerIcons />
                }
            ]
        },
        {
            path: 'icons',
            children: [
                {
                    path: 'material-icons',
                    element: <UtilsMaterialIcons />
                }
            ]
        }
    ]
};

export default MainRoutes;
