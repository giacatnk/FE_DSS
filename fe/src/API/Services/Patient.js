import instance from '../axios';

const PatientAPI = {
    get: (page = 1, size = 30) => {
        return instance.get(`/patients/?page=${page}&size=${size}`)
            .then((response) => {
                return response.data;
            })
            .catch((error) => {
                console.error('Error fetching patients:', error);
                throw error;
            });
    },
    get_by_id: (id) => {
        return instance.get(`/patients/${id}/`)
            .then((response) => {
                return response.data;
            })
            .catch((error) => {
                console.error('Error fetching patient by ID:', error);
                throw error;
            });
    },
    delete_by_id: (id) => {
        return instance.delete(`/patients/${id}/`)
            .then((response) => {
                return response.data;
            })
            .catch((error) => {
                console.error('Error deleting patient:', error);
                throw error;
            });
    },
    update_by_id: (id, data) => {
        return instance.put(`/patients/${id}/`, data)
            .then((response) => {
                return response.data;
            })
            .catch((error) => {
                console.error('Error updating patient:', error);
                throw error;
            });
    },
    create: (data) => {
        return instance.post('/patients/', data)
            .then((response) => {
                return response.data;
            })
            .catch((error) => {
                console.error('Error creating patient:', error);
                throw error;
            });
    },
    sync: () => {
        return instance.get('/patients/sync/')
            .then((response) => {
                return response.data;
            })
            .catch((error) => {
                console.error('Error syncing patients:', error);
                throw error;
            });
    }
}
export default PatientAPI;