import React from 'react';
import { Link } from 'react-router-dom';
import './index.css';
const Header = () => {
    return <>
        <div id="header"> 
            <nav className='nav-header'>
                <ul className='nav-header-list'>
                    <li className='nav-header-element'>
                        <Link className='nav-header-link' to={`/`}> Dashboard </Link>
                    </li>
                    <li className='nav-header-element'>
                        <Link className='nav-header-link' to={`/deltas`}> Delta Table </Link>
                    </li>
                    <li className='nav-header-element'>
                        <Link className='nav-header-link' to={`/ingestions`}> Ingestion </Link>
                    </li>
                    <li className='nav-header-element'>
                        <Link className='nav-header-link' to={`/models`}> Model ML </Link>
                    </li>
                </ul>
            </nav>
        </div>
    </>
}

export default Header;