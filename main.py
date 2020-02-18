from flask import Flask, render_template, session, redirect, url_for, request
import os, sys, yaml

class lesson:
    def __init__(self, name="Undef", url="nowhere", content=None):
        self.name = name
        self.url = url
        self.content = content
        print(self.name)

path = os.path.dirname(os.path.realpath(__file__))
app = Flask(__name__)
app.secret_key = b'(\xe4S$\xce\xa81\x80\x8e\x83\xfa"b%\x9fr'

lessons = []
for filename in os.listdir("lessons"):
    if filename.endswith('yaml'):
        with open("%s/lessons/%s" % (path, filename), "r") as config:
            config_list = yaml.safe_load(config)
            name = config_list['name']
            url = config_list['url']
            content = config_list['content']
            current_lesson = lesson(name, url, content)
            lessons.append(current_lesson)

def valid_login(username, password):
    return username == 'admin' and password == 'password'

@app.route('/')
def index():
    if 'username' in session:
        print('logged in')
        return render_template('header.html', lessons=lessons)
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None 
    if request.method == 'POST':
        if valid_login(request.form['username'], request.form['password']):
            session['username'] = request.form['username']
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/lessons/<lesson>')
def lessons_page(lesson):
    current_lesson = next(filter(lambda x:x.url == lesson, lessons))
    return render_template('lesson.html',
            title=current_lesson.name,
            contentFile="/content/%s" % current_lesson.content,
            lessons=lessons)

@app.route('/register', methods=['POST', 'GET'])
def register():
    pass
