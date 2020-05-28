// import React, { useState } from 'react';
import { LessonGroup } from './lessonGroup.js';
import { LessonItem } from './lessonItem.js';

const LessonNavigator = props => {

    const [activeGroup, setActiveGroup] = React.useState(['none']);

    const sideNavStyle = {
        width: props.width,
        backgroundColor: '#333333',
        height: '100%',
        display: 'flex'
    };

    const lessonSelectionStyle = {
        width: '100%',
        marginTop: '50px'
        // display: 'flex',
    };

    return React.createElement(
        'div',
        { style: sideNavStyle },
        React.createElement(
            'div',
            { style: lessonSelectionStyle },
            props.groups.map((x, i) => React.createElement(
                LessonGroup,
                { title: x.group, active: activeGroup === i, setActive: setActiveGroup, id: `${x}_${i}`, num: i, key: `${x}_${i}` },
                x.lessons.map((y, j) => React.createElement(LessonItem, { title: y.title, key: `${y.title}__${j}`, current: y.current, active: activeGroup === i }))
            ))
        )
    );
};

export { LessonNavigator };