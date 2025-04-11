import React, { useEffect, useState } from 'react';
import { Layout, Table, Row, Col, message, Button, Space, Breadcrumb } from 'antd';
import Header from '../../Layouts/Header';
import { Link } from 'react-router-dom';
import PatientAPI from '../../API/Services/Patient';
import AddPatientDrawer from './AddPatientDrawer';

const { Content, Footer } = Layout;
const contentStyle = {
  textAlign: 'center',
  padding: '0 50px',
  margin: '16px 0 0 0'
};

const Patient = (props) => {
    const [patients, setpatients] = useState([]);
    const [getpatientDone, setGetpatientDone] = useState(false);
    const [triggerGetpatient] = useState(false);

    useEffect(() => {
        PatientAPI.get()
            .then((response) => {
                const patients = response.data.patients;
                setpatients(patients.map((patient) => ({
                    key: patient.id,
                    id: patient.id,
                    name: patient.name,
                    admission_date: patient.admission_date,
                    created_at: patient.created_at,
                    updated_at: patient.updated_at,
                })))
                setGetpatientDone(true);
            }).catch(err => {
                message.error(err.response.data.error);
            })
    }, [triggerGetpatient])
    
    const loadingProps = {
        spinning: !getpatientDone
    }

    const patientColumns = [
        { title: 'ID', dataIndex: 'id', key: 'id' },
        {},
        { 
            title: 'Name', dataIndex: 'name', key: 'name',
        },
        { 
            title: 'Admission Date', dataIndex: 'admission_date', key: 'admission_date',
            render: (date) => date ? new Date(date).toLocaleDateString('vi-VN') : date
        },
        { 
            title: 'Actions', key: 'actions',
            render: (_, record) => {
                return <Space size="middle">
                    <Button>View Details</Button>
                    <Button >Edit</Button>
                    <Button type='primary' danger>Delete</Button>
                </Space>
            }
        },
    ]

    return <Layout>
        <Header selectedKey={'1'}/>
        <Content style={contentStyle}>
            <Row gutter={[16, 0]} align="middle">
                <Col span={24}>
                    <h1 className='custom-h1-header'>
                        Patients
                    </h1>
                </Col>
            </Row>
            <div className='site-layout-content'>
                <div className='site-content'>
                    <AddPatientDrawer />
                    <Table columns={patientColumns} dataSource={patients} loading={loadingProps} />
                </div>
            </div>
        </Content>
        <Footer />
    </Layout>
}

export default Patient;