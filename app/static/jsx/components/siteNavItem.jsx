
const SiteNavItem = (props) => {

    const navItemStyle = {
        height: props.height,
        // backgroundColor: props.active? '#860037': 'ffd200',
        // color: props.active? 'white': 'black',
    }

    const navClass = props.active? 'site-nav-item-active' :'site-nav-item'

    const handleClick = (e) => {
        props.store.refresh.innerHTMLReRender(props.title)
        if(props.store.checkActivePage().title != props.title && props.title != 'Logout') {
            props.store.changeActivePage(props.title)
            props.store.refresh.rootReRender(Math.random())
        } else if (props.title == 'Logout') {
            window.location.href = 'logout'
        }
    }

    return (
        <button className={navClass} style={navItemStyle} onClick={handleClick}>
            <h3>{props.title}</h3>
        </button>
    )
}

export {SiteNavItem}