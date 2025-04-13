import React, { useState, useEffect } from 'react';
import { Layout, Row, Col, Button, message, List, Card, Popconfirm, Progress, Space } from 'antd';
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
    const [, setGetAlertDone] = useState(false);
    const [showAllAlerts, setShowAllAlerts] = useState(false);

    const handleShowAllToggle = () => {
        setShowAllAlerts(!showAllAlerts);
    };
    const filteredAlerts = showAllAlerts ? alerts : alerts.filter(alert => alert.prediction);

    const intervalPoolingModelUntilCompleted = () => {
        setTimeout(() => {
            ModelAPI.get().then(
                (model) => {
                    setModel(model);
                    if (model.status === "training") {
                        intervalPoolingModelUntilCompleted();
                    } else {
                        message.success('Model training completed');
                    }
                }
            ).catch((error) => {
                console.log(error);
                message.error('Error while getting model');
            })
        }, 500)
    }

    useEffect(() => {
        AlertAPI.get().then(
            (alerts) => {
                setAlerts(alerts);
                setGetAlertDone(true);
            }
        ).catch((error) => {
            console.log(error);
            message.error('Error while getting alerts');
        })

        ModelAPI.get().then(
            (model) => {
                setModel(model);
                if (model.status === "training") {
                    intervalPoolingModelUntilCompleted();
                }
            }
        ).catch((error) => {
            console.log(error);
            message.error('Error while getting model');
        })
    }, []);

    const onUpdateModel = () => {
        setModel({ ...model, status: "training" });
        ModelAPI.update().then(
            (response) => {
                message.success(response.data.message);
                intervalPoolingModelUntilCompleted();
            }
        ).catch((error) => {
            console.log(error);
            message.error('Error while updating model');
        })
    }

    const onMarkAsFalsePrediction = (alert_id) => {
        AlertAPI.mark_as_false_positive(alert_id).then(
            (response) => {
                message.success(response.data.message);
            }
        ).catch((error) => {
            console.log(error);
            message.error('Error while marking alert as false prediction');
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
                                    return <><Button type="primary" onClick={onUpdateModel}>
                                        Update Model
                                    </Button>
                                        <ModelInfoModal model={model} />
                                    </>
                                }
                            })(model?.status)
                        }
                        <Button
                            type="primary"
                            onClick={handleShowAllToggle}
                            style={{ marginRight: '10px' }}
                        >
                            {showAllAlerts ? 'Show Predicted Only' : 'Show All Alerts'}
                        </Button>
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
                dataSource={filteredAlerts}
                renderItem={(item, index) => (
                    <List.Item>
                        <Card style={{ width: '100%', textAlign: 'left' }}>
                            <Meta description={item?.created_at} />
                            <h3>
                                Patient <Link to={`/patients/${item?.patient}`}>#{item?.patient}</Link> is having symptoms of Diabetes
                            </h3>
                            
                            {item.confidence ? <p>
                                Confidence <Progress percent={Math.round(item.confidence * 10000) / 100} percentPosition={{ align: 'center', type: 'inner' }} size={[300, 20]} />
                            </p>: null}
                            {
                                (() => {
                                    if (item?.is_correct === null) {
                                        return <Popconfirm
                                            title="Mark as false prediction"
                                            description="Are you sure to mark this alert as false prediction?"
                                            onConfirm={() => onMarkAsFalsePrediction(item.id)}
                                            okText="Yes"
                                            cancelText="No"
                                        >
                                            <Button style={{ float: 'right' }} danger>Mark as False Prediction</Button>
                                        </Popconfirm>;
                                    }
                                    return null;
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