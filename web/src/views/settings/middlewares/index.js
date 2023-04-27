import { Grid } from '@mui/material';
import MainCard from 'ui-component/cards/MainCard';
import SubCard from 'ui-component/cards/SubCard';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import { useState, useEffect, useRef } from 'react';
import PropTypes from 'prop-types';
import * as React from 'react';
import { getMiddlewares } from 'services/api/middleware';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import Divider from '@mui/material/Divider';
import IconButton from '@mui/material/IconButton';
import { IconDotsVertical } from '@tabler/icons';
import { FormattedMessage } from 'react-intl';

const Middlewares = () => {
    const [tableMaxHeight, setTableMaxHeight] = useState(null);
    const _resizeTable = () => {
        const mainElHeight = window.innerHeight;
        const max = mainElHeight - 205;
        setTableMaxHeight(max);
    };

    useEffect(() => {
        _resizeTable();

        window.addEventListener('resize', _resizeTable);

        return () => {
            window.removeEventListener('resize', _resizeTable);
        };
    }, []);

    const [loading, setLoading] = useState(false);
    const [middlewares, setMiddlewares] = useState([]);

    const loadMiddlewares = () => {
        setLoading(true);
        getMiddlewares()
            .then(
                (response) => {
                    if (response.items) {
                        setMiddlewares(response.items);
                    }
                },
                (err) => {
                    console.log('settings/Middleware', err);
                }
            )
            .finally(() => {
                setLoading(false);
            });
    };

    useEffect(() => {
        loadMiddlewares();
    }, []);

    const [anchorMiddlewareMenuEl, setAnchorMiddlewareMenuEl] = useState(null);
    const [openMiddlewareMenuElem, setOpenMiddlewareMenuElem] = useState(null);
    const handleMiddlewareOpenMenuClick = (elem) => (event) => {
        setAnchorMiddlewareMenuEl(event.currentTarget);
        setOpenMiddlewareMenuElem(elem);
    };
    const handleMiddlewareCloseMenu = () => {
        setAnchorMiddlewareMenuEl(null);
        setOpenMiddlewareMenuElem(null);
    };

    return (
        <MainCard title="Middlewares" contentSX={{ padding: '0 !important' }}>
            <Grid container spacing={0}>
                <Grid item xs={12} sm={12}>
                    <SubCard contentSX={{ padding: '0 !important' }} sx={{ border: 'none 0', borderRadius: '0' }}>
                        <Grid container direction="column" spacing={0}>
                            <Grid item sx={{ maxWidth: '100% !important' }}>
                                <TableContainer component={Paper} sx={{ borderRadius: '0', maxHeight: tableMaxHeight }}>
                                    <Table stickyHeader sx={{ minWidth: 650 }} aria-label="Middlewares table">
                                        <TableHead>
                                            <TableRow>
                                                <TableCell>Middleware</TableCell>
                                                <TableCell align="left">Nome</TableCell>
                                                <TableCell align="left">Versão</TableCell>
                                                <TableCell align="left">Descrição</TableCell>
                                            </TableRow>
                                        </TableHead>
                                        <TableBody>
                                            {middlewares.map((middleware) => (
                                                <TableRow
                                                    hover
                                                    key={middleware.id}
                                                    sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                                                >
                                                    <TableCell component="th" scope="row" sx={{ minWidth: '100px', position: 'relative' }}>
                                                        <Grid container justifyContent="flex-start" alignItems="center" direction="row">
                                                            <Grid item>
                                                                <IconButton
                                                                    id={`middleware-button-${middleware.id}`}
                                                                    aria-label="Middleware Options"
                                                                    size="small"
                                                                    aria-controls={`middleware-menu-${middleware.id}`}
                                                                    aria-haspopup="true"
                                                                    onClick={handleMiddlewareOpenMenuClick(middleware.id)}
                                                                >
                                                                    <IconDotsVertical />
                                                                </IconButton>
                                                            </Grid>
                                                            <Grid item>{middleware.id}</Grid>
                                                        </Grid>
                                                        <Menu
                                                            id={`middleware-menu-${middleware.id}`}
                                                            anchorEl={anchorMiddlewareMenuEl}
                                                            open={openMiddlewareMenuElem === middleware.id}
                                                            onClose={handleMiddlewareCloseMenu}
                                                            MenuListProps={{
                                                                'aria-labelledby': `middleware-button-${middleware.id}`
                                                            }}
                                                        >
                                                            <MenuItem>Verificar atualização</MenuItem>
                                                        </Menu>
                                                    </TableCell>
                                                    <TableCell align="left">{middleware.name}</TableCell>
                                                    <TableCell align="left">1.0.0</TableCell>
                                                    <TableCell align="left">
                                                        <span style={{ whiteSpace: 'pre-wrap' }}>
                                                            <FormattedMessage
                                                                id={middleware.description}
                                                                values={{ name: middleware.name }}
                                                            />
                                                        </span>
                                                    </TableCell>
                                                </TableRow>
                                            ))}
                                        </TableBody>
                                    </Table>
                                </TableContainer>
                            </Grid>
                        </Grid>
                    </SubCard>
                </Grid>
            </Grid>
        </MainCard>
    );
};

export default Middlewares;
