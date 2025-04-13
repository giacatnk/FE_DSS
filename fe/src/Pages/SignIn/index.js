import React from 'react';
import { Layout, Form, Input, Button } from 'antd';
import { UserOutlined } from '@ant-design/icons';
import { useDispatch, useSelector } from 'react-redux';
import { LogIn } from '../../Stores/authentication/authentication.action';
import { useNavigate } from "react-router-dom";
import SignInScreen from "../../Assets/Images/signin_screen.svg"
import Logo from "../../Assets/Images/logo.svg"

const { Content, Footer } = Layout;
const contentStyle = {
    backgroundColor: 'white',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
};

const SignIn = (props) => {
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const isLoggedIn = useSelector(state => state.authentication.isLoggedIn);
    const [form] = Form.useForm();

    const onSignIn = () => {
        const fields = form.getFieldsValue();
        const data = {
            username: fields.username,
            password: fields.password
        }
        dispatch(LogIn(data));
    }
    if (isLoggedIn) {
        navigate('/patients');
    } else return <Layout>
        <Content style={contentStyle}>
            <div style={{ position: 'relative', width: '65%' }}>
                <div style={{ position: 'absolute', display: 'flex', alignItems: 'center', top: '20px', left: '-40px' }}>
                    <img src={Logo} alt="Logo" style={{ width: '35px', marginRight: '10px' }} />
                    <h1> Intelligent System </h1>
                </div>
                <img src={SignInScreen} alt="Sign In SVG" style={{ width: '100%' }} />
            </div>
            <div style={{
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'flex-end',
                alignItems: 'space-between',
            }}>
                <h1 style={{ fontSize: '30px', margin: '35px 0px' }}> Welcome to Aceso! </h1>
                <Form layout='vertical' autoComplete="off" requiredMark={false} form={form} onFinish={onSignIn}>
                    <Form.Item name="username"
                        rules={[
                            {
                                required: true,
                                message: 'Please input your username!',
                            },
                        ]}
                    >
                        <Input suffix={<UserOutlined />} placeholder='Username' />
                    </Form.Item>
                    <Form.Item name="password"
                        rules={[
                            {
                                required: true,
                                message: 'Please input your password!',
                            },
                        ]}
                    >
                        <Input.Password placeholder="Password" className='input-password' />
                    </Form.Item>
                    <Form.Item>
                        <Button type="primary" htmlType="submit" className='custom-button'>
                            Sign In
                        </Button>
                    </Form.Item>
                </Form>
            </div>
        </Content>
        <Footer />
    </Layout>
}

export default SignIn;