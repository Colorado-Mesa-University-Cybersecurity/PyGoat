/*
File: siteNavItem.jsx
Description: file exports the SiteNavItem React Component which implements the individual buttons contained
                in the Site Navigation menu

IMPORTANT!!! If you are reading this from within a .js file,   EXIT THE FILE!!!   Go to the jsx/components directory 
    and find siteNavItem.jsx.  React is Transpiled from JSX, unless you are familiar with React, you will not
    understand anything about the file unless you read the JSX file which is declarative and self documenting 

    it is important to note that you should not 
	make any changes to that file if you wish to edit the PyGoat client, instead follow the directions on 
	the README.md contained within the static directory. Make sure any editing is done with the .jsx version
	of this file inside the static/jsx directory

Conventions followed:
    4-space tabs
    always place semicolons
    trailing commas in arrays and objects
    3 empty lines between classes and functions
    2 empty lines between methods
    Class methods always return this unless other return value desired
    Annotations follow the convention:     
            function/method  ::  (parameter types) -> (return types)
*/


"use strict";



export function SiteNavItem(props) {

    const navItemStyle = {
        height: props.height
        // backgroundColor: props.active? "#860037": "ffd200",
        // color: props.active? "white": "black"
    };

    const navClass = props.active ? "site-nav-item-active" : "site-nav-item";

    const handleClick = (e) => {
        props.store.refresh.innerHTMLReRender(props.title)
        if (props.store.checkActivePage().title != props.title && props.title != "Logout") {
            props.store.changeActivePage(props.title);
            props.store.refresh.rootReRender(Math.random());
        } else if (props.title == "Logout") {
            window.location.href = "logout";
        }
        fetch("/save", {
            method: "POST",
            "Content-Type": "application/json",
            body: JSON.stringify(props.store.warehouse)
        });
    };

    return (
        <button className={navClass} style={navItemStyle} onClick={handleClick}>
            <h3>{props.title}</h3>
        </button>
    );
}

// Preferred: Use shorthand syntax for export (see above)
// export {SiteNavItem}