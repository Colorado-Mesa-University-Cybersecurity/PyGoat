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
        console.log('hello world', props.store.hideSideBar, props)
        props.store.hideSideBar = props.store.hideSideBar? false: true;
        console.log('hello world', props.store.hideSideBar, props)
        props.setToggle(Math.random())

        // const reqOptions = {
        //     method: 'GET',
        //     headers: {'Content-Type': 'text/html'}
        // }
        // const newData = ''
        // fetch('/lesson/Worlddd', reqOptions)
        //     .then(response =>{
        //         const vals = response.text()
        //         console.log('vals', vals)
        //         console.log('response', response)
        //         return vals})
        //     .then(data => {
        //         console.log('data', data)
        //         return data.body.getReader()
        //     })
        //     .then(body => {
        //         console.log('data1', body)
        //         // body.releaseLock()
        //         // console.log(body.read())
        //         console.log('data2', body)
        //         return body.read()
        //     })
        //     .then(body => {
        //         console.log('data', body)
        //         return body
        //     })
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