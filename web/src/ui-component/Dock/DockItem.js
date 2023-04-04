import { Grid, Typography } from '@mui/material';
import { useState, useEffect, createRef } from 'react';
import PropTypes from 'prop-types';
import DockItemState from './DockItemState';
import IconButton from '@mui/material/IconButton';
import CloseIcon from '@mui/icons-material/Close';
import { IconChevronUp, IconChevronDown } from '@tabler/icons';

const DockItem = (props) => {
    const { title, children, onClose, onChangeState, state } = props;

    const minimizedWidth = 265;

    const getWidth = (state) => {
        if (state == DockItemState.maximized) {
            return 380;
        } else {
            return minimizedWidth;
        }
    };

    const [_width, _setWidth] = useState(getWidth(state));

    const [_state, _setState] = useState(state);

    const _onChangeState = (state) => {
        _setWidth(getWidth(state));
        onChangeState(state);
    };

    const handleToggleMinimize = () => {
        if (_state == DockItemState.maximized) {
            _setState(DockItemState.minimized);
        } else {
            _setState(DockItemState.maximized);
        }
    };

    const dockContentEnd = createRef();

    const handleClose = () => {
        onClose();
    };

    useEffect(() => {
        _onChangeState(_state);
    }, [_state]);

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
        <div style={{ ...styles.item, width: _width, height: `${innerHeight}px`, order: 1 }}>
            <div style={{ float: 'left' }}>
                <div style={{ ...styles.itemContainer, width: _width - 5, position: 'relative', height: `${innerHeight}px` }}>
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
                                                                style={{
                                                                    background: '#ffffff',
                                                                    borderRadius: '6px 6px 0 0',
                                                                    borderBottom: 'solid 1px #d8d8d8'
                                                                }}
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
                                                                            <IconButton
                                                                                aria-label="close"
                                                                                size="small"
                                                                                onClick={() => {
                                                                                    handleClose();
                                                                                }}
                                                                            >
                                                                                <CloseIcon fontSize="inherit" />
                                                                            </IconButton>
                                                                        </Grid>
                                                                    </Grid>
                                                                </Grid>
                                                            </Grid>
                                                            {_state == DockItemState.maximized ? (
                                                                <div
                                                                    style={{
                                                                        maxHeight: '300px',
                                                                        minHeight: '300px',
                                                                        overflow: 'hidden',
                                                                        position: 'relative'
                                                                    }}
                                                                >
                                                                    {children}
                                                                    <div
                                                                        style={{ float: 'left', clear: 'both' }}
                                                                        ref={dockContentEnd}
                                                                    ></div>
                                                                </div>
                                                            ) : null}
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
    onChangeState: PropTypes.func.isRequired,
    onClose: PropTypes.func.isRequired
};

export default DockItem;
