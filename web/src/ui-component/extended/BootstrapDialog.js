import * as React from 'react';
import PropTypes from 'prop-types';
import Button from '@mui/material/Button';
//import { styled } from '@mui/material/styles';
import Dialog from '@mui/material/Dialog';
import DialogTitle from '@mui/material/DialogTitle';
import DialogContent from '@mui/material/DialogContent';
import DialogActions from '@mui/material/DialogActions';
import IconButton from '@mui/material/IconButton';
import CloseIcon from '@mui/icons-material/Close';
import Typography from '@mui/material/Typography';
import styled from 'styled-components';

/*const BootstrapDialog = styled(Dialog)(({ theme }) => ({
    '& .MuiDialogContent-root': {
        padding: theme.spacing(2)
    },
    '& .MuiDialogActions-root': {
        padding: theme.spacing(1)
    }
}));*/

export function BootstrapDialogTitle(props) {
    const { children, onClose, ...other } = props;

    return (
        <div style={{ borderBottom: 'solid 1px #ddd' }}>
            {onClose ? (
                <IconButton
                    aria-label="close"
                    onClick={onClose}
                    sx={{
                        position: 'absolute',
                        left: 12,
                        top: 12,
                        color: (theme) => theme.palette.grey[500]
                    }}
                    size="small"
                >
                    <CloseIcon fontSize="inherit" />
                </IconButton>
            ) : null}
            <DialogTitle sx={{ m: 0, p: 2, paddingLeft: 8, paddingRight: 8, textAlign: 'center' }} {...other}>
                {children}
            </DialogTitle>
        </div>
    );
}

BootstrapDialogTitle.propTypes = {
    children: PropTypes.node,
    onClose: PropTypes.func.isRequired
};

const ActionsWrapper = styled.div`
    border-top: solid 1px #ddd;
`;

export function BootstrapDialogActions(props) {
    const { children, ...other } = props;

    return (
        <ActionsWrapper>
            <DialogActions sx={{ padding: '16px' }}>{children}</DialogActions>
        </ActionsWrapper>
    );
}

BootstrapDialogTitle.propTypes = {
    children: PropTypes.node
};
