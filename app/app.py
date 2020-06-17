"""
File: app.py
Description: File contains the implementation of the Flask server for the PyGoat application
                Do not run directly via python app.py, run through the file run.py to configure
                the environment via python run.py

IMPORTANT!!! 
    To change configuration go to config.py, there you can set the proxy and security certificate settings

Conventions followed:
    4-space tabs
    3 empty lines between classes and functions
    Lines should be limited to less than 80 characters where possible
    Avoid Polluting the global scope
    DocStrings are restrained to a single line where possible:
       def functionName(paramName: paramType) -> returnType:
            ''' contents of docstring describing function behaviour '''
    Multi-line DocStrings follow the convention:
       def functionName(paramName: paramType) -> returnType:
             '''
                  contents of docstring describing function behaviour
             '''
    Inline Type Annotations follow the convention:
        variableName: variableType = variableValue
    Inline Function/Method Annotations follow the convention:
        def functionName(paramName1: paramType, paramName2: paramType...) -> returnType:
"""

import os, logging, jinja2
from flask import Flask
from routes import router
from config import env_config
import network


def server():
    ''' Server function instantiates a server and returns the server instance '''

    PROJECT_DIR: str = os.path.dirname(os.path.realpath(__file__))

    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.basicConfig(  
            filename = 'app.log',  
            level = logging.INFO,  
            format = '%(levelname)s:%(asctime)s:\t%(message)s') 

    app: Flask = Flask(__name__)
    app.config_rules: str = env_config(PROJECT_DIR)

    # Changes the directory for the lesson templates from ./templates to ./lessons
    app.jinja_loader = jinja2.ChoiceLoader([
        app.jinja_loader,
        jinja2.FileSystemLoader(
            app.config_rules['template_dirs']
        ),
    ])

    app.secret_key: 'ByteString' = b'(\xe4S$\xce\xa81\x80\x8e\x83\xfa"b%\x9fr'
    lessons: list = []

    router(lessons, network, PROJECT_DIR, app)
    network.start(lessons, PROJECT_DIR)

    return app
