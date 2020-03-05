from flask import Flask, render_template, session, redirect, url_for, request, flash
import os, sys, yaml, sqlite3, hashlib, custom, requests, logging
from lesson_handler import lesson

logging.getLogger("requests").setLevel(logging.WARNING)

path = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__)
app.secret_key = b'(\xe4S$\xce\xa81\x80\x8e\x83\xfa"b%\x9fr'

conn = sqlite3.connect('pygoat.db')
c = conn.cursor()
c.execute('''CREATE TABLE if not exists users
                 (username text, password blob, salt blob)''')
conn.commit()

lessons = []
for filename in os.listdir("%s/lessons" % path):
    if filename.endswith('yaml'):
        with open("%s/lessons/%s" % (path, filename), "r") as config:
            config_list = yaml.safe_load(config)
            current_lesson = lesson(config_list)
            lessons.append(current_lesson)

print('Ignore the duplicate column errors below, I had to catch it as a workaround')
for lesson in lessons:
    # add columns to users database tracking lesson completion
    colName = "%sCompleted" % lesson.name
    try:
        c.execute('''ALTER TABLE users ADD "%s" integer''' % colName) 
    except sqlite3.DatabaseError as e:
        print(e)
    # initialize database tables
    if lesson.db_tables is not None:
        for table in lesson.db_tables:
            try: 
                c.execute('''DROP TABLE %s''' % table['name'])
                conn.commit()
            except sqlite3.DatabaseError as e:
                print(e)
            sqlString = '''CREATE TABLE %s (''' % table['name']
            conn.commit()
            for column in table['columns']:
                sqlString += column['name'] + ' ' + column['type'] + ','
            sqlString = sqlString[:-1:] + ')'
            c.execute(sqlString)
            for row in table['rows']:
                sqlString2 = '''INSERT INTO %s (''' % table['name']
                for colum in row.keys():
                    sqlString2 += "'" + str(colum) + "',"
                sqlString2 = sqlString2[:-1:] + ') VALUES ('
                c.execute(sqlString2 + ",".join("?"*len(row.values())) + ")", tuple(row.values()))
conn.commit()
conn.close()

def valid_login(username, password):
    conn = sqlite3.connect('pygoat.db')
    c1 = conn.cursor()
    c1.execute('''SELECT salt FROM users WHERE username = ?''', [username])
    saltarr = c1.fetchone()
    if saltarr is not None:
        salt = saltarr[0]
        m = hashlib.sha256()
        m.update(salt)
        m.update(password.encode('utf-8'))
        pass_hash = m.digest()
        c1.execute('''SELECT * from users where username=? and password =?''', (username, pass_hash))
        test = c1.fetchone()
        conn.close()
        if test is None:
            flash(('danger', 'Invalid credentials'))
        return test is not None
    else:
        conn.close()
        flash(('danger', 'Invalid credentials'))
        return False

def send_webrequest(webrequest, request):
    url = "http://localhost:5000%s" % webrequest['url']
    if webrequest['method'] == 'POST':
        if 'headers' in webrequest:
            requests.post(url, data=webrequest['body'], headers=webrequest['headers'])
        else:
            requests.post(url, data=webrequest['body'])
    else:
        if 'headers' in webrequest:
            requests.get(url, headers=webrequest['headers'])
        else:
            requests.get(url)

