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

        if (!localStorage.getItem('warehouse') == null) {
            this.warehouse = JSON.parse(localStorage.getItem('warehouse'));
        };

        this.storeLocally();

        // refresh is an object held that will hold references to methods used to update various components
        //   this is to make sure that any component that changes the app data can signal React to re-render the DOM
        //   allows components that change data to trigger a local and server storage update
        this.refresh = {}
        this.refresh.storeLocally = this.storeLocally.bind(this)

        // warehouse stores all of the data used by the react components
        this.warehouse || this.createWarehouse()

        // the parsedLessons object will hold all of the DOMs created from jinja templates fetched from the server
        this.parsedLessons = {}


        return this;
    };
    
    
    createWarehouse() {
        this.warehouse = {}
        this.warehouse.cache = {} // cache contains the html fetched from server in string form before parsing
        this.warehouse.navItems = [{group: 'Introduction', lessons: [{title: 'Welcome', url: '/welcome', current: true, group: 'Introduction', pages: 3, currentPage: 1}]}]
        this.warehouse.lessonMetaData = {lessonTitles: [], lessons: {}}
        this.warehouse.siteNav = [{title: 'Logout', active: false, pages: 1, currentPage: 1}, {title: 'Record', active: false, pages: 1, currentPage: 1}, {title: 'Contact Us', active: false, pages: 1, currentPage: 1}, {title: 'About', active: false, pages: 1, currentPage: 1}]

        this.addLesson = this.addLesson.bind(this);
    }


    checkActivePage() {
        const activeItem = [{}]
        this.warehouse.navItems.forEach((group, i) => {
            const activeLesson = group.lessons.filter((lesson, j) => {
                return lesson.current === true;
            });
            activeLesson[0] && (activeItem[0] = activeLesson[0]);
        });

        const activeSiteNavItem = this.warehouse.siteNav.filter((navItem, i) => {
            return navItem.active === true
        });
        activeSiteNavItem[0] && (activeItem[0] = activeSiteNavItem[0])

        return activeItem[0];
    };


    checkCurrentPageNumber() {
        return this.checkActivePage().currentPage;
    };

    checkNumberOfPages() {
        return Array(this.checkActivePage().pages).fill(0);
    };

    
    changeActivePage(title) {
        this.checkActivePage().current && (this.checkActivePage().current = false)
        this.checkActivePage().active && (this.checkActivePage().active = false)

        this.warehouse.siteNav.forEach((navItem, i) => {
            if(navItem.title == title) {
                navItem.active = true;
            }
        })
        
        this.warehouse.navItems.forEach((group, i) => {
            group.lessons.forEach((lesson, j) => {
                if(lesson.title == title) {
                    lesson.current = true;
                }
            })
        })

        return this;
    };


    changeCurrentPageNumber(pageNumber) {
        this.checkActivePage().currentPage = pageNumber;

        return this;
    };
    

    /**
     * addLesson  ::  {group: string, title: string, url: string} -> store object
     * 
     * Method checks the warehouse.navItem array for elements with the property group
     * 
     *      if an element's contains the same group property, push the lesson to 
     *          that element's lesson propery array
     * 
     *      if it no element contains the same group property, create a new element
     *          with a group property that matches the lesson.group property, then 
     *          create a lessons property with an array containing the new lesson 
     *          object as its only element
     * 
     * returns store object to allow method chaining
     */
    addLesson(lesson) {
        lesson.group || console.assert(false, 'lessons must have group property')
        lesson.title || console.assert(false, 'lesson must have title property')
        lesson.url || console.assert(false, 'lesson must have url property')
        lesson.pages || console.assert(false, 'lesson must have pages property')

        if(this.warehouse.lessonMetaData.lessonTitles.some((x)=> x === lesson.title)) {
            return this
        } else {
            this.warehouse.lessonMetaData.lessonTitles.push(lesson.title)
            this.warehouse.lessonMetaData.lessons[lesson.title] = lesson
        }
        
        const index = [0]
        const exists = this.warehouse.navItems.some((x, i) => {
            const test = x.group === lesson.group
            if(test) { index[0] = i }; // save the index of group that matches the lesson group
            return test
        })

        if (exists) { this.warehouse.navItems[index[0]].lessons.push(lesson) }
        else { 
            this.warehouse.navItems.push({group: lesson.group, lessons: []})
            this.warehouse.navItems[this.warehouse.navItems.length - 1].lessons.push(lesson) 
        }

        return this;
    }

    storeLocally() {
        localStorage.setItem('item', JSON.stringify(this.item))
        localStorage.setItem('warehouse', JSON.stringify(this.warehouse))
        return this;
    };
};



export {Store}