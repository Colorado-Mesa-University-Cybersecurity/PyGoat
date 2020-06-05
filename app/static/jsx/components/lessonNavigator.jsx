/*
File: lessonNavigator.jsx
Description: file exports the LessonNavigator React Component which implements the
                application's navigation sidebar. It is composed of the LessonGroup
                and LessonItem Components

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


import {LessonGroup} from './lessonGroup.js';
import {LessonItem} from './lessonItem.js';


'use strict'



/**
 * LessonNavigator  ::  Object  ->  JSX
 * 
 * @param {'Object'} props 
 * 
 * Component instantiates the sidebar and controls the state of the LessonGroup and LessonItem Components
 *      
 * Returns a JSX component
 */
const LessonNavigator = function(props){

    // Create a function hook to manage state and pass it to the child components
    const [activeGroup, setActiveGroup] = React.useState(['none'])
    
    const sideNavStyle = { width: props.width };

    if(!props.store.refresh.lessonNav) {
        props.store.refresh.lessonNav = {};
        props.store.refresh.lessonNav.setActiveGroup = setActiveGroup;
    };

    return (
        <div style={sideNavStyle} className='h100 flexIt themeColor2'>
            <div className='w100 lesson-selection-area'> 
                {props.groups.map((x, i) => 
                    <LessonGroup  title={x.group} active={activeGroup === i} setActive={setActiveGroup} id={`${x}_${i}`} num={i} key={`${x}_${i}`}>
                        {x.lessons && x.lessons.map((y, j) => 
                            <LessonItem title={y.title} key={`${y.title}__${j}`} current={y.current} active={activeGroup === i} completed={y.completed} store={props.store}/>
                        )}
                    </LessonGroup>
                )}
            </div>
        </div>
    )
};


export {LessonNavigator};