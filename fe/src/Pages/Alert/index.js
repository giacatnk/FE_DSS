import React, { useEffect, useState } from 'react';
import { Layout, Row, Col, message, Button, List, Card, Popconfirm, Progress, Space } from 'antd';
import Header from '../../Layouts/Header';
import { Link } from 'react-router-dom';
import AlertAPI from '../../API/Services/Alert';
import ModelAPI from '../../API/Services/Model';
import Meta from 'antd/es/card/Meta';
import ModelInfoModal from './ModelInfoModal';

const { Content, Footer } = Layout;
const contentStyle = {
    textAlign: 'center',
    padding: '0 50px',
    margin: '16px 0 0 0',
    height: '100vh'
};

const AlertHistory = (props) => {
    const [alerts, setAlerts] = useState([]);
    const [model, setModel] = useState(null);
    const [getAlertDone, setGetAlertDone] = useState(false);

    useEffect(() => {
        AlertAPI.get().then(
            (response) => {
                setAlerts(response.data.alerts);
                setGetAlertDone(true);
            }
        ).catch((error) => {
            console.log(error);
            message.error('Error while getting alerts');
        })

        ModelAPI.get().then(
            (response) => {
                setModel(response.data.model);
            }
        ).catch((error) => {
            console.log(error);
            message.error('Error while getting model');
        })
    }, []);

    const onMarkAsFalsePositive = (alert_id) => {
        AlertAPI.mark_as_false_positive(alert_id).then(
            (response) => {
                message.success(response.data.message);
            }
        ).catch((error) => {
            console.log(error);
            message.error('Error while marking alert as false positive');
        })
    }

    return <Layout>
        <Header selectedKey={'1'} />
        <Content style={contentStyle}>
            <Row gutter={[16, 0]} align="middle">
                <Col span={24}>
                    <h1 className='custom-h1-header'>
                        Alert History
                    </h1>
                </Col>
                <Col span={24}>
                    <Space style={{ float: 'right' }}>
                        {
                            ((status) => {
                                if (status === "training") {
                                    return <Button type="primary" loading style={{ float: 'right' }}>
                                        Training
                                    </Button>
                                } else {
                                    return <><Button type="primary" >
                                        Update Model
                                    </Button>
                                        <ModelInfoModal model={model} />
                                    </>
                                }
                            })(model?.status)
                        }
                    </Space>
                </Col>
            </Row>
            <List
                itemLayout="horizontal"
                pagination={{
                    onChange: page => {
                        console.log(page);
                    },
                    pageSize: 3,
                }}
                dataSource={alerts}
                renderItem={(item, index) => (
                    <List.Item>
                        <Card style={{ width: '100%', textAlign: 'left' }}>
                            <Meta description={item?.created_at} />
                            <h3>
                                Patient "{item?.patient_name}" <Link to={`/patients/${item?.patient_id}`}>#{item?.patient_id}</Link> is having symptoms of Diabetes
                            </h3>
                            <p>
                                Confidence <Progress percent={Math.round(item.confidence * 10000) / 100} percentPosition={{ align: 'center', type: 'inner' }} size={[300, 20]} />
                            </p>
                            {
                                (() => {
                                    if (item?.is_correct === null) {
                                        return <Popconfirm
                                            title="Mark as false positive"
                                            description="Are you sure to mark this alert as false positive?"
                                            onConfirm={() => onMarkAsFalsePositive(item.id)}
                                            okText="Yes"
                                            cancelText="No"
                                        >
                                            <Button style={{ float: 'right' }} danger>Mark as false positive</Button>
                                        </Popconfirm>
                                    } else {
                                        return <Button type='primary' style={{ float: 'right' }} danger> False positive alert </Button>
                                    }
                                })()
                            }
                        </Card>
                    </List.Item>
                )}
            />
        </Content>
        <Footer />
    </Layout>
}

export default AlertHistory;