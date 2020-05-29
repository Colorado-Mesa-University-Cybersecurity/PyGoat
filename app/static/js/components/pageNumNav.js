// import React from 'react';

const PageNumButton = props => {

    const currentPage = props.store.checkActivePage();

    const pageNumStyle = {
        backgroundColor: props.active ? '#ffd200' : '#c4c4c4',
        border: '0pt',
        marginTop: '20px',
        marginRight: '20px',
        marginBottom: '10px',
        borderRadius: '4px'
    };

    const handleClick = e => {
        console.log('clicked page nav button, current page number:', props.num);
        console.log(props.store.checkCurrentPageNumber());
        console.log(props.store.checkActivePage());
        if (props.store.checkCurrentPageNumber() != props.num) {
            props.store.changeCurrentPageNumber(props.num);
            console.log(props.store.checkCurrentPageNumber());
            props.store.refresh.rootReRender(Math.random());
        }
    };

    return React.createElement(
        'button',
        { style: pageNumStyle, onClick: handleClick },
        props.num
    );
};

export { PageNumButton };