import axios from 'axios';

const instance = axios.create({
    baseURL: `/api`
})

instance.defaults.headers.common['Content-Type'] = 'application/json';

export default instance;