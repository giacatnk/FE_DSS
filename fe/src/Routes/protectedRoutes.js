import React from 'react';
import { Navigate } from "react-router-dom";
import { useSelector } from 'react-redux';

const ProtectedRoute = ({ redirectPath = '/', authenticate = true, component, ...rest }) => {
    const authentication = useSelector(state => state.authentication);
    if (authentication.isLoggedIn === undefined) {
        return <></>;
    } else if (authentication.isLoggedIn === authenticate) {
        return component
    } else {
        return <Navigate to={redirectPath} replace />;
    }
}

export default ProtectedRoute