import instance from '../axios';

const ModelAPI = {
    get: () => {
        return Promise.resolve({
            data: { 
                model: {
                    "status": "completed",
                    "last_training_time": "2025-04-13T06:12:59.633261",
                    "error": null,
                    "metrics": {
                        "accuracy": 0.8081765894605938,
                        "precision": 0.7859197654038198,
                        "recall": 0.8081765894605938,
                        "f1_score": 0.7892653894718832,
                        "confusion_matrix": [
                            [
                                4726,
                                347
                            ],
                            [
                                887,
                                473
                            ]
                        ]
                    }
                }
            },
        })
    },
    re_train: () => {
        return Promise.resolve({
            data: { message: "Trigger re-train successfully" },
        })
    }
}

export default ModelAPI;