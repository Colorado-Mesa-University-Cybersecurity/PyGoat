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
 *      createWarehouse  ::  Void  ->  store object
 * 
 *      cacheSiteNavHTML  ::  Void  ->  store object
 * 
 *      cacheLessonHTML  ::  Void  ->  store object
 * 
 *      checkActivePage  ::  Void  ->  {title: String, group: String, current/active: Boolean, pages: Number, currentPage: Number}
 * 
 *      checkCurrentPageNumber  ::  Void  ->  Number
 * 
 *      checkNumberOfPages  ::  Void  ->  Number
 * 
 *      changeActivePage  ::  String  ->  store object
 * 
 *      changeCurrentPageNumber  ::  Number  ->  store object
 * 
 *      getID  ::  Void  ->  Void
 * 
 *      addLesson  ::  {group: string, title: string, url: string} -> store object
 * 
 *      parseHTML  ::  (String, String)  ->  store object
 * 
 *      renderInnerPage  ::  Void  ->  store object
 * 
 *      storeLocally  ::  Void  -> storeObject
 * 
 * 
 */
export class Store {
    constructor() {
        // the getID function will fetch the user's 'unique' id to use to store page state
        this.getID();
        if (!this.id) this.id = "None";
        console.log(localStorage.getItem(this.id));

        this.getFeedback();
        if (!this.feedback) this.feedback = "None";

        // the parsedHTML object will hold all of the DOMs created from jinja templates fetched from the server
        // the DOMParser object is used to transformed cached html from the server into a DOM object without 
        //      rendering the cached html. The new DOMs are indexed by page name and pages are extracted from
        //      the parsedHTML object by using .queryselector on the DOM 
        this.parser = new DOMParser();
        this.parsedHTML = {};

        // 'item' is in local storage for bug testing PyGoats ability to persist state
        if (localStorage.getItem("item") == null) this.item = "hello world";
        else this.item = JSON.parse(localStorage.getItem("item"));

        // If id exists in localStorage, reinstantiate the store object's "warehouse" 
        //      which contains the applications state
        if (localStorage.getItem(this.id) != null && localStorage.getItem(this.id) != "undefined") {
            this.warehouse = JSON.parse(localStorage.getItem(this.id));
            Object.keys(this.warehouse.cache).forEach((x) => {
                this.parseHTML(x, this.warehouse.cache[x]);
            });
            this.addLesson = this.addLesson.bind(this);
        };

        // refresh is an object held that will hold references to methods used to update various components
        //   this is to make sure that any component that changes the app data can signal React to re-render the DOM
        //   allows components that change data to trigger a local and server storage update
        this.refresh = {};
        this.refresh.storeLocally = this.storeLocally.bind(this);

        // warehouse stores all of the data used by the react components
        if (!this.warehouse) this.createWarehouse();

        // initial inner page area state
        this.currentlyRenderedHTML = "none";
        this.currentlyRenderedPageNumber = "none";

        // store client state using local storage, server storage is updated upon 
        //      interaction with lessons contained in the inner page area
        this.storeLocally();

        return this;
    };


    /**
     * createWarehouse  ::  Void  ->  store object
     * 
     * Method creates the warehouse object and sets its initial state as well as 
     *      triggering a fetch for the clients site navigation pages to cache.
     *      Also binds the functions that operate on the warehouse object
     * 
     * Returns this to enable method chaining
     */
    createWarehouse() {
        this.warehouse = {};
        this.warehouse.cache = {}; // cache contains the html fetched from server in string form before parsing
        this.warehouse.navItems = [
            {
                group: "Introduction",
                lessons: [
                    {
                        title: "Welcome",
                        url: "welcome",
                        current: true,
                        group: "Introduction",
                        pages: 3,
                        currentPage: 1,
                        completed: false,
                        completable: false
                    }
                ]
            }
        ];
        this.warehouse.lessonMetaData = {
            lessonTitles: [],
            lessons: {}
        };
        this.warehouse.siteNav = [
            {
                title: "Logout",
                active: false,
                pages: 1,
                currentPage: 1,
                url: "logout"
            },
            {
                title: "Report",
                active: false,
                pages: 1,
                currentPage: 1,
                url: "report"
            },
            {
                title: "About",
                active: false,
                pages: 1,
                currentPage: 1,
                url: "about"
            },
            /*{
                title: "Contact Us",
                active: false,
                pages: 1,
                currentPage: 1,
                url: "contactUs"
            }*/
            {
                title: "Create Lesson",
                active: false,
                pages: 1,
                currentPage: 1,
                url: "createLesson"
            }
        ];

        this.addLesson = this.addLesson.bind(this);

        this.cacheSiteNavHTML();

        return this;
    }


