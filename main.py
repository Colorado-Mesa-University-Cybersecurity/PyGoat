from flask import Flask, render_template
import os, sys, yaml

class lesson:
    def __init__(self, name="Undef", url="nowhere"):
        self.name = name
        self.url = url

path = os.path.dirname(os.path.realpath(sys.argv[0]))
app = Flask(__name__)
lessons = []
for dirname in os.listdir("lessons"):
    with open("lessons/%s/config.yaml" % dirname, "r") as config:
        config_list = yaml.safe_load(config)
        name = config_list['name']
        url = config_list['url']
        current_lesson = lesson(name, url)
        lessons.append(current_lesson)

@app.route('/')
def login():
    return render_template('login.html')

