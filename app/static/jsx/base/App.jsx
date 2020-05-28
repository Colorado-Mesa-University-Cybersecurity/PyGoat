// import React, { useState } from 'react';
import {SVGLogo} from './components/logo.js'
import {GoatHeader} from './components/header.js'
import {SiteNavigator} from './components/siteNav.js'
import {SiteNavItem} from './components/siteNavItem.js'
import {LessonNavigator} from './components/lessonNavigator.js'
import {LessonArea} from './components/lessonArea.js'
import {LessonNavToggleButton} from './components/sideBarToggle.js'
import {ResetLessonButton} from './components/resetLesson.js'
import {PageNumButton} from './components/pageNumNav.js'

 
function App(props) {

	const model = props.model
	console.log(1)
	const [state, setNewState] = React.useState()
	console.log(2)
	
	const format = {}
	format.header = {
		height: '120px',
		width: '100%'
	}

	format.sidebar = {
		minHeight: '20rem',
		width: '300px'
	}

	const sidePanelStyle = { 
		width: format.sidebar.width
	}

	const sidePanelClass = model.store.hideSideBar? 'lesson-navigator hide': 'lesson-navigator';

	const numPages = Array(4).fill(0)
	const currentPage = 1

	const navItems = ['Logout', 'Record', 'Contact Us', 'About']

	const navItemsLength = navItems.length

	const lessonNavItems = [
		{group: 'Introduction', lessons: [{title: 'Lesson Title 1', current: false}, {title: 'Lesson Title 2', current: false}, {title: 'Lesson Title 3', current: false},]},
		{group: 'Lesson Group 2', lessons: [{title: 'Lesson Title 1', current: false}, {title: 'Lesson Title 2', current: false}, {title: 'Lesson Title 3', current: false},]},
		{group: 'Lesson Group 3', lessons: [{title: 'Lesson Title 1', current: true}, {title: 'Lesson Title 2', current: false}, {title: 'Lesson Title 3', current: false},]},
		{group: 'Lesson Group 4', lessons: [{title: 'Lesson Title 1', current: false}, {title: 'Lesson Title 2', current: false}, {title: 'Lesson Title 3', current: false},]},
		{group: 'Lesson Group 5', lessons: [{title: 'Lesson Title 1', current: false}, {title: 'Lesson Title 2', current: false}, {title: 'Lesson Title 3', current: false},]},
		{group: 'Lesson Group 6', lessons: [{title: 'Lesson Title 1', current: false}, {title: 'Lesson Title 2', current: false}, {title: 'Lesson Title 3', current: false},]},
	]

	console.log('app reloaded')
	return (
		<div >
			{/* This is the Header */}
			<GoatHeader height={format.header.height} >
				<SVGLogo height={format.header.height} width={format.sidebar.width}/>
				<SiteNavigator height={format.header.height}>
					{navItems.map((x, i)=><SiteNavItem key={`${x}_${i}`} height={`${100/navItemsLength}%`} title={x} />)}
				</SiteNavigator>
			</GoatHeader> 

			<main>
				{/* This is the Side Panel */}
				<div className={sidePanelClass} style={sidePanelStyle}>
					<LessonNavigator width={format.sidebar.width} groups={lessonNavItems} />
				</div>


				{/* This is Page Contents */}
				<div className='lesson-area'>
					<LessonArea>
						<LessonNavToggleButton setToggle={setNewState} store={model.store} />
						{numPages.map((x, i) => <PageNumButton num={i+1} key={`${x}___${i}`} active={(i+1) === currentPage}/>)}
						<ResetLessonButton />
					</LessonArea>
				</div>
			</main>
		</div>
	);
}

export {App};
