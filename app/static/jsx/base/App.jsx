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


import {SVGLogo} from './components/logo.js'
import {GoatHeader} from './components/header.js'
import {SiteNavigator} from './components/siteNav.js'
import {SiteNavItem} from './components/siteNavItem.js'
import {LessonNavigator} from './components/lessonNavigator.js'
import {LessonArea} from './components/lessonArea.js'
import {LessonNavToggleButton} from './components/sideBarToggle.js'
import {ResetLessonButton} from './components/resetLesson.js'
import {PageNumButton} from './components/pageNumNav.js'


'use strict'



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

	const store = props.store
	const format = props.store.format
	const currentPage = store.checkActivePage();

	// React.useState() creates a state for the React component
	// 	the state variable is the state while the setNewState variable
	//	is used to trigger a rerender the component
	const [state, setNewState] = React.useState()
	const [rendered, render] = React.useState('none')
	store.refresh.rootReRender = setNewState;
	store.refresh.innerHTMLReRender = render;
	
	const numPages = store.checkNumberOfPages()
	const currentPageNumber = store.checkCurrentPageNumber();
	const siteNavItems = store.warehouse.siteNav
	const siteNavItemsLength = siteNavItems.length
	const pageTitle = store.checkActivePage().title

	const sidePanelClass = store.warehouse.hideSideBar? 'lesson-navigator hide': 'lesson-navigator';
	const sidePanelStyle = { width: format.sidebar.width }
	const lessonNavItems = store.warehouse.navItems

	// React.useEffect runs supplied function once after component is rendered, 
	// 	and runs it whenever the value inside the array supplied in the second 
	//  is changed
	React.useEffect(()=> {

		// if state has been given a non-zero value, fetch doesnt run
		// 	this ensures that it only runs once after initial component rendering
		state || fetch('/lessonstatus', { method: 'GET', 'Content-Type': 'application/json' }).then(d => d.json()).then(d => {
			if(d.state) {
				// console.log("the data is here")
				props.store.warehouse = JSON.parse(d.state)
			} else {
				// console.log('data is ', d)
				Object.keys(d).forEach((x, i) => {
					const lesson = d[x];
					// console.log('lesson=', lesson);
					lesson.title = x;
					lesson.current = false;
					lesson.currentPage = 1;
					store.addLesson(lesson);
				});
			}
			setNewState(1);
			store.cacheLessonHTML();
		});
	}, [state]);

	// triggers a re render of the contents of LessonArea
	React.useEffect(()=>{
		store.renderInnerPage()

	}, [rendered])

	// 	store.renderArea || (store.renderArea = document.querySelector('.renderHTML'))
	// 	console.log('rendered=', rendered)
	// 	if(store.renderArea) {
	// 		store.renderArea.innerHTML = ''
	// 		store.renderArea.append(store.parsedHTML[currentPage.title].querySelector(`.page${currentPageNumber}`))
	// 	}
	// console.log('loaded parsed HTML')

	state || console.log('app loaded')   // runs before state is initialized
	state && console.log('app reloaded') // runs after state is initialized

	// The layout is flat because most transitions outside of the navbar require the entire app to be rerendered 
	return (
		<div >
			{/* This is the Header */}
			<GoatHeader height={format.header.height} title={pageTitle}>
				<SVGLogo height={format.header.height} width={format.sidebar.width}/>
				<SiteNavigator height={format.header.height}>
					{siteNavItems.map((x, i)=><SiteNavItem key={`${x.title}_${i}`} height={`${100/siteNavItemsLength}%`} title={x.title} active={x.active} store={store}/>)}
				</SiteNavigator>
			</GoatHeader> 

			<main>
				{/* This is the Side Panel */}
				<div className={sidePanelClass} style={sidePanelStyle}>
					<LessonNavigator store={store} width={format.sidebar.width} groups={lessonNavItems} />
				</div>


				{/* This is Page Contents */}
				<div className='lesson-area'>
					<LessonArea>
						<LessonNavToggleButton setToggle={setNewState} warehouse={store.warehouse} />
						{numPages.map((x, i) => <PageNumButton num={i+1} key={`${x}___${i}`} active={(i+1) === currentPageNumber} store={store}/>)}
						<ResetLessonButton />
					</LessonArea>
				</div>
			</main>
		</div>
	);
};


export {App};
