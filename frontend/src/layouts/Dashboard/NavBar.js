import * as React from 'react';
import PropTypes from 'prop-types';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';

const NavBar = props => {
    const { pageName } = props;

    return (
        <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}>
            <Toolbar>
                <Typography variant="h6" noWrap component="div">
                    {pageName}
                </Typography>
            </Toolbar>
        </AppBar>
        );
}


NavBar.propTypes = {
    pageName: PropTypes.string
};


export default NavBar