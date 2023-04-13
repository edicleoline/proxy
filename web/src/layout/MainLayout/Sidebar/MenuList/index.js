import { Typography } from '@mui/material';

import NavGroup from './NavGroup';
import menuItem from 'menu-items';

const MenuList = () => {
    const navItems = menuItem.items.map((item, index) => {
        switch (item.type) {
            case 'group':
                return <NavGroup key={item.id} item={item} isLast={index >= menuItem.items.length - 1} />;
            default:
                return (
                    <Typography key={item.id} variant="h6" color="error" align="center">
                        Menu Items Error
                    </Typography>
                );
        }
    });

    return <>{navItems}</>;
};

export default MenuList;
