import React from 'react';
import { createBrowserRouter } from "react-router-dom";

import AsyncRoute from './asyncRoute';
import ProtectedRoute from './protectedRoutes';

import SignIn from "../Pages/SignIn";
import Home from '../Pages/Home';
import Patient from '../Pages/Patient';
import EditPatient from '../Pages/Patient/ChildPages/Edit';
import AlertHistory from '../Pages/Alert';

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
    },
    {
        path: '/patients/:id',
        element: <ProtectedRoute component={<EditPatient />}/>
    },
    {
        path: '/alerts',
        element: <ProtectedRoute component={<AlertHistory />}/>
    }
]);

export default router;