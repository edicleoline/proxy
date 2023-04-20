import * as React from 'react';
import { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { store } from 'store';
import { Outlet } from 'react-router-dom';

// material-ui
import { styled, useTheme } from '@mui/material/styles';
import { AppBar, Box, CssBaseline, Toolbar, useMediaQuery } from '@mui/material';

// project imports
import Breadcrumbs from 'ui-component/extended/Breadcrumbs';
import Header from './Header';
import Sidebar from './Sidebar';
import Customization from '../Customization';
import navigation from 'menu-items';
import { drawerWidth } from 'store/constant';
import { SET_MENU, REMOVE_NOTIFICATION } from 'store/actions/types';

// assets
import { IconChevronRight } from '@tabler/icons';

import Snackbar from '@mui/material/Snackbar';
import Button from '@mui/material/IconButton';
import MuiAlert from '@mui/material/Alert';

import { Docker } from 'ui-component/Dock/Docker';

// styles
const Main = styled('main', { shouldForwardProp: (prop) => prop !== 'open' })(({ theme, open }) => ({
    ...theme.typography.mainContent,
    ...(!open && {
        borderBottomLeftRadius: 0,
        borderBottomRightRadius: 0,
        transition: theme.transitions.create('margin', {
            easing: theme.transitions.easing.sharp,
            duration: theme.transitions.duration.leavingScreen
        }),
        [theme.breakpoints.up('md')]: {
            marginLeft: -(drawerWidth - 20),
            width: `calc(100% - ${drawerWidth}px)`
        },
        [theme.breakpoints.down('md')]: {
            marginLeft: '20px',
            width: `calc(100% - ${drawerWidth}px)`,
            padding: '16px'
        },
        [theme.breakpoints.down('sm')]: {
            marginLeft: '10px',
            width: `calc(100% - ${drawerWidth}px)`,
            padding: '16px',
            marginRight: '10px'
        }
    }),
    ...(open && {
        transition: theme.transitions.create('margin', {
            easing: theme.transitions.easing.easeOut,
            duration: theme.transitions.duration.enteringScreen
        }),
        marginLeft: 0,
        borderBottomLeftRadius: 0,
        borderBottomRightRadius: 0,
        width: `calc(100% - ${drawerWidth}px)`,
        [theme.breakpoints.down('md')]: {
            marginLeft: '20px'
        },
        [theme.breakpoints.down('sm')]: {
            marginLeft: '10px'
        }
    })
}));

// ==============================|| MAIN LAYOUT ||============================== //
const Alert = React.forwardRef(function Alert(props, ref) {
    return <MuiAlert elevation={6} ref={ref} variant="filled" {...props} />;
});

const Notification = (props) => {
    const { notification } = props;
    const dispatch = useDispatch();

    const handleCloseNotification = () => {
        dispatch({ type: REMOVE_NOTIFICATION, notification: notification });
    };

    return (
        <Snackbar
            key={notification.id}
            anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
            open={notification.props.open}
            autoHideDuration={notification.props.autoHideDuration}
            onClose={() => {
                handleCloseNotification();
            }}
            message={notification.message}
            action={
                <Button aria-label="close" size="small" color="inherit" onClick={handleCloseNotification} sx={{ fontSize: '0.875rem' }}>
                    Fechar
                </Button>
            }
        >
            {notification.props.alert === true ? (
                <Alert onClose={handleCloseNotification} severity={notification.props.severity} sx={{ width: '100%' }}>
                    {notification?.message}
                </Alert>
            ) : null}
        </Snackbar>
    );
};

const MainLayout = () => {
    const theme = useTheme();
    const matchDownMd = useMediaQuery(theme.breakpoints.down('md'));
    // Handle left drawer
    const leftDrawerOpened = useSelector((state) => state.customization.opened);
    const dispatch = useDispatch();
    const handleLeftDrawerToggle = () => {
        dispatch({ type: SET_MENU, opened: !leftDrawerOpened });
    };

    const [notifications, setNotifications] = useState([]);
    const _notifications = useSelector((state) => state.notifications);
    useEffect(() => {
        console.log(_notifications);
        setNotifications(_notifications.items);
    }, [_notifications]);

    return (
        <Box sx={{ display: 'flex' }}>
            <CssBaseline />
            {/* header */}
            <AppBar
                enableColorOnDark
                position="fixed"
                color="inherit"
                elevation={0}
                sx={{
                    bgcolor: theme.palette.background.default,
                    transition: leftDrawerOpened ? theme.transitions.create('width') : 'none'
                }}
            >
                <Toolbar>
                    <Header handleLeftDrawerToggle={handleLeftDrawerToggle} />
                </Toolbar>
            </AppBar>

            {/* drawer */}
            <Sidebar drawerOpen={!matchDownMd ? leftDrawerOpened : !leftDrawerOpened} drawerToggle={handleLeftDrawerToggle} />

            {/* main content */}
            <Main theme={theme} open={leftDrawerOpened}>
                {/* breadcrumb */}
                {/* <Breadcrumbs separator={IconChevronRight} navigation={navigation} icon title rightAlign /> */}
                <Outlet />
            </Main>
            {notifications.map((notification, index) => (
                <Notification key={index} notification={notification} />
            ))}
            <Docker />
        </Box>
    );
};

export default MainLayout;
