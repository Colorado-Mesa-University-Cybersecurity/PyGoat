"""
File: config.py
Description: Program holds the Envioronment and Flask configuration settings

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

"""



def env_config(PROJECT_DIR: str) -> dict:
    ''' Function returns Environment Configuration '''


    config: dict = {
        'certificate_path': 'None',
        'http_proxy': 'None',
        'template_dirs': [
            f'{PROJECT_DIR}/lessons'
        ]
    }

    return config
