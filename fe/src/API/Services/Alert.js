import instance from '../axios';
import alerts from '../MockData/alerts';

const AlertAPI = {
    get: (last_alert_id, size = 30) => {
        // GET {{baseUrl}}/alerts/
        return Promise.resolve({
            data: { alerts: alerts },
        })
    },
    get_by_id: (id) => {
        // GET {{baseUrl}}/alerts/{{id}}/
        return Promise.resolve({
            data: { alert: alerts.find((alert) => alert.id == id) },
        })
    },
    mark_as_false_positive: (id) => {
        // POST {{baseUrl}}/alerts/{{id}}/label/
        // body {
        //     "is_correct": false
        // }
        // return updated alerts     
        // {
        //     "id": 1,
        //     "patient": 1002,
        //     "patient_name": "Enrique Mooney",
        //     "prediction": true,
        //     "confidence": 0.947731044815638,
        //     "model_version": "20221231_094500",
        //     "is_correct": false,
        //     "created_at": "2025-04-13T05:21:48.903244Z"
        // }}

        return Promise.resolve({
            data: { message: "Marked as false successfully" },
        })
    }
}

export default AlertAPI;