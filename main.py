"""
    All the routes and the lesson helper functions are stored here
"""

from flask import Flask, render_template, session, redirect, url_for, request, flash, Response
from xml.dom.pulldom import START_ELEMENT, parseString
from xml.sax import make_parser
from xml.sax.handler import feature_external_ges
import os, sys, yaml, sqlite3, hashlib, custom, requests, logging, json, time
from lesson_handler import lesson

logging.getLogger("requests").setLevel(logging.WARNING)

path = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__)
app.secret_key = b'(\xe4S$\xce\xa81\x80\x8e\x83\xfa"b%\x9fr'

lessons = []

last_loaded = None
start_time = 0

def load_lessons(lessondir="%s/lessons" % path):
    """ load in the lessons from the yaml config files
        lessondir = string - the absolute path of the directory where the lesson 
        yaml configs are stored
    """

    for filename in os.listdir(lessondir):
        if filename.endswith('yaml'):
            with open("%s/%s" % (lessondir, filename), "r") as config:
                config_list = yaml.safe_load(config)
                current_lesson = lesson(config_list)
                lessons.append(current_lesson)

def initialize_db(dbname='pygoat.db'):
    """ initialize the 'users' table
        dbname = string - the name of the database to use 
    """
    print('Ignore the duplicate column errors below, I had to catch it as a workaround')

    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    c.execute('''CREATE TABLE if not exists users
                     (username text, password blob, salt blob)''')
    conn.commit()

    for lesson in lessons.copy():
        # add columns to users database tracking lesson completion. 
        # There is no ADD column IF NOT EXISTS in SQLite, so just catching the error will have to do for now 
        if lesson.completable:
            colName = "%sCompleted" % lesson.name
            col2Name = "%sAttempts" % lesson.name
            col3Name = "%sTime" % lesson.name
            try:
                c.execute('''ALTER TABLE users ADD "%s" integer''' % colName) 
                c.execute('''ALTER TABLE users ADD "%s" integer''' % col2Name) 
                c.execute('''ALTER TABLE users ADD "%s" integer''' % col3Name) 
            except sqlite3.DatabaseError as e:
                print(e)
    conn.commit()
    conn.close()

def initialize_lesson_db(lesson, dbname='pygoat.db'):
    """ initialize the custom database tables defined in the lesson yamls
        lesson = lesson object - a lesson object obtained from reading in a lesson
          yaml file
        dbname = string - the name of the database to use
    """
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    print('initializing %s' % lesson.name)
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

def valid_login(username, password, dbname='pygoat.db', testing=False):
    """
    tests a username and password to see if they are in the users table
    username = string - the username
    password = string - the plaintext of the password
    dbname = string - the name of the database to check
    testing = boolean - if false, will flash messages when user fails to log in
    """
    conn = sqlite3.connect(dbname)
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
        if not testing:
            if test is None:
                flash(('danger', 'Invalid credentials'))
        return test is not None
    else:
        conn.close()
        if not testing:
            flash(('danger', 'Invalid credentials'))
        return False

def send_webrequest(webrequest, request=None, url="http://localhost:5000", testing=False):
    """
     send an arbitrary web request using route actions in the config files
     replaces $form and $session primitives with their counterparts in the request

     webrequest = a webrequest object, obtained by reading in the lesson yaml
     request = a flask request object
     url = string - the url to send the webrequest to
     testing - if False, appends session data to webrequest headers as a cookie
     and sends the request, otherwise, merely returns it
     """
    url = "%s%s" % (url, webrequest['url'])
    headers = {}
    body = {}
    if 'headers' in webrequest:
        for header,value in webrequest['headers'].items():
            tempheader = ""
            tempbody = ""
            if header.startswith('$form'):
                tempheader = request.form[header[6::]]
            elif header.startswith('$session'):
                tempheader = session[header[9::]]
            else:
                tempheader = header
            if value.startswith('$form'):
                tempbody = request.form[value[6::]]
            elif value.startswith('$session'):
                tempbody = session[value[9::]]
            else:
                tempbody = value
            headers[tempheader] = tempbody
               
    if not testing:
        headers['cookie'] = 'session=' + request.cookies['session']

    if 'body' in webrequest:
        if isinstance(webrequest['body'], str):
            bodyArr = webrequest['body'].split(' ')
            for index, val in enumerate(bodyArr.copy()):
                tempval = ""
                if val.startswith('$form'):
                    tempval = request.form[val[6::]]
                elif val.startswith('$session'):
                    tempval = session[val[9::]]
                else:
                    tempval = val
                bodyArr = bodyArr[0:index:] + [tempval] + bodyArr[index+1::]
            body = ' '.join(bodyArr)
                    
        else:
            body = {}
            for key,value in webrequest['body'].items():
                tempkey = ""
                tempvalue = ""
                if key.startswith('$form'):
                    tempkey = request.form[key[6::]]
                elif key.startswith('$session'):
                    tempkey = session[key[9::]]
                else:
                    tempkey = key
                if value.startswith('$form'):
                    tempvalue = request.form[value[6::]]
                elif value.startswith('$session'):
                    tempvalue = session[value[9::]]
                else:
                    tempvalue = value
                body[tempkey] = tempvalue

    if testing:
        return url,headers,body
    else:
        if webrequest['method'] == 'POST':
                requests.post(url, data=body, headers=headers)
        elif webrequest['method'] == 'GET':
                requests.get(url, headers=headers, params=body)

