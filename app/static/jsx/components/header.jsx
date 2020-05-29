// import React from 'react';

const GoatHeader = (props)=>{

    const headerStyle = {
        display: 'flex',
        alignItems: 'center',
    }
    
    const blockStyle = {
        backgroundColor: '#333333', 
        color: 'white', 
        display:'inline-block',
        height: props.height,
        width: '100%'
    }
    
    const titleStyle = {
        fontSize: '36pt',
        fontWeight: 'lightest'

    }

    const titleBoxStyle = {
        display: 'flex',
        paddingLeft: '60px',
        alignItems: 'center',
    }

    return (
        <header style={blockStyle}>
            <div style={headerStyle}>
                <div style={{display: 'inline-block'}}>
                    {props.children[0]  /* The first child should be the Logo and Name of the App */}

                </div>
                <div style={titleBoxStyle}>
                    <h1 style={titleStyle}>{props.title}</h1>
                </div>
                {props.children[1]  /* The second child should be the site navigation panel*/}
            </div>
        </header>
    )
}

export {GoatHeader}