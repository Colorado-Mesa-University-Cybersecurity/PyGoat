/*
File: store.js
Description: file exports Store class that holds and manages data and state for the React Components

Conventions followed:
    4-space tabs
    always place semicolons
    3 empty lines between classes and functions
    2 empty lines between methods
    Class methods always return this unless other return value desired
    Annotations follow the convention:     
            function/method  ::  (parameter types) -> (return types)
*/

'use strict'



/**
 * Class Store
 * 
 * Store instantiates a store object to contain and manage all of the data used by the PyGoat application
 * 
 * Methods:
 * 
 * 		constructor  ::  void  ->  store object
 *          method creates/instantiates the datastructures the app is dependant upon
 *              If persistent data is found, that data is used
 *          creates the refresh object
 *              object: refresh
 *                  holds references to individual component state functions to 
 *                      facilitate quick updates
 *         
 * 
 * 		storeLocally  ::  void  ->  store object
 *          method stores the state of all data structures to local storage
 */
class Store{
    constructor() {
        if (localStorage.getItem('item') == null) {
            this.item = 'hello world';
        } else {
            this.item = JSON.parse(localStorage.getItem('item'));
        };
        this.storeLocally();

        // refresh is an object held that will hold references to methods used to update various components
        // this is to make sure that any component that changes the app data can signal React to re-render the DOM
        // allows components that change data to trigger a local and server storage update
        this.refresh = {}
        this.refresh.storeLocally = this.storeLocally.bind(this)

        this.warehouse = {}
        this.warehouse.navItems = [{group: 'Introduction', lessons: [{title: 'Welcome', url: '/welcome', current: true, group: 'Introduction'}]}]
        this.addLesson = this.addLesson.bind(this);

        return this;
    };
    
    addLesson(lesson) {
        lesson.group || console.assert(false, 'lessons must have group property')
        lesson.title || console.assert(false, 'lesson must have title property')
        lesson.url || console.assert(false, 'lesson must have url property')

        const atIndex;
        const exists = this.warehouse.navItems.some((x, i) => {
            const test = x.group === lesson.group
            if(test){ atIndex = i};
            return test
        })

        if(exists) {
            this.warehouse.navItems[atIndex].lessons.push(lesson):
        } else {
            this.warehouse.navItems.push({group: lesson.group, lessons: lesson});
        }

        return this;
    }

    storeLocally() {
        localStorage.setItem('item', JSON.stringify(this.item))
        return this;
    };
};


	// 	{group: 'Introduction'}
	// 	// {group: 'Introduction', lessons: [{title: 'Lesson Title 1', current: false}, {title: 'Lesson Title 2', current: false}, {title: 'Lesson Title 3', current: false},]},
	// 	// {group: 'Lesson Group 2', lessons: [{title: 'Lesson Title 1', current: false}, {title: 'Lesson Title 2', current: false}, {title: 'Lesson Title 3', current: false},]},
	// 	// {group: 'Lesson Group 3', lessons: [{title: 'Lesson Title 1', current: true}, {title: 'Lesson Title 2', current: false}, {title: 'Lesson Title 3', current: false},]},
	// 	// {group: 'Lesson Group 4', lessons: [{title: 'Lesson Title 1', current: false}, {title: 'Lesson Title 2', current: false}, {title: 'Lesson Title 3', current: false},]},
	// 	// {group: 'Lesson Group 5', lessons: [{title: 'Lesson Title 1', current: false}, {title: 'Lesson Title 2', current: false}, {title: 'Lesson Title 3', current: false},]},
	// 	// {group: 'Lesson Group 6', lessons: [{title: 'Lesson Title 1', current: false}, {title: 'Lesson Title 2', current: false}, {title: 'Lesson Title 3', current: false},]},
	


export {Store}