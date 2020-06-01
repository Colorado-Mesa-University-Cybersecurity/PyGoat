/*
File: lessonItem.jsx
Description: file exports the LessonItem React Component which implements the button that triggers a 
                change of the rendered html inside the LessonArea Component

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
 * LessonItem  ::  Object  ->  JSX
 * 
 * @param {'Object'} props 
 * 
 * Component is a button that controls the client's current lesson
 *      
 * Returns a JSX component
 */
const LessonItem = (props) => {


    const classNameIs = props.active? 'lesson-item': 'lesson-item hide'

    const currentLesson = props.current? 'current-lesson lesson-title': 'lesson-title'

    const lessonStyle = props.active?  {
        display: 'flex', 
        alignItems: 'center',
    }: {};

    const handleClick = (e) => {
        props.store.refresh.innerHTMLReRender(props.title) // Changes LessonArea
        if(props.store.checkActivePage().title != props.title){
            props.store.changeActivePage(props.title)
            props.store.refresh.rootReRender(Math.random()) // Changes LessonNavigator
        }
    }

    return (
        <div className={classNameIs} style={lessonStyle} id='lesson-item-title' onClick={handleClick}>
            <h2 className={currentLesson}>{props.title}</h2>
        </div>
    )
}

export {LessonItem}