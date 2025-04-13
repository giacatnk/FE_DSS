import instance from '../axios';
import patients from '../MockData/data';

const PatientAPI = {
    get: (page = 1, size = 30) => {
        return Promise.resolve({
            data: { patients: patients },
        })
        // return instance.get(
        //     `/v1/patients`,
        //     {
        //         params: {
        //             page: page,
        //             size: size
        //         }
        //     }
        // );
    },
    get_by_id: (id) => {
        return Promise.resolve({
            data: { patient: patients.find((patient) => patient.id === id) },
        })
        // return instance.get(
        //     `/v1/patients/${id}`,
        // );
    },
    delete_by_id: (id) => {
        return Promise.resolve({
            data: { message: "Deleted successfully" },
        })
        // return instance.delete(
        //     `/v1/patients/${id}`,
        // );
    },
    update_by_id: (id, data) => {
        return Promise.resolve({
            data: { message: "Updated successfully" },
        })
        // return instance.put(
        //     `/v1/patients/${id}`,
        //     data
        // );
    },
    create: (data) => {
        return Promise.resolve({
            data: { message: "Created successfully" },
        })
        // return instance.post(
        //     `/v1/patients`,
        //     data
        // );
    },
}

export default PatientAPI;