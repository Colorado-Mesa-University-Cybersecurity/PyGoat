# PyGoat Front-End

This directory holds all of the static files used in the creation of the front-end for the PyGoat Application

The front-end is built using jinja templates for the login and registration pages (found in the ../templates directory)

User's who have registered and logged in will then be served the jinja template index.html which will implement the react code

This Readme is to help future developers work without confusion

## Architecture

### Directory layout
```bash
    static
    |
    |___ css
    |
    |___ js
    |   |
    |   |___ components
    |   |
    |   |___ libraries
    |   |
    |   |___ store
    |   |
    |   |___ tests
    |
    |___ jsx
    |   |
    |   |___ base
    |   |
    |   |___ components
    |   
    |___ photos
    |
    |___ styles
```

### Directory Contents

static/css: constains all the css rules used by index.html

static/js/components: contains all transpiled react components. Do Not Edit These Files Directly!!! use the transpiler to edit their corresponding .jsx files in jsx/components and transpile them into this directory

static/js/libraries: contains all of the libraries requested from the client to speed up load times

static/js/store: contains all of the store files that manage the data used to render and manage state of the react components

static/js/tests: contains tests on client-side javascript. The testing library Jest is used, it is super simple so don't worry if you are not familiar with it.

static/js: contains the client's base javascript react files that import the components and the stores. Do Not Edit These Files Directly!!! use the transpiler to edit their corresponding .jsx files in jsx/base and transpile them into this directory

static/jsx/base: contains all of the react JSX versions of the .js files in static/js directory (not in any of the directories contained in static/js). Edit these files while running the transpiler

static/jsx/components: contains all of the react JSX versions of the components in the static/js/components directory. Edit these components or add new components here while running the transpiler

static/photos: contains all image assets

static/styles: contains legacy files used to by the login and registration screens. needs refactored

static: contains the Figma template used to create the PyGoat Application, package.json for installing and running the transpiler, favicon.ico, the babel.config.json file for the transpiler, and other .json files for npm.


## Set up

### Installation

Inside the static directory, run the command:

```bash
    npm install
```

note: this only works in a CLI environment with node.js installed

### Run the Transpiler

#### Base

Once npm install has finished, run the following command to build the base components:

```bash
    npm run buildBase
```

Note: this command will run a babel transpiler within the user's console window. Babel will watch the static/jsx/base directory, and anytime a file is added or changed, it will transpile that file and deposit it in static/js.

#### Components

Run the following command to build React Components used by the PyGoat Application:

```bash
    npm run buildComps
```

Note: this command will run a babel transpiler within the user's console window. Babel will watch the static/jsx/components directory, and anytime a file is added or changed, it will transpile that file and deposit it in static/js/components.


### jsx transpilation

User's can run the babel transpiler without npm by altering the following command to suit their needs:

```bash
    npx babel --watch ./jsx/components --out-dir ./js/components --presets react
```  

Then the user can edit the files in the directory following the --watch flag and the babel transpiler will compile the files into .js any time any files in the directory are change, the compiled .js files are deposited in the directory following the --out-dir flag
