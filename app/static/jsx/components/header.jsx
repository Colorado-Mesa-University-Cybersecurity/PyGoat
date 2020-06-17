/*
File: header.jsx
Description: file exports the GoatHeader React Component which implements the applications header

IMPORTANT!!! If you are reading this from within a .js file,  EXIT THE FILE!!!  Go to the jsx/components directory 
    and find header.jsx.  React is Transpiled from JSX, unless you are familiar with React, you will not
    understand anything about the file unless you read the JSX file which is declarative and self documenting 

    it is important to note that you should not 
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


/**
 * GoatHeader  ::  Object  ->  JSX
 * 
 * @param {'Object'} props 
 * 
 * Component is composed of a logo and a site navigation component that are passed into the props under
 *      the key children. height of the header is derived from the height passed in using the key height 
 *      
 * Returns a JSX component
 */
const GoatHeader = (props)=>{

    const blockStyle = {
        backgroundColor: '#333333', // these are not in main.css because they would be over-written
        color: 'white', 
        height: props.height,
    }

    return (
        <header style={blockStyle} className='w100 inBlock'>
            <div className='boxIt'>
                <div style={{display: 'inline-block'}}>
                    {props.children[0]  /* The first child should be the Logo and Name of the App */}

                </div>
                <div className='boxIt header-title-box'>
                    <h1 className='header-title' >{props.title}</h1>
                </div>
                {props.children[1]  /* The second child should be the site navigation panel*/}
            </div>
        </header>
    )
}

export {GoatHeader}