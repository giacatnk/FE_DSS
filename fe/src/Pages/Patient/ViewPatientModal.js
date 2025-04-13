import React from 'react';
import { Button, Descriptions, Modal } from 'antd';
import PatientAPI from '../../API/Services/Patient';
import criteria_metadata from '../../Utils/criteria_metadata';

const ViewPatientModal = (props) => {
  const [open, setOpen] = React.useState(false);
  const [loading, setLoading] = React.useState(true);
  const [patient, setPatient] = React.useState({});

  const onOpen = () => {
    setOpen(true);
    setLoading(true);
    
    PatientAPI.get_by_id(props.patient_id)
      .then((patient) => {
        setPatient(patient);
        setLoading(false);
      })
      .catch((err) => {
        console.log(err);
      });
  };

  return (
    <>
      <Button type="primary" onClick={onOpen}>
        View Details
      </Button>
      <Modal
        title={<p>Patient {props.patient_id} info </p>}
        footer={
          <Button type="primary" onClick={() => setOpen(false)}>
            Close
          </Button>
        }
        loading={loading}
        open={open}
        onCancel={() => setOpen(false)}
        width={1000}
      >
        <Descriptions>
          <Descriptions.Item label="ID">{patient.id}</Descriptions.Item>
          <Descriptions.Item label="Name">{patient.name}</Descriptions.Item>
          <Descriptions.Item label="Admission Date">{patient.admission_date}</Descriptions.Item>
          {
            criteria_metadata.map((criteria) => {
              return (
                <Descriptions.Item key={criteria.name} label={criteria.label}>
                  {
                    (() => {
                      if (criteria.type === "boolean") {
                        return patient[criteria.name] === 1 ? "True" : "False";
                      } else if (criteria.type === "enum") {
                        return criteria.values[patient[criteria.name]];
                      } else {
                        return patient[criteria.name];
                      }
                    })()
                  }
                </Descriptions.Item>
              );
            })
          }
        </Descriptions>
      </Modal>
    </>
  );
};
export default ViewPatientModal;