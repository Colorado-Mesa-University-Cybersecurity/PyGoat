// import React from 'react';

const LessonItem = props => {

    const classNameIs = props.active ? 'lesson-item' : 'lesson-item hide';

    const currentLesson = props.current ? 'current-lesson' : 'emptyClass';

    const lessonStyle = props.active ? {
        display: 'flex',
        alignItems: 'center'
    } : {};

    const titleStyle = {
        paddingLeft: '50px'
    };

    const handleClick = e => {
        console.log('clicked Lesson nav button!', props.store.refresh.rootReRender);
        if (props.store.checkActivePage().title != props.title) {
            props.store.changeActivePage(props.title);
            props.store.refresh.rootReRender(Math.random());
        }
    };

    return React.createElement(
        'div',
        { className: classNameIs, style: lessonStyle, id: 'lesson-item-title', onClick: handleClick },
        React.createElement(
            'h2',
            { style: titleStyle, className: currentLesson },
            props.title
        )
    );
};

export { LessonItem };