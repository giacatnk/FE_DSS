import { createSlice } from "@reduxjs/toolkit";
import { LogIn, LogOut, GetCurrentUser } from "./authentication.action";

const initialState = {
    isLoggedIn: undefined,
    userInformation: {
        userID: "",
        username: "",
    }
}

const authenticationSlice = createSlice({
    name: 'authentication',
    initialState,
    reducers: {
    },
    extraReducers: (builder) => {
        builder.addCase(LogIn.fulfilled, (state, action) => {
            state.isLoggedIn = true;
            state.userInformation = action.payload
        })
        builder.addCase(LogIn.rejected, (state, action) => {
            state.isLoggedIn = false;
        })
        builder.addCase(LogOut.fulfilled, (state, action) => {
            state = initialState;
            state.isLoggedIn = false;
        });
        builder.addCase(GetCurrentUser.fulfilled, (state, action) => {
            const user = action.payload;
            state.isLoggedIn = true;
            state.userInformation = {
                userID: user.userID,
                username: user.username,
            }
        });
        builder.addCase(GetCurrentUser.rejected, (state, action) => {
            state.isLoggedIn = false;
        });
    }
})

export default authenticationSlice.reducer