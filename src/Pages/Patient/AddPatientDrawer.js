import React, { useState, useEffect } from 'react';
import { MinusCircleOutlined, PlusCircleFilled, PlusOutlined, ImportOutlined } from '@ant-design/icons';
import { Button, Col, DatePicker, Drawer, Form, Input, Row, Select, Space } from 'antd';


const criteria_metadata = [
    { name: "age", label: "Age", type: "integer" },
    { name: "weight", label: "Weight", type: "float" },
    { name: "gender", label: "Gender", type: "select", values: [{ value: "male", label: "Male" }, { value: "female", label: "Female" }] },
    { name: "platelets", label: "Platelets", type: "float" },
    { name: "spo2", label: "SpO2", type: "float" },
    { name: "creatinine", label: "Creatinine", type: "float" },
    { name: "hematocrit", label: "Hematocrit", type: "float" },
    { name: "aids", label: "AIDS", type: "boolean" },
    { name: "limphoma", label: "Lymphoma", type: "boolean" },
    { name: "solid_tumor_with_metastasis", label: "Solid Tumor with Metastasis", type: "boolean" },
    { name: "heart_rate", label: "Heart Rate", type: "float" },
    { name: "calcium", label: "Calcium", type: "float" },
    { name: "wbc", label: "WBC", type: "float" },
    { name: "glucose", label: "Glucose", type: "float" },
    { name: "inr", label: "INR", type: "float" },
    { name: "potassium", label: "Potassium", type: "float" },
    { name: "sodium", label: "Sodium", type: "float" },
    { name: "ethicity", label: "Ethicity", type: "select", values: [{ value: "white", label: "White" }, { value: "black", label: "Black" }, { value: "hispanic", label: "Hispanic" }, { value: "asian", label: "Asian" }] },
]

const AddPatientDrawer = (props) => {
    const [open, setOpen] = useState(false);
    const [confirmLoading, setConfirmLoading] = useState(false);
    const [form] = Form.useForm()

    const showDrawer = () => {
        setOpen(true);
    };

    const onClose = () => {
        setOpen(false);
    };

    const onSubmitForm = () => {
        // TODO: Add API Create Patient
        console.log("Form submitted");
        console.log(form.getFieldsValue());
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
                                                                    criteria_metadata.map((item) => ({
                                                                        value: item.name,
                                                                        label: item.label,
                                                                    }))
                                                                }
                                                            />
                                                        </Form.Item>
                                                    </Col>
                                                    <Col span={11}>
                                                        <Form.Item colon={false} {...restField} name={[name, 'value']}
                                                            rules={[
                                                                {
                                                                    required: true,
                                                                    message: 'Please fill criteria value',
                                                                },
                                                            ]}
                                                        >
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
                        </Col>
                    </Row>
                </Form>
            </Drawer>
        </>
    );
};

export default AddPatientDrawer;