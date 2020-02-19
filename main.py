from flask import Flask, render_template, session, redirect, url_for, request, flash
import os, sys, yaml, sqlite3, hashlib

class lesson:
    def __init__(self, name="Undef", url="nowhere", content=None):
        self.name = name
        self.url = url
        self.content = content
        print(self.name)

path = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__)
app.secret_key = b'(\xe4S$\xce\xa81\x80\x8e\x83\xfa"b%\x9fr'

conn = sqlite3.connect('pygoat.db')
c = conn.cursor()
c.execute('''CREATE TABLE if not exists users
                 (username text, password blob, salt blob)''')
conn.commit()
conn.close()

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
    conn = sqlite3.connect('pygoat.db')
    c1 = conn.cursor()
    c1.execute('''SELECT salt FROM users WHERE username = ?''', [username])
    salt = c1.fetchone()[0]
    if salt is not None:
        m = hashlib.sha256()
        m.update(salt)
        m.update(password.encode('utf-8'))
        pass_hash = m.digest()
        c1.execute('''SELECT * from users where username=? and password =?''', (username, pass_hash))
        test = c1.fetchone()
        conn.close()
        if test is None:
            flash('Invalid credentials')
        return test is not None
    else:
        conn.close()
        flash('Invalid credentials')
        return False

@app.route('/')
def index():
    if 'username' in session:
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
    return render_template('login.html', login=True)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/lessons/<lesson>')
def lessons_page(lesson):
    if 'username' in session:
        current_lesson = next(filter(lambda x:x.url == lesson, lessons))
        return render_template('lesson.html',
                title=current_lesson.name,
                contentFile="/content/%s" % current_lesson.content,
                lessons=lessons)
    else:
        return redirect(url_for('login'))

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('pygoat.db')
        c1 = conn.cursor()
        c1.execute('SELECT username FROM users WHERE username=?', [username])
        if c1.fetchone() is None:
            salt = os.urandom(32)

            m = hashlib.sha256()
            m.update(salt)
            m.update(password.encode('utf-8'))
            pass_hash = m.digest()
            print(username, pass_hash, salt)

            c1.execute('''INSERT INTO users VALUES (?, ?, ?)''', (username, pass_hash, salt))
            conn.commit()
            session['username'] = request.form['username']
            conn.close()
            return redirect(url_for('index'))
        else:
            conn.close()
            flash('username already exists')
    return render_template('login.html', login=False)
