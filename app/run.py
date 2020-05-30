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
        def functionName(param1: paramType, param2: paramType...) -> returnType:
"""

from os import environ
from sys import argv
from app import server



def getConfig() -> dict:
    '''Function returns App Configuration'''

    config: dict = {
        'certificate_path': 'None',
        'http_proxy': 'None',
    }

    return config



def checkDebug() -> tuple:
    '''Function checks arguments for a debug statement and accompanying IP address'''

    return (argv[2], True) if len(argv) >= 3 and argv[1] == "debug" else ('localhost', False)



def setEnvironment(config: dict) -> dict:
    '''Function applies App Configuration to local environment'''

    environ['REQUESTS_CA_BUNDLE'] = config['certificate_path']
    environ['HTTP_PROXY'] = config['http_proxy']
    (config['host'], config['debug']) = checkDebug()

    return config



def start() -> None:
    '''Function configures local environment then launches the Flask App'''

    config: dict = setEnvironment(getConfig())

    # the app is imported after the environment is properly configured
    # this is because flask uses the local environment configuration
    # at launch

    app = server()
    app.env = 'development'
    print(f' * Running on http://{config["host"]}:5000/')
    app.run(host=config['host'], debug=True)
    # app.run(host=config['host'], debug=config['debug'])





if __name__ == "__main__":
    start()