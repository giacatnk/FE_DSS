import { message } from 'antd';

function sleep(milliseconds) {
    const date = Date.now();
    let currentDate = null;
    do {
      currentDate = Date.now();
    } while (currentDate - date < milliseconds);
}

const AuthenticationAPI = {
    Login: async (username, password) => {
        try {
            sleep(1000);
            if (username === 'admin' && password === 'aceso123') {
                localStorage.setItem('userID', '123456');
                localStorage.setItem('username', 'admin');
                return {
                    user: {
                        userID: localStorage.getItem('userID'),
                        username: localStorage.getItem('username')
                    }
                }
            } else {
                throw Error('Invalid credentials');
            }
        } catch (err) {
            console.error(err);
            message.error(err.message)
            throw err;
        }
    },

    Logout: async () => {
        try {
            localStorage.removeItem('userID');
            localStorage.removeItem('username');
        } catch (err) {
            console.error(err);
            throw err;
        }
    },

    GetCurrentUser: async () => {
        try {
            if (localStorage.getItem('username') === null) {
                throw Error("Haven't authenticated yet");
            } else return {
                user: {
                    username: localStorage.getItem('username'),
                    userID: localStorage.getItem('userID')
                }
            }
        } catch (err) {
            console.error(err);
        }
    }
}

export default AuthenticationAPI;