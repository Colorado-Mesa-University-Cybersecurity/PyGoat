// import React from 'react';

const SiteNavItem = props => {

    const navItemStyle = {
        height: props.height
    };

    return React.createElement(
        'button',
        { className: 'site-nav-item', style: navItemStyle },
        React.createElement(
            'h3',
            null,
            props.title
        )
    );
};

export { SiteNavItem };