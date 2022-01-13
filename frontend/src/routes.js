import React, { lazy } from 'react';
import { Redirect } from 'react-router-dom';

import DashboardLayout from "./layouts/Dashboard";

const routes = [
    {
        path: "/",
        exact: true,
        component: () => <Redirect to="/home/upload-file" />
    },
    {
        path: "/home",
        component: DashboardLayout,
        routes: [
            {
                path: "/home/upload-file",
                exact: true,
                component: lazy(() => import("./views/UploadFile/UploadFile"))
            },
            {
                path: "/home/operations",
                exact: true,
                component: lazy(() => import("./views/Operations/Operations"))
            },
        ]
    }
]

export default routes;