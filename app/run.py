"""
File: run.py
Description: Program configures the local environment and then launches the PyGoat application

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


from flask import Flask
from os import environ, path
from sys import argv
from app import server
from config import env_config



def checkDebug() -> tuple:
    ''' Function checks arguments for a debug statement and accompanying IP address '''

    return (argv[2], True) if len(argv) >= 3 and argv[1] == "debug" else ('localhost', False)



def setEnvironment(config: dict) -> dict:
    ''' Function applies App Configuration to local environment '''

    environ['REQUESTS_CA_BUNDLE'] = config['certificate_path']
    environ['HTTP_PROXY'] = config['http_proxy']
    (config['host'], config['debug']) = checkDebug()

    return config



def start(run_through_python: bool) -> None:
    ''' Function configures local environment then launches the Flask App '''

    config: dict = env_config(path.dirname(path.realpath(__file__)))

    session_config: dict = setEnvironment(config)

    app = server()

    app.env = 'development'

    print(f' * Running on http://{session_config["host"]}:5000/')

    if run_through_python:  # if running using run.py activates, otherwise if using run.sh or flask run, skips
        app.run(host=session_config['host'], debug=session_config['debug'])





if __name__ == "__main__":
    start(True)
else:
    start(False)