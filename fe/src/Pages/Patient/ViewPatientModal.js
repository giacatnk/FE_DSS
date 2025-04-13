import React, { useEffect } from 'react';
import { Button, Modal } from 'antd';
import PatientAPI from '../../API/Services/Patient';

const ViewPatientModal = (props) => {
  const [open, setOpen] = React.useState(false);
  const [loading, setLoading] = React.useState(true);
  const [patient, setPatient] = React.useState({});

  const onOpen = () => {
    setOpen(true);
    setLoading(true);
  };

  useEffect(() => {
    PatientAPI.get_by_id(props.patient_id)
      .then((response) => {
        const patient = response.data.patient;
        setPatient(patient);
        setTimeout(() => {
          setLoading(false);
        }, 1000);
      })
      .catch((err) => {
        console.log(err);
      });
  })
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
      >
        <p>Patient ID: {patient.id}</p>
        <p>Name: {patient.name}</p>
        <p>Admission Date: {patient.admission_date}</p>
        <p> TODO: Display criteria </p>
      </Modal>
    </>
  );
};
export default ViewPatientModal;