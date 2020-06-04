import os, logging
import jinja2
from flask import Flask
from routes import router
from config import env_config
import network

def server():
    ''' Server function instantiates a server and returns the server instance '''

    PROJECT_DIR: str = os.path.dirname(os.path.realpath(__file__))

    logging.getLogger("requests").setLevel(logging.WARNING)

    logging.basicConfig(  
            filename = 'app.log',  
            level = logging.INFO,  
            format = '%(levelname)s:%(asctime)s:\t%(message)s') 

    app = Flask(__name__)

    app.config_rules = env_config(PROJECT_DIR)

    app.jinja_loader = jinja2.ChoiceLoader([
        app.jinja_loader,
        jinja2.FileSystemLoader(
            app.config_rules['template_dirs']
            # f'{path}/templates'
        ),
    ])

    app.secret_key = b'(\xe4S$\xce\xa81\x80\x8e\x83\xfa"b%\x9fr'

    lessons = []

    router(lessons, network, PROJECT_DIR, app)

    network.start(lessons, PROJECT_DIR)

    return app