def make_sql_query(query, request=None, dbname='pygoat.db', testing=False):
    """
    make arbitrary sql queries using route actions in the config files
    replace $form and $session primitives with their counterparts in the request
    if designated injectable, pass the parameters into the query as strings, otherwise pass in a prepared statement
    will probably break if you want non-injectable sql and variable tables or column names
    query - a query object, obtained by reading in the lesson yaml
    request - a flask request
    dbname = string - the name of the database to query
    testing = boolean - if False, flashes the sql query and its output to the screen and runs it, otherwise, returns it

    """
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    parameters = []
    qstring = query['qstring']
    # the below line is why each $form and $session primitive need to be surrounded by spaces, 
    # otherwise it will try to read bad form values and throw 400 errors
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
                dat2 = request.form[dat[6::]]
            elif dat.startswith('$session'):
                dat2 = session[dat[9::]]
            else: dat2 = dat
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
            elif dat.startswith('$session'):
                dat2 = session[dat[9::]]
            else: dat2 = dat
            parameters = parameters[0:index:] + [dat2] + parameters[index + 1::]

        qstring = " ".join(qstringArr)
        print(qstring)
        c.execute(qstring, tuple(parameters))
        rows = c.fetchall()
        rows.append(qstring)
        rows.append(tuple(parameters))

    if not testing:
        flash(("warning", rows))

    conn.commit()
    conn.close()

def make_custom_response(response, request=None, testing=False):
    """
     returns an arbitrary response using route actions in the config files
     replaces $form and $session primitives with their counterparts in the 
response object

     response = a response object, obtained by reading in the lesson yaml
     request = a flask request object
     testing - if False, appends session data to response headers as a cookie and returns flask Response object, otherwise, returns the headers and body dictionaries
     """

    headers = {}
    body = {}

    if 'headers' in response:
        for header,value in response['headers'].items():
            tempheader = ""
            tempbody = ""
            if header.startswith('$form'):
                tempheader = request.form[header[6::]]
            elif header.startswith('$session'):
                tempheader = session[header[9::]]
            else:
                tempheader = header
            if value.startswith('$form'):
                tempbody = request.form[value[6::]]
            elif value.startswith('$session'):
                tempbody = session[value[9::]]
            else:
                tempbody = value
            headers[tempheader] = tempbody
               
    if not testing:
        headers['cookie'] = 'session=' + request.cookies['session']

    if 'body' in response:
        if isinstance(response['body'], str):
            bodyArr = response['body'].split(' ')
            for index, val in enumerate(bodyArr.copy()):
                tempval = ""
                if val.startswith('$form'):
                    tempval = request.form[val[6::]]
                elif val.startswith('$session'):
                    tempval = session[val[9::]]
                else:
                    tempval = val
                bodyArr = bodyArr[0:index:] + [tempval] + bodyArr[index+1::]
            body = ' '.join(bodyArr)
                    
        else:
            body = {}
            for key,value in response['body'].items():
                tempkey = ""
                tempvalue = ""
                if key.startswith('$form'):
                    tempkey = request.form[key[6::]]
                elif key.startswith('$session'):
                    tempkey = session[key[9::]]
                else:
                    tempkey = key
                if value.startswith('$form'):
                    tempvalue = request.form[value[6::]]
                elif value.startswith('$session'):
                    tempvalue = session[value[9::]]
                else:
                    tempvalue = value
                body[tempkey] = tempvalue

    if not testing:
        return Response(response=body, headers=headers)
    else:
        return body, headers

