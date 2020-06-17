"""
File: lesson_handler.py
Description: File instantiates the lesson class to hold lesson data after being parsed from yaml files


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

import yaml



class lesson:
    def __init__(self, yaml_config):
        self.name: str = yaml_config['name'] # for the template
        self.title: str = yaml_config['name'] # for client-side rendering
        self.group: str = yaml_config['group']
        self.url: str = yaml_config['url'] 
        self.pages: int or str = yaml_config['numberOfPages'] 
        self.content = yaml_config['content']
        self.difficulty: int or str = yaml_config['difficulty']
        self.type = yaml_config['type']
        self.completable: bool = yaml_config['completable']
        self.completed: bool = False
        
        self.success_condition = None
        self.load_script = None
        self.load_return = None
        self.db_tables = None
        self.routes = None


        if 'success-condition' in yaml_config:
            self.success_condition = yaml_config['success-condition']
        if 'db-tables' in yaml_config:
            self.db_tables = yaml_config['db-tables']
        if 'routes' in yaml_config:
            self.routes = yaml_config['routes']
        if 'load-script' in yaml_config:
            self.load_script = yaml_config['load-script']
        if 'load-return' in yaml_config:
            self.load_return = yaml_config['load-return']
