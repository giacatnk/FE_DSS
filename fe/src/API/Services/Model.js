import instance from '../axios';

const ModelAPI = {
    get: () => {
        return Promise.resolve({
            data: { status: "training", version: "20221231_094500" },
        })
    },
    re_train: () => {
        return Promise.resolve({
            data: { message: "Trigger re-train successfully" },
        })
    }
}

export default ModelAPI;