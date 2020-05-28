// import React from 'react';

const PageNumButton = props => {

    const pageNumStyle = {
        backgroundColor: props.active ? '#ffd200' : '#c4c4c4',
        border: '0pt',
        marginTop: '20px',
        marginRight: '20px',
        marginBottom: '10px',
        borderRadius: '4px'
    };

    return React.createElement(
        'button',
        { style: pageNumStyle },
        props.num
    );
};

export { PageNumButton };