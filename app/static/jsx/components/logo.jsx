// import React from 'react';
// import logo from '../logo.svg'

const SVGLogo = (props)=>{

    const imgStyle = {
        height: props.height,
        width: props.height,
        marginTop: '-10px'
    } 
    
    const blockStyle = {
        backgroundColor: '#860037', 
        // color: 'white', 
        // paddingLeft: '5px', 
        // display:'inline-block',
        verticalAlign: 'middle',
        width: props.width,
        height: props.height,
        display: 'flex',
        alignItems: 'center'
    }
    
    const titleStyle = {
        marginLeft: '5px',
        fontSize: '36pt',
    }

    return (
        <div className="sidebar-header" style={blockStyle}>
                <img id="logo-img" src={'../static/photos/logo.svg'} style={imgStyle}/>
                <h2 style={titleStyle}>PyGoat</h2> 
        </div>
    )
}

export {SVGLogo}