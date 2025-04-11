import React from 'react';
import { createBrowserRouter } from "react-router-dom";

import AsyncRoute from './asyncRoute';
import ProtectedRoute from './protectedRoutes';

import SignIn from "../Pages/SignIn";
import Home from '../Pages/Home';
import Patient from '../Pages/Patient';

const router = createBrowserRouter([
    {
        path: '/',
        element: <AsyncRoute component={<Home />}/>
    },
    {
        path: '/signin',
        element: <ProtectedRoute authenticate={false} component={<SignIn />}/>
    },
    {
        path: '/patients',
        element: <ProtectedRoute component={<Patient />}/>
    }
]);

export default router;