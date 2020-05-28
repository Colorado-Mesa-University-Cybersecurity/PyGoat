// import React from 'react';

const SiteNavigator = (props)=>{

    const navStyle = {
        color: 'black',
        display:'inline-block',
        verticalAlign: 'middle',
        backgroundColor: '#ffd200',
        height: props.height,
        marginLeft:'auto',
        marginRight: '0px',
        width: '140px'
    }

    return (
        <div style={navStyle}>
            {props.children}
        </div>
    )
}

export {SiteNavigator}