import React from "react";
import { AlertOutlined, UserOutlined } from '@ant-design/icons';
import { Link } from 'react-router-dom';
import { Menu } from 'antd';

const FeatureNavigation = (props) => {
    const ProjectNavItems = [
        { label: 'Patients', to: `/patients`, icon: <UserOutlined /> },
        { label: 'Alerts', to: `/alerts`, icon: <AlertOutlined /> },
    ]

    return <Menu
        className='custom-header-menu'
        style={{ backgroundColor: 'inherit', marginLeft: '8px', float: 'left', width: '70%' }}
        theme="dark"
        mode="horizontal"
        selectedKeys={[props.selectedKey]}
        items={ProjectNavItems.map((item, index) => {
            const key = index + 1;
            return {
                key,
                icon: item.icon,
                label: <Link to={item.to}>
                    <span style={{ color: '#F6F7F8' }}>
                        {item.label}
                    </span>
                </Link>,
            };
        })}
    />
}

export default FeatureNavigation;