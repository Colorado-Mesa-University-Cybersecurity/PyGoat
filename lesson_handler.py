import os, yaml

path = os.path.dirname(os.path.realpath(__file__))

class lesson:
    def __init__(self, yaml_config):
            self.name = yaml_config['name']
            self.url = yaml_config['url']
            self.difficulty = yaml_config['difficulty']
            self.pages = yaml_config['pages']

            for page in self.pages:
                page['completed'] = False
