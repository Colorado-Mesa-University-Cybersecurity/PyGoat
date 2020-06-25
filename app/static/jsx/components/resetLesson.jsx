/*
File: resetLesson.jsx
Description: file exports the ResetLessonButton React Component which implements the 
                application's lesson reset button. This allows users to repeat lessons

!!! Not completely functional

IMPORTANT!!! If you are reading this from within a .js file,   EXIT THE FILE!!!   Go to the jsx/components directory 
    and find resetLesson.jsx.  React is Transpiled from JSX, unless you are familiar with React, you will not
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



/**
 * ResetLessonButton  ::  Object  ->  JSX
 * 
 * @param {"Object"} props 
 * 
 * Component resets the lesson associated with the current page
 *      
 * Returns a JSX component
 */
export function ResetLessonButton(props) {

    const resetStyle = {
        backgroundColor: "#333333",
        color: "white",
        border: "0pt",
        marginTop: "20px",
        marginRight: "20px",
        marginBottom: "10px",
        borderRadius: "4px"
    };

    const handleClick = (e) => {
        console.log("clicked reset lesson button")
    };

    return (
        <button style={resetStyle} onClick={handleClick}>Reset Lesson</button>
    );
}

// Preferred: Use shorthand syntax for export (see above)
// export { ResetLessonButton }