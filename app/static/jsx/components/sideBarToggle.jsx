/*
File: sideBarToggle.jsx
Description: file exports the LessonNavToggleButton React Component which implements a button that 
                hides the lesson navigation sidebar when clicked

IMPORTANT!!! If you are reading this from within a .js file,   EXIT THE FILE!!!   Go to the jsx/components directory 
    and find sideBarToggle.jsx.  React is Transpiled from JSX, unless you are familiar with React, you will not
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



const LessonNavToggleButton = (props) => {

    const lessonToggleStyle = {
        backgroundColor: '#333333',
        border: '0pt',
        marginLeft: '20px',
        marginTop: '20px',
        marginRight: '20px',
        marginBottom: '10px',
        paddingTop: '5px',
        borderRadius: '4px',
    }

    const handleClick = (e) => {
        props.warehouse.hideSideBar = props.warehouse.hideSideBar? false: true;
        props.setToggle(Math.random())
    }

    return (
        <button style={lessonToggleStyle} onClick={handleClick}>
            <svg width="1em" height="1em" viewBox="0 0 20 20" fill="#333333" >
                <path fill='#eeeeee' fillRule="evenodd" d="M4 14.5a.5.5 0 01.5-.5h11a.5.5 0 010 1h-11a.5.5 0 01-.5-.5zm0-3a.5.5 0 01.5-.5h11a.5.5 0 010 1h-11a.5.5 0 01-.5-.5zm0-3a.5.5 0 01.5-.5h11a.5.5 0 010 1h-11a.5.5 0 01-.5-.5zm0-3a.5.5 0 01.5-.5h11a.5.5 0 010 1h-11a.5.5 0 01-.5-.5z" clipRule="evenodd"/>
            </svg>

        </button>
    )
}

export {LessonNavToggleButton}