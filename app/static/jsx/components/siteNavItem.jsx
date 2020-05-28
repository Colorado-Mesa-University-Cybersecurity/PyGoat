// import React from 'react';

const SiteNavItem = (props) => {

    const navItemStyle = {
        height: props.height,
    }


    return (
        <button className='site-nav-item' style={navItemStyle}>
            <h3>{props.title}</h3>
        </button>
    )
}

export {SiteNavItem}