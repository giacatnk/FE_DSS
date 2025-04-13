import React from 'react';
import { useSelector } from 'react-redux';

const AsyncRoute = ({ component, ...rest }) => {
    const isLoggedIn = useSelector(state => state.authentication.isLoggedIn);
    if (isLoggedIn === undefined) {
        return <></>;
    } else {
        return component
    }
}

export default AsyncRoute