def lesson_success(lesson, dbname='pygoat.db', testing=False):
    """
    sets the target lesson as successful in the database
    lesson - a lesson object, obtained by reading in the lesson yamls
    dbname = string - the name of the database to use
    testing = boolean - if False, redirects the user to the lesson page
    """

    colName = "%sCompleted" % lesson.name
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    c.execute('''UPDATE users SET "%s" = 1 WHERE username = ?''' % colName, [session['username']])
    conn.commit()
    conn.close()
    if not testing:
        return(redirect('/lessons/%s' % lesson.url))

def check_success(dbname='pygoat.db'):
    """
    loops through the lessons and checks to see if any of them are completed,
    if so, sets the completed variable in said lesson to true, otherwise, sets it to false

    dbname = string - the name of the database to use
    """

    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    for lesson in lessons:
        if lesson.completable:
            colName = "%sCompleted" % lesson.name
            c.execute('''SELECT "%s" FROM users WHERE username = ?''' % colName, [session['username']])
            result = c.fetchone()
            if result is not None and result[0] == 1:
                lesson.completed = True
            else:
                lesson.completed = False
    conn.close()

def increment_attempts(lesson, dbname='pygoat.db'):
    """
    increments the number of times the user has attempted a lesson in the database

    lesson - lesson object retrieved from yaml config
    dbname - name of database to modify
    """
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    colName = "%sAttempts" % lesson.name
    c.execute('''SELECT "%s" from users WHERE username = ?''' % colName, [session['username']])
    result = c.fetchone()
    if result is not None:
        if result[0] is None:
            newResult = 1
        else:
            newResult = int(result[0]) + 1
        c.execute('''UPDATE users SET "%s" = ? WHERE username = ?''' % colName, [newResult, session['username']])
        conn.commit()
    conn.close()

def update_time(lesson, timeToAdd, dbname='pygoat.db'):
    """
    updates the amount of time that the user has spent working on a particular lesson

    lesson - lesson object retrieved from yaml config
    timeToAdd - sqlite time string - the amount of time to add to the lesson
    dbname - name of database to modify
    """

    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    colName = "%sTime" % lesson.name
    c.execute('''SELECT "%s" from users WHERE username = ?''' % colName, [session['username']])
    result = c.fetchone()
    if result is not None:
        runningTime = result[0]
        if runningTime is None:
            runningTime = timeToAdd
        else:
            runningTime += timeToAdd
        c.execute('''UPDATE users SET "%s" = ? WHERE username = ?''' % colName, [runningTime, session['username']])
    conn.commit()
    conn.close()

def get_lesson_stats(dbname='pygoat.db'):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    for lesson in lessons:
        colName = "%sTime" % lesson.name
        col2Name = "%sAttempts" % lesson.name
        c.execute('''SELECT "%s","%s" from users WHERE username = ?''' % (colName, col2Name), [session['username']])
        result = c.fetchone()
        if result is not None:
            lesson.seconds = result[0]
            lesson.attempts = result[1]
    conn.close()

@app.route('/favicon.ico')
def favicon():
    """ 
    path = /favicon.ico
    returns the icon 
    """
    return(redirect(url_for('static', filename='favicon.ico')))

@app.route('/')
def index():
    """ 
    path = /
    if user is logged in, return home page, otherwise, return login page 
    """ 
    if 'username' in session:
        check_success()
        return render_template('lesson.html', lessons=lessons, title="Lessons", contentFile="doesn't exist")
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['POST', 'GET'])
def login():
    """ 
    path = /login
    if user sends GET to this page, returns login html
    if user POSTs this page, checks provided credentials against database, if they login successfully, add their username to the session cookie and redirect to home page
    """ 

    error = None 
    if request.method == 'POST':
        if valid_login(request.form['username'], request.form['password']):
            session['username'] = request.form['username']
            check_success()
            return redirect(url_for('index'))
    return render_template('login.html', login=True)

