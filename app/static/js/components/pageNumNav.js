/*
File: pageNumNav.jsx
Description: file exports the PageNumButton React Component which implements the application's 
                lesson navigation, allowing users to view lessons page-by-page

IMPORTANT!!! If you are reading this from within a .js file,   EXIT THE FILE!!!   Go to the jsx/components directory 
    and find pageNumNav.jsx.  React is Transpiled from JSX, unless you are familiar with React, you will not
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

'use strict';

/**
 * PageNumButton  ::  Object  ->  JSX
 * 
 * @param {'Object'} props 
 * 
 * Component creates page number navigation buttons that render the chosen page index when clicked
 *      
 * Returns a JSX component
 */

const PageNumButton = props => {

    const pageNumStyle = {
        backgroundColor: props.active ? '#ffd200' : '#c4c4c4'
        // border: '0pt',
        // marginTop: '20px',
        // marginRight: '20px',
        // marginBottom: '10px',
        // borderRadius: '4px',
    };

    const handleClick = e => {
        props.store.refresh.innerHTMLReRender(props.num);
        if (props.store.checkCurrentPageNumber() != props.num) {
            props.store.changeCurrentPageNumber(props.num);
            props.store.refresh.rootReRender(Math.random());
        };
        fetch('/save.json', {
            method: 'POST',
            'Content-Type': 'application/json',
            body: JSON.stringify(props.store.warehouse)
        });
    };

    return React.createElement(
        'button',
        { className: 'page-num-nav', style: pageNumStyle, onClick: handleClick },
        props.num
    );
};

export { PageNumButton };