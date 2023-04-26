import { createAsyncThunk } from "@reduxjs/toolkit";
import AuthenticationAPI from '../../API/auth';

const LogIn = createAsyncThunk(
    'authentication/login',
    async ({ username, password }, thunkAPI) =>  {
        const data = await AuthenticationAPI.Login(username, password);
        return data.user;
    }
)

const LogOut = createAsyncThunk(
    'authentication/logout',
    async (thunkAPI) => {
        const result = await AuthenticationAPI.Logout();
        window.location.reload();
        return result;
    }
)

const GetCurrentUser = createAsyncThunk(
    'session/get-current-user',
    async (thunkAPI) => {
        const data = await AuthenticationAPI.GetCurrentUser();
        return data.user;
    }
)

export {
    LogIn,
    LogOut,
    GetCurrentUser,
}