import React from "react";
import { UserOutlined } from '@ant-design/icons';
import { Link } from 'react-router-dom';
import { Menu } from 'antd';
import { useSelector, useDispatch } from 'react-redux';
import { LogOut } from "../../../Stores/authentication/authentication.action";

const UserNavigation = (props) => {
    const dispatch = useDispatch();
    const authentication = useSelector(state => state.authentication);
    return <Menu
        style={{ backgroundColor: 'inherit', width: '10%', float: 'right' }}
        theme="dark"
        mode="horizontal"
        items={[
            { 
                key: 1, icon: <UserOutlined style={{ color: 'white' }} />, label: <span style={{ color: 'white' }}> {authentication.userInformation.username} </span>,
                children: [
                    { key: 2, label: <span> Logout </span>, onClick: () => { 
                        dispatch(LogOut());
                    } }
                ]
            }
        ]}
        />
}

export default UserNavigation;