// import React, {useState} from 'react'

const LessonGroup = props => {

    const groupStyle = {
        alignItems: 'center'
    };

    const arrowStyle = {
        marginLeft: 'auto',
        marginRight: 40
    };

    const arrowShape = props.active ? "M0 0 L20 0 L10 15 Z" : "M0 0 L15 10 L0 20 Z";

    const clickHandler = e => {
        const newState = props.active ? 'none' : props.num;
        props.setActive(newState);
    };

    return React.createElement(
        React.Fragment,
        null,
        React.createElement(
            'div',
            { style: groupStyle, className: 'lesson-group', onClick: clickHandler },
            React.createElement(
                'h1',
                null,
                props.title
            ),
            React.createElement(
                'div',
                { style: arrowStyle },
                React.createElement(
                    'svg',
                    { height: '20', width: '20' },
                    React.createElement('path', { d: arrowShape })
                )
            )
        ),
        props.children
    );
};

export { LessonGroup };