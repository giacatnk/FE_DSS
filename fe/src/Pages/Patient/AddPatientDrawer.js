import React, { useState, useEffect } from 'react';
import { MinusCircleOutlined, PlusCircleFilled, PlusOutlined, ImportOutlined } from '@ant-design/icons';
import { Button, Col, DatePicker, Drawer, Form, Input, Modal, Row, Select, Space, message } from 'antd';

const AddPatientDrawer = (props) => {
    const [open, setOpen] = useState(false);
    const [confirmLoading, setConfirmLoading] = useState(false);
    const [form] = Form.useForm();
    const patientApi = props.api

    const showDrawer = () => {
        setOpen(true);
    };

    const onClose = () => {
        setOpen(false);
    };

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

    const handleImport = () => {
        Modal.confirm({
            title: 'Confirm Import',
            content: 'This will import new patients from the source database. Are you sure you want to proceed?',
            okText: 'Import',
            cancelText: 'Cancel',
            onOk: () => {
                // Call the sync endpoint
                patientApi.sync()
                    .then(response => {
                        message.success('Import completed successfully');
                        // Refresh the patient list
                        queryClient.invalidateQueries(['patients']);
                    })
                    .catch(error => {
                        message.error('Import failed: ' + error.message);
                    });
            },
            onCancel: () => {
                message.info('Import cancelled');
            }
        });
    };

    return (
        <>
            <Space style={{ float: 'right' }}>
                <Button className='custom-button' type="primary" onClick={showDrawer} icon={<PlusCircleFilled />} style={{ marginBottom: '10px', float: 'right' }}>
                    Add
                </Button>
                <Button className='custom-button' type="primary" icon={<ImportOutlined />} onClick={handleImport} style={{ marginBottom: '10px', float: 'right' }}>
                    Import
                </Button>
            </Space>
            <Drawer
                title="Add new patient"
                width={720} onClose={onClose} open={open}
                bodyStyle={{ paddingBottom: 80 }}
                extra={
                    <Space>
                        <Button className='custom-ghost-button' onClick={onClose}>Cancel</Button>
                        <Button
                            className='custom-button' 
                            onClick={() => { form.submit() }} 
                            type="primary"
                            htmlType='submit'
                            loading={confirmLoading}
                        >
                            Submit
                        </Button>
                    </Space>
                }
            >
                <Form layout="vertical" form={form} autoComplete='off' onFinish={onSubmitForm}>
                    <Row gutter={16}>
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
                                        message: "Patient name must not contain character in ',;{}()\n\t=#-.|'"
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
                                />
                            </Form.Item>
                        </Col>
                        <Col span={8}>
                            <Form.Item name="limphoma" label="Lymphoma">
                                <Select 
                                    options={[
                                        {value: true, label: "True"},
                                        {value: false, label: "False"}
                                    ]}
                                    placeholder="Choose a boolean value"
                                    allowClear
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
                            <Form.Item name="ethicity" label="Ethicity">
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
                                />
                            </Form.Item>
                        </Col>
                    </Row>
                </Form>
            </Drawer>
        </>
    );
};

export default AddPatientDrawer;