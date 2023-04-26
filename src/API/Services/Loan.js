import axios from '../axios';
const LoansAPI = {
    GetLoans: () => {
        return axios.get(`/api`);
    },
    PredictLoans: (data) => {
        return axios.post('/api', data = data);
    }
}

export default LoansAPI;