import { configureStore } from "@reduxjs/toolkit";
import authenticationReducer from './authentication/authentication.slice';

export const store = configureStore({
    reducer: {
        authentication: authenticationReducer,
    },
})