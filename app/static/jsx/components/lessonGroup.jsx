/*
File: lessonGroup.jsx
Description: file exports the LessonGroup React Component which implements a group button 
                composed of toggleable internal LessonItem buttons

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


/**
 * LessonArea  ::  Object  ->  JSX
 * 
 * @param {'Object'} props 
 * 
 * Component houses all of individual LessonItem components that change the rendered lesson
 *      
 * Returns a JSX component
 */
const LessonGroup = (props) => {

    const groupStyle = { alignItems: 'center' }

    const arrowStyle = {
        marginLeft: 'auto',
        marginRight: 40,
    }

    // This is the code that controls the direction the arrow points 
    //      points down if active, to the side if not
    const arrowShape = props.active? "M0 0 L20 0 L10 15 Z" : "M0 0 L15 10 L0 20 Z";

    // triggers the parent component to toggle the actve LessonGroup buttton
    //      Only one can be active at a time, if the active one is clicked,
    //      none of the LessonGroup components are active
    const clickHandler = (e) => {
        const newState = props.active? 'none': props.num;
        props.setActive(newState)
    }

    return (
        <React.Fragment>
            <div style={groupStyle} className='lesson-group' onClick={clickHandler}>
                <h3>
                    {props.title}
                </h3>

                <div style={arrowStyle}>
                    <svg height="20" width="20">
                        <path d={arrowShape} />
                    </svg> 
                </div>

            </div>
            {props.children /* These are individual components that get displayed when the state of the component is active */}
        </React.Fragment>
    )
}


export {LessonGroup}