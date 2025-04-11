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
}

export default PatientAPI;