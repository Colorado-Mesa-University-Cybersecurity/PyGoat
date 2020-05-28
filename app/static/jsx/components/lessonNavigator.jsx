// import React, { useState } from 'react';
import {LessonGroup} from './lessonGroup.js';
import {LessonItem} from './lessonItem.js'

const LessonNavigator = (props) => {

    const [activeGroup, setActiveGroup] = React.useState(['none'])

    const sideNavStyle = {
        width: props.width,
        backgroundColor: '#333333',
        height: '100%',
        display: 'flex'
    }

    const lessonSelectionStyle = {
        width: '100%',
        marginTop: '50px',
        // display: 'flex',
    }

    return (
        <div style={sideNavStyle}>
            <div style={lessonSelectionStyle}>
                {props.groups.map((x, i) => 
                    <LessonGroup  title={x.group} active={activeGroup === i} setActive={setActiveGroup} id={`${x}_${i}`} num={i} key={`${x}_${i}`}>
                        {x.lessons && x.lessons.map((y, j) => 
                            <LessonItem title={y.title} key={`${y.title}__${j}`} current={y.current} active={activeGroup === i} />
                        )}
                    </LessonGroup>
                    )}
            </div>
        </div>
    )
}

export {LessonNavigator}