/*
File: logo.jsx
Description: file exports the Logo React Component which implements the logo and application Title at the top 
                left corner of the application

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

'use strict';

/**
 * SVGLogo  ::  Object  ->  JSX
 * 
 * @param {'Object'} props 
 * 
 * Component instantiates the Logo and App Title in the top left corner of the client's screen
 *      
 * Returns a JSX component
 */

const SVGLogo = props => {

    const imgStyle = {
        height: props.height,
        width: props.height,
        marginTop: '-10px'
    };

    const blockStyle = {
        width: props.width,
        height: props.height,
        verticalAlign: 'middle'
    };

    return React.createElement(
        'div',
        { className: 'sidebar-header boxIt themeColor1', style: blockStyle },
        React.createElement('img', { id: 'logo-img', src: '../static/photos/logo.svg', style: imgStyle }),
        React.createElement(
            'h2',
            { className: 'page-title' },
            'PyGoat'
        )
    );
};

export { SVGLogo };