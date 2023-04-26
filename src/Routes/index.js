import React from 'react';
import { createBrowserRouter } from "react-router-dom";

import AsyncRoute from './asyncRoute';
import ProtectedRoute from './protectedRoutes';

import SignIn from "../Pages/SignIn";
import Loan from '../Pages/Loan';
import Home from '../Pages/Home';

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
        path: '/loans',
        element: <ProtectedRoute component={<Loan />}/>
    }
]);

export default router;