// import React from 'react';

const ResetLessonButton = props => {

    const resetStyle = {
        backgroundColor: '#333333',
        color: 'white',
        border: '0pt',
        marginTop: '20px',
        marginRight: '20px',
        marginBottom: '10px',
        borderRadius: '4px'
    };

    return React.createElement(
        'button',
        { style: resetStyle },
        'Reset Lesson'
    );
};

export { ResetLessonButton };