    /**
     * cacheSiteNavHTML  ::  Void  ->  store object
     * 
     * Method fetches html for the top right site navigation bar from the server and
     *      stores it as a string within this.warehouse.cache. It then calls the parseHTML 
     *      method to create and stash a document object based upon that html cache
     * 
     * Returns this to allow for method chaining
     */
    cacheSiteNavHTML() {
        this.warehouse.siteNav.forEach(async (item) => {
            if (item.title === "Logout") return; // renders no page for logout screen, user will be redirected to login screen
            const URL = `/nav/${item.url}`;
            let htmlString = await (await fetch(URL, {method: "GET", "Content-Type": "text/html"})).text();
            this.warehouse.cache[item.title] = htmlString;
            this.parseHTML(item.title, htmlString);
                /*
                NOTE: async/await preferred over .then() to promote clearer code flow.
                
                .then(d => d.text())  // promise chains are used due to the asynchronous nature of fetching server data
                .then(htmlString => {
                    this.warehouse.cache[item.title] = htmlString;
                    this.parseHTML(item.title, htmlString);
                });*/
        });

        return this;
    }


    /**
     * cacheLessonHTML  ::  Void  ->  store object
     * 
     * Method fetches lesson html templates prerendered by the server and stores their HTML
     *      within this.warehouse.cache. Calls parseHTML method to store DOM objects created
     *      from the server rendered jinja templates and stores them inside the this.parsedHTML object
     * 
     * Returns this to allow for method chaining
     */
    cacheLessonHTML() {
        this.warehouse.navItems.forEach((group, i) => {
            group.lessons.forEach(async (lesson, j) => {
                let URL;
                if (lesson.title == "Welcome") URL = `/nav/${lesson.url}`;
                else URL = `/lessons/${lesson.url}`;

                console.log("the store cache", lesson.title);

                let htmlString = await (await fetch(URL, {method: "GET", "Content-Type": "text/html"})).text();
                this.parseHTML(lesson.title, htmlString);
                this.warehouse.cache[lesson.title] = htmlString;
                if (!this.renderArea) this.renderArea = document.querySelector(".renderHTML");
                //this.renderArea || (this.renderArea = document.querySelector(".renderHTML")) || console.log("cannot grab render area yet");
                if (!this.feedbackArea) this.feedbackArea = document.querySelector(".renderResultHTML");
                //this.feedbackArea || (this.feedbackArea = document.querySelector(".renderResultHTML"));
                this.refresh.innerHTMLReRender(Math.random());
                    /*
                    NOTE: async/await preferred over .then() to promote clearer code flow.
                    
                    .then(d => d.text())
                    .then(htmlString => {
                        this.parseHTML(lesson.title, htmlString);
                        this.warehouse.cache[lesson.title] = htmlString;
                        this.renderArea || (this.renderArea = document.querySelector(".renderHTML")) || console.log("cannot grab render area yet");
                        this.feedbackArea || (this.feedbackArea = document.querySelector(".renderResultHTML"));
                        this.refresh.innerHTMLReRender(Math.random());
                    });*/
            });
        });

        return this;
    }

    /**
     * checkActivePage  ::  Void  ->  {title: String, group: String, current/active: Boolean, pages: Number, currentPage: Number}
     * 
     * Method checks the warehouse navItems for a single page object that has a property of current or a active with a value of true
     * 
     * Returns the page object with a current/active property of true
     */
    checkActivePage() {
        let activeItem = {}; // empty object is given so that the inner objects reference can be replace instead of pushing to the array
        this.warehouse.navItems.forEach((group) => {
            const activeLesson = group.lessons.filter((lesson) => lesson.current === true);
            if (activeLesson[0]) activeItem = activeLesson[0];
        });

        const activeSiteNavItem = this.warehouse.siteNav.filter((navItem) => navItem.active === true);
        if (activeSiteNavItem[0]) activeItem = activeSiteNavItem[0];

        return activeItem;
    };


    /**
     * checkCurrentPageNumber  ::  Void  ->  Number
     * 
     * Method returns the page number the client should render 
     */
    checkCurrentPageNumber() {
        return this.checkActivePage().currentPage;
    };


    /**
     * checkNumberOfPages  ::  Void  ->  Number
     * 
     * Method returns the total number of pages for the current lesson being displayed
     *      It is used to determine how many page navigation buttons to spawn
     */
    checkNumberOfPages() {
        return Array(this.checkActivePage().pages).fill(0);
    };


    /**
     * changeActivePage  ::  String  ->  store object
     * 
     * @param {string} title 
     * 
     * Method takes a page title and searches the warehouse for objects that have a matching title property
     *      Takes the object with a matching title quality and changes its current property to true
     *      This is used to change the page when react re-renders after a page navigation item is clicked
     * 
     * Returns this to facilitate method chaining
     */
    changeActivePage(title) {
        if (this.checkActivePage().current) this.checkActivePage().current = false;
        if (this.checkActivePage().active) this.checkActivePage().active = false;

        for (let navItem of this.warehouse.siteNav) if (navItem.title == title) navItem.active = true;

        for (let group of this.warehouse.navItems) for (let lesson of group.lessons) if (lesson.title == title) lesson.current = true;

        this.storeLocally();

        return this;
    };


