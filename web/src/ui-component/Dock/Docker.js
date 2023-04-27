import { useState, useEffect, useRef } from 'react';
import PropTypes from 'prop-types';
import { Dock } from 'ui-component/Dock';
import { useDispatch, useSelector } from 'react-redux';
import { store } from 'store';
import { ADD_DOCK, REMOVE_DOCK, UPDATE_DOCK_STATE } from 'store/actions/types';
import { default as _addDock } from 'store/actions/addDock';
import updateDockState from 'store/actions/updateDockState';
import ModemLog from 'ui-component/ModemLog';
import { Grid } from '@mui/material';
import IconButton from '@mui/material/IconButton';
import { IconDotsVertical } from '@tabler/icons';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import { modemLog, bulkStoreModemLog } from 'storage/modem/log';
import { logs } from 'services/api/modem/log';

export const addDock = (id, type, state, data) => {
    const dock = store.getState().docker.docks.find((item) => item.dock.id === id);
    if (!dock) {
        store.dispatch(
            _addDock({
                type: ADD_DOCK,
                dock: {
                    id: id,
                    type: type,
                    state: state,
                    data: data
                }
            })
        );
    } else {
        store.dispatch(updateDockState(id, state));
    }
};

export const DOCK_TYPE = {
    MODEM_LOG: 'MODEM_LOG'
};

export const DockModemLogToolbar = ({ modem }) => {
    const [anchorModemMenuEl, setAnchorModemMenuEl] = useState(null);
    const [openModemMenuElem, setOpenModemMenuElem] = useState(null);
    const handleModemOpenMenuClick = (elem) => (event) => {
        setAnchorModemMenuEl(event.currentTarget);
        setOpenModemMenuElem(elem);
    };
    const handleModemCloseMenu = () => {
        setAnchorModemMenuEl(null);
        setOpenModemMenuElem(null);
    };

    const removeLogs = () => {
        console.log('remove logs', modem);
        modemLog.where('modem_id').anyOf(modem.id).delete();
    };

    const loadFromApi = () => {
        logs(modem.id, 0, 200, 'next', 'desc')
            .then(
                (response) => {
                    console.log(response);
                    bulkStoreModemLog(response);
                },
                (err) => {
                    const message =
                        err.response && err.response.data && err.response.data.error && err.response.data.error.message
                            ? err.response.data.error.message
                            : err.message;
                    console.log(message);
                }
            )
            .finally(() => {
                //console.log();
            });
    };

    return (
        <Grid item>
            <IconButton
                id={`modem-log-${modem.id}-menu-button`}
                aria-label="close"
                size="small"
                onClick={handleModemOpenMenuClick(modem.id)}
            >
                <IconDotsVertical size="18" />
            </IconButton>
            <Menu
                id={`modem-log-${modem.id}-menu`}
                anchorEl={anchorModemMenuEl}
                open={openModemMenuElem === modem.id}
                onClose={handleModemCloseMenu}
                MenuListProps={{
                    'aria-labelledby': `modem-log-${modem.id}-menu-button`
                }}
            >
                <MenuItem
                    onClick={() => {
                        removeLogs();
                        handleModemCloseMenu();
                    }}
                >
                    Deletar logs
                </MenuItem>
                <MenuItem
                    onClick={() => {
                        loadFromApi();
                        handleModemCloseMenu();
                    }}
                >
                    Recuperar logs do servidor
                </MenuItem>
            </Menu>
        </Grid>
    );
};

export const Docker = () => {
    const _docks = useSelector((state) => state.docker.docks);
    const dispatch = useDispatch();

    const _dockItems = useRef([]);
    const [dockItems, setDockItems] = useState([]);

    const title = (type, data) => {
        if (type === DOCK_TYPE.MODEM_LOG) {
            return `Log modem ${data.id}`;
        }
    };

    const content = (type, data) => {
        if (type === DOCK_TYPE.MODEM_LOG) {
            return <ModemLog modem={data} />;
        }
    };

    const toolbarChildren = (type, data) => {
        if (type === DOCK_TYPE.MODEM_LOG) {
            return <DockModemLogToolbar modem={data} />;
        }
    };

    useEffect(() => {
        _dockItems.current = _docks.map((item) => {
            return {
                id: item.dock.id,
                title: title(item.dock.type, item.dock.data),
                state: item.dock.state,
                content: content(item.dock.type, item.dock.data),
                toolbarChildren: toolbarChildren(item.dock.type, item.dock.data),
                onChangeState: (id, state) => {
                    dispatch({ type: UPDATE_DOCK_STATE, id: id, state: state });
                }
            };
        });
        setDockItems(_dockItems.current);
    }, [_docks]);

    const handleCloseDock = (item) => {
        const dock = _dockItems.current.find((i) => i.id === item.id);
        dispatch({ type: REMOVE_DOCK, id: dock.id });
    };

    return <Dock items={dockItems} onClose={handleCloseDock} />;
};
