"""
File: run.py
Description: Program configures the local environment and then launches the PyGoat application

IMPORTANT!!!
    If a user wishes to pass in a .pem security certificate
        and a proxy host, then alter the dictionary in getConfig

            config = {
                    'certificate_path': '<Absolute path to .pem certificate>',
                    'http_proxy': 'http://<proxyIP>:<proxyPort>',
                }

            Ex.

            config = {
                    'certificate_path': '/home/lucas/certificate.pem',
                    'http_proxy': 'http://127.0.0.1:8082',
                }


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
import os, jinja2, config
from flask import Flask
from os import environ
from sys import argv
from app import server

# The initialization of app had to be moved out here in order for the app to start from bash command line - Let me know if this isn't the whole story
app = Flask(__name__)

loader = jinja2.ChoiceLoader([
    app.jinja_loader,
    jinja2.FileSystemLoader([
        f'{PROJECT_DIR}/templates',
        *config['template_dirs']
    ]),
])
app.jinja_loader = loader



def checkDebug() -> tuple:
    ''' Function checks arguments for a debug statement and accompanying IP address '''

    return (argv[2], True) if len(argv) >= 3 and argv[1] == "debug" else ('localhost', False)



def setEnvironment(config: dict) -> dict:
    ''' Function applies App Configuration to local environment '''

    environ['REQUESTS_CA_BUNDLE'] = config['certificate_path']
    environ['HTTP_PROXY'] = config['http_proxy']
    (config['host'], config['debug']) = checkDebug()

    return config



def start() -> None:
    ''' Function configures local environment then launches the Flask App '''

    session_config: dict = setEnvironment(config)

    server(app)
    app.env = 'development'

    print(f' * Running on http://{session_config["host"]}:5000/')
    
    # app.run(host=config['host'], debug=True)
    # app.run(host=config['host'], debug=config['debug'])





# if __name__ == "__main__":
start()