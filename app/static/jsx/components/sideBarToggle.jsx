// import React from 'react';

const LessonNavToggleButton = (props) => {

    const lessonToggleStyle = {
        backgroundColor: '#333333',
        border: '0pt',
        marginLeft: '20px',
        marginTop: '20px',
        marginRight: '20px',
        marginBottom: '10px',
        paddingTop: '5px',
        borderRadius: '4px',
    }

    const handleClick = (e) => {
        props.warehouse.hideSideBar = props.warehouse.hideSideBar? false: true;
        props.setToggle(Math.random())
    }

    return (
        <button style={lessonToggleStyle} onClick={handleClick}>
            <svg width="1em" height="1em" viewBox="0 0 20 20" fill="#333333" >
                <path fill='#eeeeee' fillRule="evenodd" d="M4 14.5a.5.5 0 01.5-.5h11a.5.5 0 010 1h-11a.5.5 0 01-.5-.5zm0-3a.5.5 0 01.5-.5h11a.5.5 0 010 1h-11a.5.5 0 01-.5-.5zm0-3a.5.5 0 01.5-.5h11a.5.5 0 010 1h-11a.5.5 0 01-.5-.5zm0-3a.5.5 0 01.5-.5h11a.5.5 0 010 1h-11a.5.5 0 01-.5-.5z" clipRule="evenodd"/>
            </svg>

        </button>
    )
}

export {LessonNavToggleButton}