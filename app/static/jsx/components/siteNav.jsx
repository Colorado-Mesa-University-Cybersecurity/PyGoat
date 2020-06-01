/*
File: siteNav.jsx
Description: file exports the SiteNavigator React Component which implements the site navigation menu 
                contained in the upper right hand corner of the application

IMPORTANT!!! If you are reading this from within a .js file, it is important to note that you should not 
	make any changes to that file if you wish to edit the PyGoat client, instead follow the directions on 
	the README.md contained within the static directory. Make sure any editing is done with the .jsx version
	of this file inside the static/jsx directory

Conventions followed:
    4-space tabs
    always place semicolons
    3 empty lines between classes and functions
    2 empty lines between methods
    Class methods always return this unless other return value desired
    Annotations follow the convention:     
            function/method  ::  (parameter types) -> (return types)
*/


'use strict'



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