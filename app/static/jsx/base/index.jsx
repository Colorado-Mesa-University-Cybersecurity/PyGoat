/*
File: index.js
Description: file defines the View and Controller classes and instantiates them using the imported store Class
				This is designed based on Reacts role as the View in a traditional MVC, but views contain their
				state along with the application state in an object known as the Store instead of a model.
				The MVC pattern is used client side as opposed to server side to create a Single Page Application
				learn more about this MVC implementation here: https://www.taniarascia.com/javascript-mvc-todo-app/
				
IMPORTANT!!! If you are reading this from within a .js file,  EXIT THE FILE!!!   Go to the jsx/base directory 
    and find index.jsx.  React is Transpiled from JSX, unless you are familiar with React, you will not
    understand anything about the file unless you read the JSX file which is declarative and self documenting 


    it is important to note that you should not 
	make any changes to that file if you wish to edit the PyGoat client, instead follow the directions on 
	the README.md contained within the static directory. Make sure any editing is done with the .jsx version
	of this file inside the static/jsx directory

Conventions followed:
    4-space tabs
    always place semicolons
    trailing commas in arrays and objects
    3 empty lines between classes and functions
    2 empty lines between methods
    Class methods always return this unless other return value desired
    annotations follow the convention:     
            function/method  ::  (parameter types) -> (return types)
*/


import {App} from "./app.js";
import {Store} from "./store/store.js"


/**
 * Class View
 * 
 * View instantiates a view object to control rendering and updating the user interface
 * 
 * Methods:
 *
 *		constructor  ::  void  -> view object
 *			method instantiates view object and creates format object to pass to react components
 *
 *
 * 		render  ::  store object  ->  view object
 * 			renders all of the App components using the data in the store object passed to the method
 */
class View {
    constructor() {
        this.format = {};
        this.format.header = {height: "120px", width: "100%"};
        this.format.sidebar = {minHeight: "20rem", width: "300px"};

        return this;
    }


    render(props) {
        props.format = this.format;

        ReactDOM.render(

            // This is JSX, JavaScript with XML
            // This is used to create component based designs in the React and Vue libraries
            // learn more about JSX here  https://reactjs.org/docs/introducing-jsx.html
            <React.StrictMode>
                // This just prevents bugs from the "this" object
                <App store={props} />
            </React.StrictMode>,
            document.getElementById("root")
        );
        return this;
    };
};



/**
 * Class Controller
 * 
 * Controller instantiates a controller object to direct the exchange of data between store and view objects
 * 
 * Methods:
 * 
 * 		constructor  ::  ( store object, view object )  ->  controller object
 */
class Controller {
    constructor(store, view) {
        this.store = store;
        this.view = view;
        this.view.render(this.store);

        return this;
    };
};


/**
 * launch  ::  void -> void
 * 
 * Function launch is an IIFE(Immediately Invoked Functional Expression) that instantiates the
 *    Store, View, and Controller Classes 
 * 
 * learn more about IIFE's here: https://developer.mozilla.org/en-US/docs/Glossary/IIFE
 * 
 */
;(function launch() {
    localStorage.clear()
    const PyGoat = new Controller(new Store, new View);
    console.log("index.jsx loaded");
})();