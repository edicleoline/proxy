import * as React from 'react';
import Button from '@mui/material/Button';
import ButtonGroup from '@mui/material/ButtonGroup';
import ArrowDropDownIcon from '@mui/icons-material/ArrowDropDown';
import ClickAwayListener from '@mui/material/ClickAwayListener';
import Grow from '@mui/material/Grow';
import Paper from '@mui/material/Paper';
import Popper from '@mui/material/Popper';
import MenuItem from '@mui/material/MenuItem';
import MenuList from '@mui/material/MenuList';

const options = ['Create a merge commit', 'Squash and merge', 'Rebase and merge'];

const ProxyUsersActions = () => {
    const handleClick = () => {
        console.log('add');
    };

    return (
        <Button variant="contained" onClick={handleClick}>
            Adicionar usuário
        </Button>
    );
};

export default ProxyUsersActions;
