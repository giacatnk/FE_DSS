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
            if (username === 'admin' && password === 'dss123') {
                localStorage.setItem('dssUserID', '123456');
                localStorage.setItem('dssUsername', 'admin');
                return {
                    user: {
                        userID: localStorage.getItem('dssUserID'),
                        username: localStorage.getItem('dssUsername')
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
            localStorage.removeItem('dssUserID');
            localStorage.removeItem('dssUsername');
        } catch (err) {
            console.error(err);
            throw err;
        }
    },

    GetCurrentUser: async () => {
        try {
            if (localStorage.getItem('dssUsername') === null) {
                throw Error("Haven't authenticated yet");
            } else return {
                user: {
                    username: localStorage.getItem('dssUsername'),
                    userID: localStorage.getItem('dssUserID')
                }
            }
        } catch (err) {
            console.error(err);
        }
    }
}

export default AuthenticationAPI;