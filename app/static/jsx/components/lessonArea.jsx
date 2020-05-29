// import React from 'react';

const LessonArea = (props) => {

    const pageNavStyle = {
        display: 'inline-block',
        width: '100%'
    }

    const innerNavStyle = {
        display: 'flex'
    }

    // because I cannot use the ... spread operator in JSX, I need to incorporate the first and 
    // third elements into the array and render that to keep them all in the same line
    const pageNav = props.children[1].map(x => x)
        pageNav.unshift(props.children[0])
        pageNav.push(props.children[2])

    return (
        <div id='inner-lesson-area'>
            <div style={pageNavStyle} id='page-nav'>
                <div style={innerNavStyle} id='inner-page-nav'>
                    {pageNav}
                </div>
                <hr/>
                <div className="renderHTML"></div>
            </div>
        </div>
    )
}

export {LessonArea}