def make_sql_query(query, request):
    conn = sqlite3.connect('pygoat.db')
    c = conn.cursor()
    parameters = []
    qstring = query['qstring']
    qstringArr = qstring.split(' ')

    if query['injectable']:
        for index, dat in enumerate(qstringArr.copy()):
            if dat.startswith("'$"):
               parameters.append(dat)
               qstringArr = qstringArr[0:index:] + ["'%s'"] + qstringArr[index+1::]
            elif dat.startswith("$"):
               parameters.append(dat)
               qstringArr = qstringArr[0:index:] + ["%s"] + qstringArr[index+1::]

        for index, dat in enumerate(parameters.copy()):
            if dat.startswith('$form'):
                if dat.endswith(';'):
                    dat2 = request.form[dat[6:-1:]]
                    dat2 += ';'
                else:
                    dat2 = request.form[dat[6::]]
                parameters = parameters[0:index:] + [dat2] + parameters[index + 1::]

        qstring = " ".join(qstringArr)
        c.execute(qstring % tuple(parameters))
        rows = c.fetchall()
        rows.append(qstring % tuple(parameters))

    else:
        for index, dat in enumerate(qstringArr.copy()):
            if dat.startswith('$'):
               parameters.append(dat)
               qstringArr = qstringArr[0:index:] + ["?"] + qstringArr[index+1::]

        for index, dat in enumerate(parameters.copy()):
            if dat.startswith('$form'):
                dat2 = request.form[dat[6::]]
                parameters = parameters[0:index:] + [dat2] + parameters[index + 1::]

        qstring = " ".join(qstringArr)
        c.executescript(qstring, tuple(parameters))
        rows = c.fetchall()
        rows.append(qstring)
        rows.append(tuple(parameters))
    print(rows)
    flash(("warning", rows))

    conn.commit()
    conn.close()

def lesson_success(lesson):
    colName = "%sCompleted" % lesson.name
    conn = sqlite3.connect('pygoat.db')
    c = conn.cursor()
    c.execute('''UPDATE users SET "%s" = 1 WHERE username = ?''' % colName, [session['username']])
    conn.commit()
    conn.close()
    return(redirect('/lessons/%s' % lesson.url))
    print('lesson %s successful' % lesson.name)

@app.route('/')
def index():
    if 'username' in session:
        return render_template('lesson.html', lessons=lessons, title="Lessons", contentFile="doesn't exist")
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
        if current_lesson.success_condition is not None:
            results = custom.find_and_run(current_lesson.success_condition, request)
            if results is not None and results == True:
                lesson_success(current_lesson)

        colName = "%sCompleted" % current_lesson.name
        conn = sqlite3.connect('pygoat.db')
        c = conn.cursor()
        c.execute('''SELECT "%s" from users where username = ?''' % colName, [session['username']])
        if c.fetchone()[0] == 1:
            flash(('success', 'You have completed this lesson'))
        conn.close()

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

            c1.execute('''INSERT INTO users (username, password, salt) VALUES (?, ?, ?)''', (username, pass_hash, salt))
            conn.commit()
            session['username'] = request.form['username']
            conn.close()
            return redirect(url_for('index'))
        else:
            conn.close()
            flash(('danger', 'username already exists'))
    return render_template('login.html', login=False)

@app.route('/<routeName>', methods=['POST', 'GET'])
def custom_routes(routeName):
    if 'username' in session:
        routename_with_slash = '/' + routeName

        # determine which lesson this route is attached to. This might be slow with a lot of lessons
        source_lesson = next(filter(lambda x: x.routes is not None and len(list(filter(lambda y: y['path'] == routename_with_slash,x.routes))) > 0, lessons))

        # determine which route in said lesson got us here
        source_route = next(filter(lambda x: x['path'] == routename_with_slash, source_lesson.routes))

        print(source_lesson.name)

        if source_lesson.success_condition is not None:
            results = custom.find_and_run(source_lesson.success_condition, request)
            if results is not None and results == True:
                lesson_success(source_lesson)

        if source_route['action'] == 'send-webrequest':
            send_webrequest(source_route['webrequest'], request)
        elif source_route['action'] == 'sql-query':
            make_sql_query(source_route['query'], request)
        elif source_route['action'].startswith('$custom'):
            result = custom.find_and_run(source_route['action'], request)
            if 'success_if_true' in souce_route and source_route['success_if_true']:
                if result is not None and result == True:
                    lesson_success(source_lesson)

        return render_template('lesson.html',
            title=source_lesson.name,
            contentFile="/content/%s" % source_lesson.content,
            lessons=lessons)
    else: 
        return(redirect(url_for('login')))
