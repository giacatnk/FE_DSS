import React, { useState, useEffect } from 'react';
import { MinusCircleOutlined, FireOutlined, PlusCircleFilled, PlusOutlined, ImportOutlined } from '@ant-design/icons';
import { Button, Col, DatePicker, Drawer, Form, Input, message, Row, Select, Space, Switch, Table } from 'antd';
const { Option } = Select;

const AddPatientDrawer = (props) => {
    const [open, setOpen] = useState(false);

    const [confirmLoading, setConfirmLoading] = useState(false);
    const [validateLoading, setValidateLoading] = useState(false);

    const [validateErrors, setValidateErrors] = useState([]);

    const [form] = Form.useForm()


    const showDrawer = () => {
        setOpen(true);
    };

    const onClose = () => {
        setOpen(false);
    };

    const onSubmitForm = () => {
        // Add API Create Patient
        console.log("Form submitted");
        console.log(form.getFieldsValue());
        setConfirmLoading(false);
        
    }
    
    return (
        <>
            <Space style={{ float: 'right' }}>
                <Button className='custom-button' type="primary" onClick={showDrawer} icon={<PlusCircleFilled />} style={{ marginBottom: '10px', float: 'right' }}>
                    Add
                </Button>
                <Button className='custom-button' type="primary" icon={<ImportOutlined />} style={{ marginBottom: '10px', float: 'right' }}>
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
                        <Button className='custom-button' onClick={() => { form.submit() }} type="primary" htmlType='submit'
                            loading={confirmLoading}>
                            Submit
                        </Button>
                    </Space>
                }
            >
                <Form layout="vertical" form={form} autoComplete='off' onFinish={onSubmitForm}>
                    <Row gutter={16}>
                        <Col span={12}>
                            <Form.Item  
                                name="name" label="Name"
                                rules={[
                                    {
                                        required: true,
                                        message: 'Please enter patient name'
                                    },
                                    {
                                        pattern: RegExp(/^[^\s,;{}()\n\t=#-.|]+$/),
                                        message: "Patient name must not contain character in ' ,;{}()\n\t=#-.|'"
                                    }]}
                            >
                                <Input />
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
                        <Col span={24}>
                            <Form.Item colon={false} name="criterias">
                                <Form.List name="criterias">
                                    {(fields, { add, remove }) => (
                                        <>
                                            {fields.map(({ key, name, ...restField }) => (
                                                <div key={key}>
                                                    <Row gutter={32}>
                                                        <Col span={24}> Criteria {key + 1} </Col>
                                                        <Col span={11}>
                                                            <Form.Item colon={false} {...restField} name={[name, 'name']}
                                                                rules={[
                                                                    {
                                                                        required: true,
                                                                        message: 'Please fill criteria name',
                                                                    },
                                                                ]}
                                                            >
                                                                <Select 
                                                                    placeholder="Name" 
                                                                    options={
                                                                        [
                                                                            { value: 'fever', label: 'Fever' },
                                                                            { value: 'cough', label: 'Cough' },
                                                                            { value: 'headache', label: 'Headache' },
                                                                            { value: 'nausea', label: 'Nausea' },
                                                                            { value: 'diarrhea', label: 'Diarrhea' },
                                                                            { value: 'fatigue', label: 'Fatigue' },
                                                                            { value: 'muscle pain', label: 'Muscle pain' },
                                                                            { value: 'sore throat', label: 'Sore throat' },
                                                                        ]
                                                                    }
                                                                />
                                                            </Form.Item>
                                                        </Col>
                                                        <Col span={11}>
                                                            <Form.Item colon={false} {...restField} name={[name, 'value']}>
                                                                <Input placeholder="Value" />
                                                            </Form.Item>
                                                        </Col>
                                                        <Col span={2}>
                                                            <MinusCircleOutlined onClick={() => remove(name)} />
                                                        </Col>
                                                    </Row>
                                                </div>
                                            ))}
                                            <Form.Item colon={false}>
                                                <Button type="dashed" onClick={() => add()} block icon={<PlusOutlined />}>
                                                    Add a criteria
                                                </Button>
                                            </Form.Item>
                                        </>
                                    )}
                                </Form.List>
                            </Form.Item>
                        </Col>
                    </Row>
                </Form>
            </Drawer>
        </>
    );
};

export default AddPatientDrawer;