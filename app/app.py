import os, logging
from flask import Flask
from routes import router
import network

def server(app):
    ''' Server function instantiates a server and returns the server instance '''

    path = os.path.dirname(os.path.realpath(__file__))

    logging.getLogger("requests").setLevel(logging.WARNING)

    logging.basicConfig(  
            filename = 'app.log',  
            level = logging.INFO,  
            format = '%(levelname)s:%(asctime)s:\t%(message)s') 


    app.secret_key = b'(\xe4S$\xce\xa81\x80\x8e\x83\xfa"b%\x9fr'

    lessons = []

    router(lessons, network, path, app)

    network.start(lessons, path)

    return app

# App wouldn't initialize without this (functionality moved to run.py)
# if __name__ == "__main__":
# server()