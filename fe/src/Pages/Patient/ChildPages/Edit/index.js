import React, {useEffect, useState}  from 'react';
import { Layout, Table, Row, Col, Form, Input, Select, DatePicker, Button } from 'antd';
import Header from '../../../../Layouts/Header';
import { useParams } from 'react-router-dom';
import PatientAPI from '../../../../API/Services/Patient';
import dayjs from 'dayjs';
import criteria_metadata from '../../../../Utils/criteria_metadata';

const { Content, Footer } = Layout;
const contentStyle = {
  textAlign: 'center',
  padding: '0 50px',
  margin: '16px 0 0 0'
};

const EditPatient = (props) => {
    const [form] = Form.useForm();
    const [confirmLoading, setConfirmLoading] = useState(false);
    const params = useParams();

    const onSubmitForm = () => {
        // TODO: Add API Create Patient
        console.log("Form submitted");
        const fields = form.getFieldsValue();
        let data = {}
        for (const key in fields) {
            if (key === "date_of_birth") {
                data[key] = fields[key].format("YYYY-MM-DD");
            } else if (fields[key] !== undefined) {
                data[key] = fields[key];
            }
        }
        console.log(data);
    }

    useEffect(() => {
        PatientAPI.get_by_id(params.id).then((res) => {
            const patient = res.data.patient;
            if (patient.date_of_birth) {
                patient.date_of_birth = dayjs(patient.date_of_birth);
            }

            for (const key in criteria_metadata) {
                if (patient[criteria_metadata[key].name] === undefined) {
                    patient[criteria_metadata[key].name] = null;
                }
                if (criteria_metadata[key].type === "boolean") {
                    patient[criteria_metadata[key].name] = Boolean(patient[criteria_metadata[key].name]);
                }
            }
            console.log(patient);
            form.setFieldsValue(patient);
    })}, [params.id, form]);
    
    return <Layout>
        <Header selectedKey={'1'}/>
        <Content style={contentStyle}>
            <Row gutter={[16, 0]} align="middle">
                <Col span={24}>
                    <h1 className='custom-h1-header'>
                        Edit patient {params.id}
                    </h1>
                </Col>
            </Row>
            <div className='site-layout-content'>
                <div className='site-content'>
                    <Form layout="vertical" form={form} autoComplete='off' onFinish={onSubmitForm}>
                        <Row gutter={16}>
                            <Col span={24}>
                            <Button
                                className='custom-button' 
                                onClick={() => { form.submit() }} 
                                type="primary"
                                htmlType='submit'
                                loading={confirmLoading}
                                style={{ float: 'right' }}
                            >
                            Submit
                        </Button>
                            </Col>
                            <Col span={24}>
                                <Form.Item
                                    name="name" label="Name"
                                    rules={[
                                        {
                                            required: true,
                                            message: 'Please enter patient name'
                                        },
                                        {
                                            pattern: RegExp(/^[^,;{}()\n\t=#-.|]+$/),
                                            message: "Patient name must not contain character in ' ,;{}()\n\t=#-.|'"
                                        }]}
                                >
                                    <Input placeholder='Fill a name'/>
                                </Form.Item>
                            </Col>
                            <Col span={12}>
                                <Form.Item
                                    name="date_of_birth" label="Date of Birth"
                                    rules={[{ required: true, message: "Please fill patient's date of birth" }]}
                                >
                                    <DatePicker style={{ width: '100%' }} placeholder="Select date of birth" />
                                </Form.Item>
                            </Col>
                            <Col span={12}>
                                <Form.Item
                                    name="gender" label="Gender"
                                    rules={[{ required: true, message: "Please fill patient's gender" }]}
                                >
                                    <Select 
                                        options={[
                                            {value: "male", label: "Male"},
                                            {value: "female", label: "Female"}
                                        ]}
                                        placeholder="Choose a gender"
                                        style={{ textAlign: 'left' }}
                                    />
                                </Form.Item>
                            </Col>
                            <Col span={12}>
                                <Form.Item name="age" label="Age">
                                    <Input type='number' placeholder='Fill an age'/>
                                </Form.Item>
                            </Col>
                            <Col span={12}>
                                <Form.Item name="weight" label="Weight">
                                    <Input placeholder='Fill a weight'/>
                                </Form.Item>
                            </Col>
                            <Col span={8}>
                                <Form.Item name="platelets" label="Platelets">
                                    <Input placeholder='Fill platelets'/>
                                </Form.Item>
                            </Col>
                            <Col span={8}>
                                <Form.Item name="spo2" label="SpO2">
                                    <Input placeholder='Fill SpO2'/>
                                </Form.Item>
                            </Col>
                            <Col span={8}>
                                <Form.Item name="creatinine" label="Creatinine">
                                    <Input placeholder='Fill creatinine'/>
                                </Form.Item>
                            </Col>
                            <Col span={8}>
                                <Form.Item name="hematocrit" label="Hematocrit">
                                    <Input placeholder='Fill hematocrit'/>
                                </Form.Item>
                            </Col>
                            <Col span={8}>
                                <Form.Item name="aids" label="AIDS">
                                    <Select 
                                        options={[
                                            {value: true, label: "True"},
                                            {value: false, label: "False"}
                                        ]}
                                        placeholder="Choose a boolean value"
                                        allowClear
                                        style={{ textAlign: 'left' }}
                                    />
                                </Form.Item>
                            </Col>
                            <Col span={8}>
                                <Form.Item name="lymphoma" label="Lymphoma">
                                    <Select 
                                        options={[
                                            {value: true, label: "True"},
                                            {value: false, label: "False"}
                                        ]}
                                        placeholder="Choose a boolean value"
                                        allowClear
                                        style={{ textAlign: 'left' }}
                                    />
                                </Form.Item>
                            </Col>
                            <Col span={8}>
                                <Form.Item name="solid_tumor_with_metastasis" label="Solid Tumor with Metastasis">
                                    <Select 
                                        options={[
                                            {value: true, label: "True"},
                                            {value: false, label: "False"}
                                        ]}
                                        placeholder="Choose a boolean value"
                                        allowClear
                                        style={{ textAlign: 'left' }}
                                    />
                                </Form.Item>
                            </Col>
                            <Col span={8}>
                                <Form.Item name="heartrate" label="Heart Rate">
                                    <Input placeholder='Fill heart rate'/>
                                </Form.Item>
                            </Col>
                            <Col span={8}>
                                <Form.Item name="calcium" label="Calcium">
                                    <Input placeholder='Fill calcium'/>
                                </Form.Item>
                            </Col>
                            <Col span={8}>
                                <Form.Item name="wbc" label="WBC">
                                    <Input placeholder='Fill WBC'/>
                                </Form.Item>
                            </Col>
                            <Col span={8}>
                                <Form.Item name="glucose" label="Glucose">
                                    <Input placeholder='Fill glucose'/>
                                </Form.Item>
                            </Col>
                            <Col span={8}>
                                <Form.Item name="inr" label="INR">
                                    <Input placeholder='Fill INR'/>
                                </Form.Item>
                            </Col>
                            <Col span={8}>
                                <Form.Item name="potassium" label="Potassium">
                                    <Input placeholder='Fill potassium'/>
                                </Form.Item>
                            </Col>
                            <Col span={8}>
                                <Form.Item name="sodium" label="Sodium">
                                    <Input placeholder='Fill sodium'/>
                                </Form.Item>
                            </Col>
                            <Col span={8}>
                                <Form.Item name="ethnicity" label="Ethnicity">
                                    <Select 
                                        options={[
                                            {value: 1, label: "White"},
                                            {value: 2, label: "Black"},
                                            {value: 3, label: "Asian"},
                                            {value: 4, label: "Latino"},
                                            {value: 5, label: "Others"}
                                        ]}
                                        placeholder="Choose a boolean value"
                                        allowClear
                                        style={{ textAlign: 'left' }}
                                    />
                                </Form.Item>
                            </Col>
                        </Row>
                    </Form>
                </div>
            </div>
        </Content>
        <Footer />
    </Layout>
}

export default EditPatient;