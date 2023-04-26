import React from "react";
import { LoginOutlined, UserAddOutlined } from '@ant-design/icons';
import { Link } from 'react-router-dom';
import { Menu } from 'antd';

const GuestNavigation = (props) => {
    return <Menu
        style={{ backgroundColor: 'inherit', float: 'right' }}
        theme="dark"
        mode="horizontal">
        <Menu.Item
            key={1}
            icon={<LoginOutlined />}>
            <Link to={'/signin'}>
                <span style={{ color: 'white' }}>
                    Sign in
                </span>
            </Link>
        </Menu.Item>
    </Menu>
}

export default GuestNavigation;