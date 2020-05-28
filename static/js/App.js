// import React, { useState } from 'react';
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

	const model = props.model;
	console.log(1);
	const [state, setNewState] = React.useState();
	console.log(2);

	const format = {};
	format.header = {
		height: '120px',
		width: '100%'
	};

	format.sidebar = {
		minHeight: '20rem',
		width: '300px'
	};

	const sidePanelStyle = {
		width: format.sidebar.width
	};

	const sidePanelClass = model.store.hideSideBar ? 'lesson-navigator hide' : 'lesson-navigator';

	const numPages = Array(4).fill(0);
	const currentPage = 1;

	const navItems = ['Logout', 'Record', 'Contact Us', 'About'];

	const navItemsLength = navItems.length;

	const lessonNavItems = [{ group: 'Introduction', lessons: [{ title: 'Lesson Title 1', current: false }, { title: 'Lesson Title 2', current: false }, { title: 'Lesson Title 3', current: false }] }, { group: 'Lesson Group 2', lessons: [{ title: 'Lesson Title 1', current: false }, { title: 'Lesson Title 2', current: false }, { title: 'Lesson Title 3', current: false }] }, { group: 'Lesson Group 3', lessons: [{ title: 'Lesson Title 1', current: true }, { title: 'Lesson Title 2', current: false }, { title: 'Lesson Title 3', current: false }] }, { group: 'Lesson Group 4', lessons: [{ title: 'Lesson Title 1', current: false }, { title: 'Lesson Title 2', current: false }, { title: 'Lesson Title 3', current: false }] }, { group: 'Lesson Group 5', lessons: [{ title: 'Lesson Title 1', current: false }, { title: 'Lesson Title 2', current: false }, { title: 'Lesson Title 3', current: false }] }, { group: 'Lesson Group 6', lessons: [{ title: 'Lesson Title 1', current: false }, { title: 'Lesson Title 2', current: false }, { title: 'Lesson Title 3', current: false }] }];

	console.log('app reloaded');
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
				navItems.map((x, i) => React.createElement(SiteNavItem, { key: `${x}_${i}`, height: `${100 / navItemsLength}%`, title: x }))
			)
		),
		React.createElement(
			'main',
			null,
			React.createElement(
				'div',
				{ className: sidePanelClass, style: sidePanelStyle },
				React.createElement(LessonNavigator, { width: format.sidebar.width, groups: lessonNavItems })
			),
			React.createElement(
				'div',
				{ className: 'lesson-area' },
				React.createElement(
					LessonArea,
					null,
					React.createElement(LessonNavToggleButton, { setToggle: setNewState, store: model.store }),
					numPages.map((x, i) => React.createElement(PageNumButton, { num: i + 1, key: `${x}___${i}`, active: i + 1 === currentPage })),
					React.createElement(ResetLessonButton, null)
				)
			)
		)
	);
}

export { App };