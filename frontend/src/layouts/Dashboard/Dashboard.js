import React, { Suspense } from 'react';
import { renderRoutes } from 'react-router-config';
import { LinearProgress } from '@material-ui/core';
import Box from '@mui/material/Box';
import CssBaseline from '@mui/material/CssBaseline';
import Toolbar from '@mui/material/Toolbar';
import PropTypes from 'prop-types';
import NavBar from './NavBar';
import SideBar from './SideBar';
import { RoutesTitle, RoutesNavigation } from './NavigationConfig';

const Dashboard = props => {
    const { route, location } = props;
    const title = RoutesTitle[location.pathname].title;

    return (
        <Box sx={{ display: 'flex' }}>
            <CssBaseline />
            <NavBar pageName={title}></NavBar>
            <SideBar itemsList={RoutesNavigation}></SideBar>
            <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
                <Toolbar />
                <Suspense fallback={<LinearProgress />}>
                    {renderRoutes(route.routes)}
                </Suspense>
            </Box>
        </Box>
    )
}

Dashboard.propTypes = {
    route: PropTypes.object,
    location: PropTypes.object
}

export default Dashboard;