import { Grid, Box, Card, Typography } from '@mui/material';
import Button from '@mui/material/Button';

import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import TextField from '@mui/material/TextField';
import Stack from '@mui/material/Stack';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import Switch from '@mui/material/Switch';
import FormControlLabel from '@mui/material/FormControlLabel';
import FormGroup from '@mui/material/FormGroup';
import InputAdornment from '@mui/material/InputAdornment';
import FormHelperText from '@mui/material/FormHelperText';
import Visibility from '@mui/icons-material/Visibility';
import VisibilityOff from '@mui/icons-material/VisibilityOff';
import OutlinedInput from '@mui/material/OutlinedInput';
import Divider from '@mui/material/Divider';
import IconButton from '@mui/material/IconButton';
import CloseIcon from '@mui/icons-material/Close';
import { IconChevronUp, IconChevronDown } from '@tabler/icons';

import { useState, useEffect, useRef } from 'react';
import PropTypes from 'prop-types';
import { BootstrapDialogTitle } from 'ui-component/extended/BootstrapDialog';

import Log from 'ui-component/ModemLog';

export const Dockmodal = (props) => {
    const { open, onClose, ...other } = props;

    return (
        <>
            <Grid
                container
                justifyContent="flex-start"
                alignItems="start"
                direction="row"
                sx={{ p: 0.2, px: 0.8, borderRadius: 1, minWidth: '160px' }}
            >
                <Grid item>test</Grid>
            </Grid>
        </>
    );
};

Dockmodal.propTypes = {
    // onClose: PropTypes.func.isRequired,
    // onConfirm: PropTypes.func.isRequired
};

export const DockItemState = {
    minimized: 'minimized',
    maximized: 'maximized'
};

export const DockItem = (props) => {
    const { title, children, open, onClose, onToggleMinimize, state, ...other } = props;

    const minimizedWidth = 265;
    let _width = useRef(minimizedWidth);

    let __state = state;
    const [_state, _setState] = useState(__state);

    const handleToggleMinimize = () => {
        if (_state == DockItemState.maximized) {
            __state = DockItemState.minimized;
            _width.current = minimizedWidth;
        } else {
            __state = DockItemState.maximized;
            _width.current = 380;
        }
        _setState(__state);
    };

    // useEffect(() => {
    //     onToggleMinimize(__state);
    // }, [_state]);

    useEffect(() => {
        console.log('loaded dockitem');
    });

    const styles = {
        item: {
            minHeight: '1px',
            float: 'left'
        },
        itemContainer: {
            minHeight: '1px',
            float: 'left'
        },
        itemWrapper: {
            width: '100%',
            bottom: 0
        },
        dialog: {
            visibility: 'visible',
            boxShadow: '0px 8px 10px 1px rgb(0 0 0 / 14%), 0px 3px 14px 2px rgb(0 0 0 / 12%), 0px 5px 5px -3px rgb(0 0 0 / 20%)',
            borderRadius: '8px 8px 0 0'
        }
    };

    return (
        <div style={{ ...styles.item, width: _width.current, height: `${innerHeight}px`, order: 1 }}>
            <div style={{ float: 'left' }}>
                <div style={{ ...styles.itemContainer, width: _width.current - 5, position: 'relative', height: `${innerHeight}px` }}>
                    <div style={{ ...styles.itemWrapper, position: 'absolute' }}>
                        <div>
                            <div role="dialog" style={styles.dialog}>
                                <div>
                                    <div>
                                        <div
                                            style={{
                                                width: '100%',
                                                borderRadius: '8px 8px 0 0',
                                                float: 'none',
                                                background: '#f2f6fc'
                                            }}
                                        >
                                            <div
                                                style={{
                                                    background: 'none'
                                                }}
                                            >
                                                <div
                                                    style={{
                                                        position: 'relative',
                                                        borderRadius: '8px 0 0 0'
                                                    }}
                                                >
                                                    <div>
                                                        <div>
                                                            <Grid
                                                                container
                                                                justifyContent="space-between"
                                                                alignItems="center"
                                                                direction="row"
                                                                sx={{ padding: '6px 8px 6px 12px' }}
                                                            >
                                                                <Grid item sx={{ flex: 1 }}>
                                                                    <Typography variant="h5" component="span" sx={{ fontWeight: '500' }}>
                                                                        {title}
                                                                    </Typography>
                                                                </Grid>
                                                                <Grid item>
                                                                    <Grid
                                                                        container
                                                                        justifyContent="space-between"
                                                                        alignItems="start"
                                                                        direction="row"
                                                                    >
                                                                        <Grid item>
                                                                            <IconButton
                                                                                aria-label="maximize"
                                                                                size="small"
                                                                                onClick={() => {
                                                                                    handleToggleMinimize();
                                                                                }}
                                                                            >
                                                                                {_state == DockItemState.maximized ? (
                                                                                    <IconChevronDown size={18} />
                                                                                ) : (
                                                                                    <IconChevronUp size={18} />
                                                                                )}
                                                                            </IconButton>
                                                                        </Grid>
                                                                        <Grid item>
                                                                            <IconButton aria-label="close" size="small">
                                                                                <CloseIcon fontSize="inherit" />
                                                                            </IconButton>
                                                                        </Grid>
                                                                    </Grid>
                                                                </Grid>
                                                            </Grid>
                                                            {_state == DockItemState.maximized ? <div>{children}</div> : null}
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

DockItem.propTypes = {
    title: PropTypes.string.isRequired,
    onToggleMinimize: PropTypes.func.isRequired
    // onConfirm: PropTypes.func.isRequired
};

export const Dock = (props) => {
    const { open, onClose, items, ...other } = props;

    const styles = {
        container: {
            visibility: 'hidden',
            position: 'absolute',
            left: 0,
            top: 0,
            width: '100%',
            height: '100%',
            overflow: 'hidden',
            zIndex: 9999
        }
    };

    const [innerHeight, setInnerHeight] = useState(0);
    const _resize = () => {
        const ih = window.innerHeight;
        setInnerHeight(ih);
        console.log(ih);
    };
    useEffect(() => {
        _resize();

        window.addEventListener('resize', _resize);

        return () => {
            window.removeEventListener('resize', _resize);
        };
    }, []);

    // const _items = [
    //     {
    //         id: 1,
    //         title: 'Log modem 1',
    //         content: <Log>content log modem 1</Log>,
    //         state: dockItemStates.minimized
    //     },
    //     {
    //         id: 2,
    //         title: 'Log modem 2',
    //         content: <Log>content log modem 2</Log>,
    //         state: dockItemStates.minimized
    //     }
    // ];

    // const items = useRef(_items);

    return (
        <div style={styles.container}>
            <div>
                <div style={{ width: '1872px' }}>
                    <div style={{ height: `${innerHeight}px` }}>
                        <div style={{ float: 'right' }}>
                            <div style={styles.item}></div>
                            {items
                                ? items.map((item) => (
                                      <DockItem
                                          key={item.id}
                                          title={item.title}
                                          state={item.state}
                                          onToggleMinimize={() => {
                                              console.log('toggle event');
                                          }}
                                      >
                                          {item.content}
                                      </DockItem>
                                  ))
                                : null}
                            <div style={styles.item}></div>
                            <div style={styles.item}></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

Dock.propTypes = {
    // onClose: PropTypes.func.isRequired,
    // onConfirm: PropTypes.func.isRequired
};
