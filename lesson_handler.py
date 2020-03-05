import os, yaml

path = os.path.dirname(os.path.realpath(__file__))

class lesson:
    def __init__(self, yaml_config):
            self.name = yaml_config['name']
            self.url = yaml_config['url']
            self.content = yaml_config['content']

            self.success_condition = None
            self.db_tables = None
            self.routes = None

            if 'success-condition' in yaml_config:
                self.success_condition = yaml_config['success-condition']
            if 'db-tables' in yaml_config:
                self.db_tables = yaml_config['db-tables']
            if 'routes' in yaml_config:
                self.routes = yaml_config['routes']
