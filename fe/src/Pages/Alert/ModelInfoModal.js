import React, { useEffect } from 'react';
import { Button, Descriptions, Modal, Progress, Row, Col, Statistic } from 'antd';
import { InfoCircleOutlined } from '@ant-design/icons';

const formatPercent = (value) => {
    if (value > 1) {
        return value;
    }
    return (value * 100).toFixed(2);
}

const ModelInfoModal = (props) => {
    const [model, setModel] = React.useState(null);
    const [open, setOpen] = React.useState(false);

    const onOpen = () => {
        setOpen(true);
    };

    useEffect(() => {
        if (props.model) {
            setModel(props.model);
        }
    }, [props.model]);

    return (
        <>
            <Button onClick={onOpen} icon={<InfoCircleOutlined />} />
            <Modal
                title="Model Infomation"
                footer={
                    <Button type="primary" onClick={() => setOpen(false)}>
                        Close
                    </Button>
                }
                open={open}
                onCancel={() => setOpen(false)}
                width={1000}
            >
                <Row gutter={16}>
                    <Col span={24}>
                        <Descriptions bordered column={1}>
                            <Descriptions.Item label="Status">{model?.status}</Descriptions.Item>
                            <Descriptions.Item label="Last Training Time">{model?.last_training_time}</Descriptions.Item>
                            <Descriptions.Item label="Version">{model?.version}</Descriptions.Item>
                            <Descriptions.Item label="Accuracy">
                                <Statistic
                                    value={formatPercent(model?.metrics?.accuracy)}
                                    precision={2}
                                    suffix="%"
                                />
                                <Progress percent={formatPercent(model?.metrics?.accuracy)} showInfo={false} />
                            </Descriptions.Item>
                            <Descriptions.Item label="Precision">
                                <Statistic
                                    value={formatPercent(model?.metrics?.precision)}
                                    precision={2}
                                    suffix="%"
                                />
                                <Progress percent={formatPercent(model?.metrics?.precision)} showInfo={false} />
                            </Descriptions.Item>
                            <Descriptions.Item label="Recall">
                                <Statistic
                                    value={formatPercent(model?.metrics?.recall)}
                                    precision={2}
                                    suffix="%"
                                />
                                <Progress percent={formatPercent(model?.metrics?.recall)} showInfo={false} />
                            </Descriptions.Item>
                            <Descriptions.Item label="F1 Score">
                                <Statistic
                                    value={formatPercent(model?.metrics?.f1_score)}
                                    precision={2}
                                    suffix="%"
                                />
                                <Progress percent={formatPercent(model?.metrics?.f1_score)} showInfo={false} />
                            </Descriptions.Item>
                            <Descriptions.Item label="Confusion Matrix">
                                <div style={{ display: 'flex', justifyContent: 'space-around' }}>
                                    <div>
                                        <h4>True Positive</h4>
                                        {model?.metrics?.confusion_matrix[1][1]}
                                    </div>
                                    <div>
                                        <h4>False Positive</h4>
                                        {model?.metrics?.confusion_matrix[0][1]}
                                    </div>
                                    <div>
                                        <h4>True Negative</h4>
                                        {model?.metrics?.confusion_matrix[0][0]}
                                    </div>
                                    <div>
                                        <h4>False Negative</h4>
                                        {model?.metrics?.confusion_matrix[1][0]}
                                    </div>
                                </div>
                            </Descriptions.Item>
                        </Descriptions>
                    </Col>
                </Row>
            </Modal>
        </>
    );
};
export default ModelInfoModal;