import os, yaml

path = os.path.dirname(os.path.realpath(__file__))

class lesson:
    def __init__(self, yaml_config):
            self.name = yaml_config['name']
            self.url = yaml_config['url']
            self.content = yaml_config['content']
            self.difficulty = yaml_config['difficulty']
            self.completable = yaml_config['completable']
            self.completed = False
            
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
