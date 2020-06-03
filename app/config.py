# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

config: dict = {
    'certificate_path': 'None',
    'http_proxy': 'None',
    'template_dirs': [
        f'{PROJECT_DIR}/lessons'
    ]
}