@app.route('/logout')
def logout():
    """
    path = /logout
    logs out the user
    """
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/lessonstatus')
def lessonstatus():
    """
    path = /lessonstatus
    for testing api, returns a list of lessons and whether they are completable and have been completed
    """
    if 'username' in session:
        check_success()
        finalDict = {}
        for lesson in lessons:
            finalDict[lesson.name] = {}
            finalDict[lesson.name]['completable'] = lesson.completable
            if lesson.completable:
                finalDict[lesson.name]['completed'] = lesson.completed
        return (json.dumps(finalDict))
    else:
        return redirect(url_for('login'))

# route for every lesson with a yaml config
@app.route('/lessons/<lesson>')
def lessons_page(lesson):
    """ 
    path = /lessons/<lesson>

    parameters:
    lesson - the url field of the lesson to load

    finds the lesson with the url field of lesson, checks if user has completed it, runs any cutom load scripts, and returns the loaded lesson
    """
    if 'username' in session:
        global last_loaded
        global start_time

        check_success()
        # get lesson with url passed into the route
        current_lesson = next(filter(lambda x:x.url == lesson, lessons))

        # track time associated with this lesson
        if last_loaded is None:
            last_loaded = current_lesson
            start_time = int(time.time())
        elif last_loaded.name != current_lesson.name:
            timeToAdd = int(time.time()) - start_time
            update_time(last_loaded, timeToAdd)
            last_loaded = current_lesson
            start_time = int(time.time())

        # check to see if the lesson has been completed
        if current_lesson.success_condition is not None:
            results = custom.find_and_run(current_lesson.success_condition, request)
            if results is not None and results == True:
                lesson_success(current_lesson)

        # if the lesson has been completed at some point in the past, let the user know
        if current_lesson.completed:
            flash(('success', 'You have completed this lesson'))

        # some lessons will define custom scripts to pass information to the html files
        # run those scripts and pass the information to the html here
        if current_lesson.load_script is not None:
            result = custom.find_and_run(current_lesson.load_script, request)
            param_dict = {
                    'template_name_or_list':'lesson.html',
                    'title':current_lesson.name,
                    'contentFile':"/content/%s" % current_lesson.content,
                    'lessons':lessons,
                    current_lesson.load_return: result}

            return render_template(**param_dict) 
        
        # for lessons with no custom initialization scripts
        return render_template('lesson.html',
                title=current_lesson.name,
                contentFile="/content/%s" % current_lesson.content,
                lessons=lessons)
    else:
        return redirect(url_for('login'))

@app.route('/register', methods=['POST', 'GET'])
def register():
    """
    path = /register
    if the user sends a GET request, returns register html
    if user POSTs, adds a new user to the database with the provided username and password
    """
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

@app.route('/reset/<lessonTitle>')
def reset_lesson(lessonTitle):
    """
    path = /reset/<lessonTitle>
    parameters:
    lessonTitle - the url of the lesson to reset

    Sets target lesson to not completed and recreates the associated database tables
    """

    if 'username' in session:
        lesson = next(filter(lambda x:x.url == lessonTitle, lessons))
        colName = "%sCompleted" % lesson.name
        col2Name = "%sAttempts" % lesson.name
        col3Name = "%sTime" % lesson.name
        conn = sqlite3.connect('pygoat.db')
        c = conn.cursor()
        c.execute('''UPDATE users SET "%s" = 0 WHERE username = ?''' % colName, [session['username']])
        c.execute('''UPDATE users SET "%s" = 0 WHERE username = ?''' % col2Name, [session['username']])
        c.execute('''UPDATE users SET "%s" = 0 WHERE username = ?''' % col3Name, [session['username']])
        conn.commit()
        conn.close()
        initialize_lesson_db(lesson)
        return redirect(url_for('lessons_page', lesson=lesson.url))
    else:
        return redirect(url_for('login'))

@app.route('/resetall')
def reset_all():
    """
    path = /resetall
    reinitializes all lesson tables and sets them all to not completed
    """
    if 'username' in session:
        conn = sqlite3.connect('pygoat.db')
        c = conn.cursor() 
        for lesson in lessons:
            colName = "%sCompleted" % lesson.name
            col2Name = "%sAttempts" % lesson.name
            col3Name = "%sTime" % lesson.name
            c.execute('''UPDATE users SET "%s" = 0 WHERE username = ?''' % colName, [session['username']])
            c.execute('''UPDATE users SET "%s" = 0 WHERE username = ?''' % col2Name, [session['username']])
            c.execute('''UPDATE users SET "%s" = 0 WHERE username = ?''' % col3Name, [session['username']])
            conn.commit()
            initialize_lesson_db(lesson)
        conn.close()
        check_success()
        return("Lessons reset")
    else:
        return redirect(url_for('login'))

