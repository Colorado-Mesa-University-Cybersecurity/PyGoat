// import React, {useState} from 'react'

const LessonGroup = (props) => {

    

    const groupStyle = {
        alignItems: 'center',
    }

    const arrowStyle = {
        marginLeft: 'auto',
        marginRight: 40,
    }

    const arrowShape = props.active? "M0 0 L20 0 L10 15 Z" : "M0 0 L15 10 L0 20 Z"

    const clickHandler = (e) => {
        const newState = props.active? 'none': props.num;
        props.setActive(newState)
    }

    return (
        <React.Fragment>
            <div style={groupStyle} className='lesson-group' onClick={clickHandler}>
                <h1>
                    {props.title}
                </h1>

                <div style={arrowStyle}>
                    <svg height="20" width="20">
                        <path d={arrowShape} />
                    </svg> 
                </div>

            </div>
            {props.children}
        </React.Fragment>
    )
}

export {LessonGroup}