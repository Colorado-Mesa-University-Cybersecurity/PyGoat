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
    Import inside a function's scope if Library is only used in that function
    DocStrings are restrained to a single line where possible
    Multi-line DocStrings follow the convention:
        '''
            contents of docstring
        '''
    Inline Annotations follow the convention:
        def functionName(param1: paramType, param2: paramType...) -> returnType:
"""



def getConfig() -> dict:
    '''Function returns App Configuration'''
    config = {
        'certificate_path': 'None',
        'http_proxy': 'None',
    }
    return config



def setEnvironment(config: dict) -> None:
    '''Function applies App Configuration to local environment'''
    from os import environ

    environ['REQUESTS_CA_BUNDLE'] = config['certificate_path']
    environ['HTTP_PROXY'] = config['http_proxy']



def checkDebug() -> bool:
    '''Function checks arguments for a debug statement'''
    from sys import argv
    return True if len(argv) >= 2 and argv[1] == "debug" else False



def start():
    '''Function configures local environment then launches the Flask App'''
    setEnvironment(getConfig())

    # the app is imported after the environment is properly configured
    # this is because flask uses the local environment configuration
    # at launch
    import main 
    main.app.env = 'development'
    main.app.run(host='localhost', debug=checkDebug())



# An IIFE (Immediately Invoked Funcitonal Expression)
# Function takes no input and starts the program immediately
#   after creation without entering the global scope
(lambda: start() if __name__ == "__main__" else None)()