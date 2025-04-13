import instance from '../axios';
import patients from '../MockData/patients';

const PatientAPI = {
    get: (page = 1, size = 30) => {
        // GET/patients/?page=202&offset=10
        return Promise.resolve({
            data: { patients: patients },
        })
    },
    get_by_id: (id) => {
        // GET {{baseUrl}}/patients/2013/
        return Promise.resolve({
            data: { patient: patients.find((patient) => patient.id == id) },
        })
    },
    delete_by_id: (id) => {
        // DELETE {{baseUrl}}/patients/2010/
        return Promise.resolve({
            data: { message: "Deleted successfully" },
        })
    },
    update_by_id: (id, data) => {
        // PATCH {{baseUrl}}/patients/2013/
        // body {patient info, only updated fields}
        return Promise.resolve({
            data: { message: "Updated successfully" },
        })
    },
    create: (data) => {
        //POST {{baseUrl}}/patients/
        // body {patient info}
        return Promise.resolve({
            data: { message: "Created successfully" },
        })
    },
}

export default PatientAPI;