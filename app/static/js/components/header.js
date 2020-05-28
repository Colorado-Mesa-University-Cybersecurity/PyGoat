// import React from 'react';

const GoatHeader = props => {

    const headerStyle = {
        display: 'flex',
        alignItems: 'center'
    };

    const blockStyle = {
        backgroundColor: '#333333',
        color: 'white',
        display: 'inline-block',
        height: props.height,
        width: '100%'
    };

    const titleStyle = {
        fontSize: '36pt',
        fontWeight: 'lightest'

    };

    const titleBoxStyle = {
        display: 'flex',
        paddingLeft: '60px',
        alignItems: 'center'
    };

    return React.createElement(
        'header',
        { style: blockStyle },
        React.createElement(
            'div',
            { style: headerStyle },
            React.createElement(
                'div',
                { style: { display: 'inline-block' } },
                props.children[0] /* The first child should be the Logo and Name of the App */
            ),
            React.createElement(
                'div',
                { style: titleBoxStyle },
                React.createElement(
                    'h1',
                    { style: titleStyle },
                    'Lesson/Page Title'
                )
            ),
            props.children[1] /* The second child should be the site navigation panel*/
        )
    );
};

export { GoatHeader };