import React from "react";
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Drawer from '@mui/material/Drawer';
import List from '@mui/material/List';
import PropTypes from 'prop-types';
import { NavigationListItem } from '../../components';

const drawerWidth = 240;

const SideBar = props => {
    const { itemsList } = props;

    return (
        <Drawer
            variant="permanent"
            sx={{
            width: drawerWidth,
            flexShrink: 0,
            [`& .MuiDrawer-paper`]: { width: drawerWidth, boxSizing: 'border-box' },
            }}
        >
            <Toolbar />
            <Box sx={{ overflow: 'auto' }}>
            <List>
                {itemsList.map((item, index) => (
                    <NavigationListItem title={item.title} icon={item.icon} key={index} href={item.href}/>
                ))}
            </List>
            </Box>
        </Drawer>
    );
}

SideBar.propTypes = {
    pageName: PropTypes.string
};

export default SideBar