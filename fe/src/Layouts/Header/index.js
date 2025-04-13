import React from 'react';
import { Layout } from 'antd';
import LogoConstract from '../../Assets/Images/logo-constract.svg';
import GuestNavigation from './HeaderNavigation/GuestNavigation';
import UserNavigation from './HeaderNavigation/UserNavigation';
import { useSelector } from 'react-redux';
import FeatureNavigation from './HeaderNavigation/FeatureNavigation';
const { Header } = Layout

const layoutStyle = {
    display: 'flex',
    justifyContent: 'center',
}
const HeaderLayout = (props) => {
    const authentication = useSelector((state) => state.authentication);
    return <Layout style={{ ...layoutStyle }}>
        <Header className="header" style={{ 
        }}>
            <a href={'/'} style={{ float: 'left' }}>
                <div style={{ float: 'left', height: 'inherit', cursor: 'pointer' }}>
                    <img src={LogoConstract} alt='Logo Constract' style={{ width: '48px', height: '48px', marginTop: '8px' }} />
                    <span
                        style={{ fontSize: '25px', fontWeight: 'bold', color: 'white', float: 'right', margin: '0px 8px 0px 8px' }}>
                        ACESO
                    </span>
                </div>
            </a>
            { authentication.isLoggedIn ? <FeatureNavigation /> : null }
            { authentication.isLoggedIn ? <UserNavigation /> : <GuestNavigation /> }
            
        </Header>
    </Layout>
}

export default HeaderLayout;