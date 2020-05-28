// import React from 'react';

const LessonItem = (props) => {


    const classNameIs = props.active? 'lesson-item': 'lesson-item hide'

    const currentLesson = props.current? 'current-lesson': 'emptyClass'

    const lessonStyle = props.active?  {
        display: 'flex', 
        alignItems: 'center',
    }: {};

    const titleStyle = {
        paddingLeft: '50px'
    }

    return (
        <div className={classNameIs} style={lessonStyle} id='lesson-item-title'>
            <h2 style={titleStyle} className={currentLesson}>{props.title}</h2>
        </div>
    )
}

export {LessonItem}