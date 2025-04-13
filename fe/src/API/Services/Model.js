import instance from '../axios';

const ModelAPI = {
    get: () => {
        return instance.get('/models/status')
            .then((response) => {
                return response.data;
            })
            .catch((error) => {
                console.error('Error fetching model:', error);
                throw error;
            });
    },
    update: () => {
        return instance.post('/models/retrain/')
            .then((response) => {
                return response;
            })
            .catch((error) => {
                console.error('Error retraining model:', error);
                throw error;
            });
    }
}

export default ModelAPI;