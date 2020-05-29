import { SVGLogo } from './components/logo.js';
import { GoatHeader } from './components/header.js';
import { SiteNavigator } from './components/siteNav.js';
import { SiteNavItem } from './components/siteNavItem.js';
import { LessonNavigator } from './components/lessonNavigator.js';
import { LessonArea } from './components/lessonArea.js';
import { LessonNavToggleButton } from './components/sideBarToggle.js';
import { ResetLessonButton } from './components/resetLesson.js';
import { PageNumButton } from './components/pageNumNav.js';

function App(props) {

	// React.useState() creates a state for the React component
	// 	the state variable is the state while the setNewState variable
	const [state, setNewState] = React.useState();
	const store = props.store;
	const format = props.format;
	store.refresh.rootReRender = setNewState;

	const numPages = store.checkNumberOfPages();
	const currentPage = store.checkCurrentPageNumber();
	const siteNavItems = store.warehouse.siteNav;
	const siteNavItemsLength = siteNavItems.length;

	const sidePanelClass = store.warehouse.hideSideBar ? 'lesson-navigator hide' : 'lesson-navigator';
	const sidePanelStyle = { width: format.sidebar.width };
	const lessonNavItems = store.warehouse.navItems;

	// React.useEffect runs supplied function once after component is rendered, 
	// 	and runs it whenever the value inside the array supplied in the second 
	//  is changed
	React.useEffect(() => {

		// if state has been given a non-zero value, fetch doesnt run
		// 	this ensures that it only runs once after initial component rendering
		state || fetch('/lessonstatus', { method: 'GET', 'Content-Type': 'application/json' }).then(d => d.json()).then(d => {
			Object.keys(d).forEach((x, i) => {
				const lesson = d[x];
				lesson.title = x;
				lesson.current = false;
				lesson.currentPage = 1;
				store.addLesson(lesson);
			});
			setNewState(1);
		});
	}, [state]);

	state || console.log('app loaded');
	state && console.log('app reloaded');

	return React.createElement(
		'div',
		null,
		React.createElement(
			GoatHeader,
			{ height: format.header.height },
			React.createElement(SVGLogo, { height: format.header.height, width: format.sidebar.width }),
			React.createElement(
				SiteNavigator,
				{ height: format.header.height },
				siteNavItems.map((x, i) => React.createElement(SiteNavItem, { key: `${x.title}_${i}`, height: `${100 / siteNavItemsLength}%`, title: x.title, active: x.active, store: store }))
			)
		),
		React.createElement(
			'main',
			null,
			React.createElement(
				'div',
				{ className: sidePanelClass, style: sidePanelStyle },
				React.createElement(LessonNavigator, { store: store, width: format.sidebar.width, groups: lessonNavItems })
			),
			React.createElement(
				'div',
				{ className: 'lesson-area' },
				React.createElement(
					LessonArea,
					null,
					React.createElement(LessonNavToggleButton, { setToggle: setNewState, warehouse: store.warehouse }),
					numPages.map((x, i) => React.createElement(PageNumButton, { num: i + 1, key: `${x}___${i}`, active: i + 1 === currentPage, store: store })),
					React.createElement(ResetLessonButton, null)
				)
			)
		)
	);
}

export { App };