import instance from '../axios';
import patients from '../MockData/patients';

const PatientAPI = {
    get: (page = 1, size = 30) => {
        return Promise.resolve({
            data: { patients: patients },
        })
    },
    get_by_id: (id) => {
        return Promise.resolve({
            data: { patient: patients.find((patient) => patient.id == id) },
        })
    },
    delete_by_id: (id) => {
        return Promise.resolve({
            data: { message: "Deleted successfully" },
        })
    },
    update_by_id: (id, data) => {
        return Promise.resolve({
            data: { message: "Updated successfully" },
        })
    },
    create: (data) => {
        return Promise.resolve({
            data: { message: "Created successfully" },
        })
    },
}

export default PatientAPI;