// import React from 'react';

const ResetLessonButton = (props) => {

    const resetStyle = {
        backgroundColor: '#333333',
        color: 'white',
        border: '0pt',
        marginTop: '20px',
        marginRight: '20px',
        marginBottom: '10px',
        borderRadius: '4px',
    }

    const handleClick = (e) => {
        console.log('clicked reset lesson button')
    }

    return (
        <button style={resetStyle} onClick={handleClick}>Reset Lesson</button>
    )
}

export {ResetLessonButton}