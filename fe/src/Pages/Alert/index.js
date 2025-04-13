import React, { useEffect, useState } from 'react';
import { Layout, Table, Row, Col, message, Button, Space, Breadcrumb, List, Avatar } from 'antd';
import Header from '../../Layouts/Header';
import { Link, useNavigate } from 'react-router-dom';
import AlertAPI from '../../API/Services/Alert';

const { Content, Footer } = Layout;
const contentStyle = {
  textAlign: 'center',
  padding: '0 50px',
  margin: '16px 0 0 0'
};

const AlertHistory = (props) => {
    const [alerts, setalerts] = useState([]);
    const [getAlertDone, setGetAlertDone] = useState(false);

    useEffect(() => {
        AlertAPI.get().then(
            (response) => {
                setalerts(response.data.alerts);
                setGetAlertDone(true);
            }
        ).catch((error) => {
            console.log(error);
            message.error('Error while getting alerts');
        })
    }, []);
    
    return <Layout>
        <Header selectedKey={'1'}/>
        <Content style={contentStyle}>
            <Row gutter={[16, 0]} align="middle">
                <Col span={24}>
                    <h1 className='custom-h1-header'>
                        Alert History
                    </h1>
                </Col>
            </Row>
            <div className='site-layout-content'>
                <div className='site-content'>
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
                        <List.Item.Meta
                        avatar={<Avatar src={`https://api.dicebear.com/7.x/miniavs/svg?seed=${index}`} />}
                        title={<a href="https://ant.design">{item.title}</a>}
                        description="Ant Design, a design language for background applications, is refined by Ant UED Team"
                        />
                    </List.Item>
                    )}
                />
                </div>
            </div>
        </Content>
        <Footer />
    </Layout>
}

export default AlertHistory;