# addtional routes defined in the yaml configs
@app.route('/<path:routeName>', methods=['POST', 'GET'])
def custom_routes(routeName):
    """
    path = /<path:routeName>
    parameters:
    routeName - the path for the custom route

    Checks if a route with the path routeName is defined in a lesson yaml and performs the actions associated with it

    1. send-webrequest - sends a request to the target url with a specified body and headers
    2. sql-query - query the sql database
    3. $custom.funcName(args) - runs the function in custom.py with the name funcName and any listed arguments
    4. response - returns a response defined in the lesson yaml

    It then checks if the lesson is completed.
    """
    if 'username' in session:
        global last_loaded
        global start_time

        check_success()
        routename_with_slash = '/' + routeName

        # determine which lesson this route is attached to. This might be slow with a lot of lessons
        source_lesson = next(filter(lambda x: x.routes is not None and len(list(filter(lambda y: y['path'] == routename_with_slash,x.routes))) > 0, lessons))

        # determine which route in said lesson got us here
        source_route = next(filter(lambda x: x['path'] == routename_with_slash, source_lesson.routes))

        # track time associated with this lesson
        if last_loaded is None:
            last_loaded = source_lesson
            start_time = int(time.time())
        elif last_loaded.name != source_lesson.name:
            timeToAdd = int(time.time()) - start_time
            update_time(last_loaded, timeToAdd)
            last_loaded = source_lesson
            start_time = int(time.time())

        # increment the number of times the user has attempted this lesson
        increment_attempts(source_lesson)

        # check to see if actions here complete the lesson where this route is defined
        if source_lesson.success_condition is not None:
            results = custom.find_and_run(source_lesson.success_condition, request)
            if results is not None and results == True:
                lesson_success(source_lesson)

        if source_lesson.completed:
            flash(('success', 'You have completed this lesson'))

        # handle route actions: there are 3 types
        # 1: send request to some other part of the site
        # 2: query the sql database
        # 3: run a custom script
        # 3a: the script might have complete the lesson if it returns True. Handle that case
        if source_route['action'] == 'send-webrequest':
            send_webrequest(source_route['webrequest'], request)
        elif source_route['action'] == 'sql-query':
            make_sql_query(source_route['query'], request)
        elif source_route['action'].startswith('$custom'):
            actionArr = source_route['action'].split(' ')
            for index, act in enumerate(actionArr.copy()):
                temp = act
                if act.startswith('$form'):
                    temp = request.form[act[6::]]
                elif act.startswith('$session'):
                    temp = session[act[9::]]
                actionArr = actionArr[0:index:] + [temp] + actionArr[index+1::]
            action = ' '.join(actionArr)
            print(action)
            print(routename_with_slash)
            result = custom.find_and_run(action, request)
            if 'success_if_true' in source_route and source_route['success_if_true']:
                if result:
                    lesson_success(source_lesson)
        elif source_route['action'] == 'response':
            print('response')
            response = source_route['response']
            flask_response = make_custom_response(response, request)
            return flask_response

        # display results on the html page for the lesson that defines the route
        if source_lesson.load_script is not None:
            result = custom.find_and_run(source_lesson.load_script, request)
            param_dict = {
                    'template_name_or_list':'lesson.html',
                    'title':source_lesson.name,
                    'contentFile':"/content/%s" % source_lesson.content,
                    'lessons':lessons,
                    source_lesson.load_return: result}

            return render_template(**param_dict) 

        return render_template('lesson.html',
           title=source_lesson.name,
           contentFile="/content/%s" % source_lesson.content,
           lessons=lessons)
    else: 
        return(redirect(url_for('login')))

@app.route('/report', methods=['GET'])
def report():
    """ 
    path = /report
    returns the report page
    """

    if 'username' in session:
        global last_loaded
        global start_time

        # update time for latest lesson
        if last_loaded is not None:
            timeToAdd = int(time.time()) - start_time
            update_time(last_loaded, timeToAdd)
            last_loaded = None
            start_time = 0

        get_lesson_stats()

        return render_template('report.html', title="Reporting", lessons=lessons)
    else:
        return redirect(url_for('login'))

load_lessons()
initialize_db()
for lesson in lessons:
    initialize_lesson_db(lesson)
