import instance from '../axios';

const AlertAPI = {
    get: (last_alert_id, size = 30) => {
        // GET {{baseUrl}}/alerts/?last_alert_id={{last_alert_id}}&size={{size}}
        return instance.get(`/alerts/?last_alert_id=${last_alert_id}&size=${size}`)
            .then((response) => {
                return response.data;
            })
            .catch((error) => {
                console.error('Error fetching alerts:', error);
                throw error;
            });
    },
    mark_as_false_positive: (id) => {
        // POST {{baseUrl}}/alerts/{{id}}/mark_as_false_positive/
        return instance.post(`/alerts/${id}/label/`)
            .then((response) => {
                return response.data;
            })
            .catch((error) => {
                console.error('Error marking alert as false positive:', error);
                throw error;
            });
    }
}

export default AlertAPI;