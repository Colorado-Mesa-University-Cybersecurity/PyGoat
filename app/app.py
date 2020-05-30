from flask import Flask
import os, logging
from routes import router
import network

path = os.path.dirname(os.path.realpath(__file__))

logging.getLogger("requests").setLevel(logging.WARNING)

logging.basicConfig(  
        filename = 'app.log',  
        level = logging.INFO,  
        format = '%(levelname)s:%(asctime)s:%(message)s') 

app = Flask(__name__)

app.secret_key = b'(\xe4S$\xce\xa81\x80\x8e\x83\xfa"b%\x9fr'

lessons = []

router(lessons, network, path, app)

network.start(lessons, path)