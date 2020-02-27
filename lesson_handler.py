import os, yaml

path = os.path.dirname(os.path.realpath(__file__))

class lesson:
    def __init__(self, yaml_config):
        with open("%s/lessons/%s" % (path, lessons) as conf:
                config_list = yaml.safe_load(conf)
                self.name = config_list['name']
                self.url = config_list['url']
                self.content = config_list['content']

                self.success_condition = config_list['