    /**
     * changeCurrentPageNumber  ::  Number  ->  store object
     * 
     * @param {number} pageNumber 
     * 
     * Method takes a number and changes the current page property of the object returned
     *      by the checkActivePage method to match the number given. 
     *      This is used by the page navigation to change what page a user is looking at within a lesson
     * 
     * Returns this to allow for method chaining
     */
    changeCurrentPageNumber(pageNumber) {
        this.checkActivePage().currentPage = pageNumber;
        this.storeLocally();

        return this;
    };

    getFeedback() {
        // Thoughts on shorter syntax?
        //const feedbackArea = document.getElementById("feedback");
        this.feedback = document.getElementById("feedback").innerHTML;
        return this;
    }


    /**
     * getID  ::  Void  ->  Void
     * 
     * Method takes no parameters and returns no output values. Checks the page for an element
     *      with an id of id, this.id is set to the innerText of that element, and that element
     *      has its innerText rewritten to nothing
     * 
     * This Method is technically insecure, which would be bad in the context of any other 
     *      web application, but since this is a Purposefully Insecure web application meant to
     *      teach students what NOT to do, this could be seen as more of a feature than a vulnerability
     */
    getID() {
        const idArea = document.getElementById("id");
        this.id = idArea.innerText;
        idArea.innerText = "";
    }


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
        lesson.group || console.assert(false, "lessons must have group property");
        lesson.title || console.assert(false, "lesson must have title property");
        lesson.url || console.assert(false, "lesson must have url property");
        lesson.pages || console.assert(false, "lesson must have pages property");

        if (this.warehouse.lessonMetaData.lessonTitles.some((x) => x === lesson.title)) return this;
        else {
            this.warehouse.lessonMetaData.lessonTitles.push(lesson.title);
            this.warehouse.lessonMetaData.lessons[lesson.title] = lesson;
        }

        const found = this.warehouse.navItems.find((x) => {
            const test = x.group === lesson.group;
            return test;
        });

        if (found) found.lessons.push(lesson);
        else {
            this.warehouse.navItems.push({group: lesson.group, lessons: []});
            this.warehouse.navItems[this.warehouse.navItems.length - 1].lessons.push(lesson);
        }

        // this.cacheLessonHTML()

        return this;
    }


    /**
     * parseHTML  ::  (String, String)  ->  store object
     * 
     * @param {string} title 
     * @param {string} htmlString 
     * 
     * Method takes a title and an html string and parses the html string into a DOM object
     *      it then stores that DOM object with this.parsedHTML using the supplied title
     *      as the key
     * 
     * Returns this to allow for method chaining
     */
    parseHTML(title, htmlString) {
        this.parsedHTML[title] = this.parser.parseFromString(htmlString, "text/html");

        return this;
    }


    /**
     * renderInnerPage  ::  Void  ->  store object
     * 
     * Method swaps out the page being displayed inside the lesson area, first it destroys the 
     *      contents of the lessons area then the this.parsedHTML object has a node of a dom 
     *      matching the new page pulled out and appended to the display area. it then re-renders
     *      a new DOM object using the parseHTML method to replace the node that was pulled out
     * 
     * Returns this to allow for method chainings
     */
    renderInnerPage() {
        if (!this.renderArea) return this;
        const page = this.checkActivePage();
        const pageTitle = page.title;

        const feedbackName = page.completed ? `${page.title}_complete` : `${page.title}_feedback`;
        if (!this.parsedHTML[pageTitle]) return this;
        if (this.currentlyRenderedHTML == pageTitle && page.currentPage == this.currentlyRenderedPageNumber) return this;

        this.renderArea.innerHTML = "";
        if (
            this.renderArea.append(this.parsedHTML[pageTitle].querySelector(`.page${page.currentPage}`))
        ) console.log("append ran");
        this.parseHTML(page.title, this.warehouse.cache[page.title]);
        this.currentlyRenderedHTML = pageTitle;
        this.currentlyRenderedPageNumber = page.currentPage;

        console.log("the are we are in: ", this.warehouse.cache[feedbackName]); // What on earth is this?
        console.log(Object.keys(this.warehouse.cache));

        this.feedbackArea.innerHTML = "";

        if (this.warehouse.cache[feedbackName]) {
            this.parseHTML(feedbackName, this.warehouse.cache[feedbackName]);
            console.log(this.parsedHTML[feedbackName].body);
            this.feedbackArea.append(this.parsedHTML[feedbackName].body);
        }

        return this;
    }


    /**
     * storeLocally  ::  Void  -> storeObject
     * 
     * Method is used to store the state of the client within localStorage
     * 
     * Returns this to allow for method chaining
     */
    storeLocally() {
        localStorage.setItem("item", JSON.stringify(this.item));
        localStorage.setItem(this.id, JSON.stringify(this.warehouse));
        return this;
    }
};



//export {Store};