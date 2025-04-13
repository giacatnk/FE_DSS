import instance from '../axios';
import alerts from '../MockData/alerts';

const AlertAPI = {
    get: (last_alert_id, size = 30) => {
        return Promise.resolve({
            data: { alerts: alerts },
        })
    },
    mark_as_false: (id) => {
        return Promise.resolve({
            data: { message: "Marked as false successfully" },
        })
    }
}

export default AlertAPI;