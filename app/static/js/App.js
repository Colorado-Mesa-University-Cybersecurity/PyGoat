/*
File: App.jsx
Description: file exports the App React Component which is composed of all of the Project components to create the UI

IMPORTANT!!! If you are reading this from within a .js file, it is important to note that you should not 
	make any changes to that file if you wish to edit the PyGoat client, instead follow the directions on 
	the README.md contained within the static directory. Make sure any editing is done with the .jsx version
	of this file inside the static/jsx directory

Conventions followed:
    4-space tabs
    always place semicolons
    3 empty lines between classes and functions
    2 empty lines between methods
    Class methods always return this unless other return value desired
    Annotations follow the convention:     
            function/method  ::  (parameter types) -> (return types)
*/

import { SVGLogo } from './components/logo.js';
import { GoatHeader } from './components/header.js';
import { SiteNavigator } from './components/siteNav.js';
import { SiteNavItem } from './components/siteNavItem.js';
import { LessonNavigator } from './components/lessonNavigator.js';
import { LessonArea } from './components/lessonArea.js';
import { LessonNavToggleButton } from './components/sideBarToggle.js';
import { ResetLessonButton } from './components/resetLesson.js';
import { PageNumButton } from './components/pageNumNav.js';

'use strict';

/**
 * App  ::  Object  ->  JSX
 * 
 * @param {'Object'} props 
 * 
 * Component is composed of every individual component used to create the PyGoat client, the
 * 		props object must have an object passed in underneath the key store.
 * 
 * Returns a JSX component
 */
function App(props) {

	const store = props.store;
	const format = props.store.format;
	const currentPage = store.checkActivePage();

	// React.useState() creates a state for the React component
	// 	the state variable is the state while the setNewState variable
	//	is used to trigger a rerender the component
	const [state, setNewState] = React.useState();
	const [rendered, render] = React.useState('none');
	store.refresh.rootReRender = setNewState;
	store.refresh.innerHTMLReRender = render;

	const numPages = store.checkNumberOfPages();
	const currentPageNumber = store.checkCurrentPageNumber();
	const siteNavItems = store.warehouse.siteNav;
	const siteNavItemsLength = siteNavItems.length;
	const pageTitle = store.checkActivePage().title;

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
			if (d.state) {
				// console.log("the data is here")
				props.store.warehouse = JSON.parse(d.state);
			} else {
				console.log('data is ', d);
				Object.keys(d).forEach((x, i) => {
					const lesson = d[x];
					console.log('lesson=', lesson);
					lesson.title = x;
					lesson.current = false;
					lesson.currentPage = 1;
					store.addLesson(lesson);
				});
			}
			console.log('feedback: ', props.store.feedback);
			if (props.store.feedback !== 'None') {
				const page = props.store.checkActivePage();
				const feedbackType = page.completed ? 'complete' : 'feedback';
				props.store.warehouse.cache[`${page.title}_${feedbackType}`] = props.store.feedback;
			}
			fetch('/save', {
				method: 'POST',
				'Content-Type': 'application/json',
				body: JSON.stringify(props.store.warehouse)
			});
			setNewState(1);
			store.cacheLessonHTML();
		});
	}, [state]);

	// triggers a re render of the contents of LessonArea
	React.useEffect(() => {
		store.renderInnerPage();
	}, [rendered]);

	state || console.log('app loaded'); // runs before state is initialized
	state && console.log('app reloaded'); // runs after state is initialized

	// The layout is flat because most transitions outside of the navbar require the entire app to be rerendered 
	return React.createElement(
		'div',
		null,
		React.createElement(
			GoatHeader,
			{ height: format.header.height, title: pageTitle },
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
					{ store: store },
					React.createElement(LessonNavToggleButton, { setToggle: setNewState, warehouse: store.warehouse }),
					numPages.map((x, i) => React.createElement(PageNumButton, { num: i + 1, key: `${x}___${i}`, active: i + 1 === currentPageNumber, store: store })),
					React.createElement(ResetLessonButton, null)
				)
			)
		)
	);
};

export { App };