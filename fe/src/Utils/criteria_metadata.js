const criteria_metadata = [
    { name: "gender", label: "Gender" },
    { name: "age", label: "Age" },
    { name: "weight", label: "Weight" },
    { name: "platelets", label: "Platelets" },
    { name: "spo2", label: "SpO2" },
    { name: "creatinine", label: "Creatinine" },
    { name: "hematocrit", label: "Hematocrit" },
    { name: "aids", label: "AIDS", type: "boolean" },
    { name: "lymphoma", label: "Lymphoma", type: "boolean" },
    { name: "solid_tumor_with_metastasis", label: "Solid Tumor with Metastasis", type: "boolean" },
    { name: "heartrate", label: "Heart rate" },
    { name: "calcium", label: "Calcium" },
    { name: "wbc", label: "WBC" },
    { name: "glucose", label: "Glucose" },
    { name: "inr", label: "INR" },
    { name: "potassium", label: "Potassium" },
    { name: "sodium", label: "Sodium" },
    { name: "ethnicity", label: "Ethnicity", type: "enum", values: {"1": "White", "2": "Black", "3": "Asian", "4": "Latino", "5": "Others"} },
]

export default criteria_metadata;
