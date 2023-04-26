import axios from 'axios';
import { API_URL } from '../Configs';

const instance = axios.create({
    baseURL: `/api`
})

instance.defaults.headers.common['Content-Type'] = 'application/json';

export default instance;