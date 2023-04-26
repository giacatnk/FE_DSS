import React from 'react';
import { useSelector } from 'react-redux';
import { Navigate } from 'react-router-dom';

const Home = (props) => {
    const isLoggedIn = useSelector(state => state.authentication.isLoggedIn);

    if (isLoggedIn === undefined) {
        return <> </>
    } else if (isLoggedIn === false) {
        return <Navigate to='/signin' />
    } else {
        return <Navigate to='/loans' />
    }
}

export default Home;