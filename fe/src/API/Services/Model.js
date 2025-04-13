import instance from '../axios';

const ModelAPI = {
    get: () => {
        // GET {{baseUrl}}/models/status
        // return 
        // {
        //     "status": "completed",
        //     "last_training_time": "2025-04-13T07:24:33.277644",
        //     "error": null,
        //     "metrics": {
        //       "accuracy": 0.808176589460594,
        //       "precision": 0.78591976540382,
        //       "recall": 0.808176589460594,
        //       "f1_score": 0.789265389471883,
        //       "confusion_matrix": [
        //         [4726, 347],
        //         [887, 473]
        //       ]
        //     }
        //   }
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
        // GET {{baseUrl}}/models/retrain/
        // return 
        // {
        //     "status": "success",
        //     "message": "Model retraining started in background"
        // }
        return Promise.resolve({
            data: { message: "Trigger re-train successfully" },
        })
    }
}

export default ModelAPI;