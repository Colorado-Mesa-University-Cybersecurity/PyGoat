from flask import Flask, render_template, session, redirect, url_for, request, flash
from xml.dom.pulldom import START_ELEMENT, parseString
from xml.sax import make_parser
from xml.sax.handler import feature_external_ges
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

# load in the lessons from the yaml config files
lessons = []
for filename in os.listdir("%s/lessons" % path):
    if filename.endswith('yaml'):
        with open("%s/lessons/%s" % (path, filename), "r") as config:
            config_list = yaml.safe_load(config)
            current_lesson = lesson(config_list)
            lessons.append(current_lesson)

print('Ignore the duplicate column errors below, I had to catch it as a workaround')
for lesson in lessons.copy():
    # add columns to users database tracking lesson completion. 
    # There is no ADD column IF NOT EXISTS in SQLite, so just catching the error will have to do for now 
    if lesson.completable:
        colName = "%sCompleted" % lesson.name
        try:
            c.execute('''ALTER TABLE users ADD "%s" integer''' % colName) 
        except sqlite3.DatabaseError as e:
            print(e)
conn.commit()
conn.close()

def initialize_db(lesson):
    conn = sqlite3.connect('pygoat.db')
    c = conn.cursor()
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

# send an arbitrary web request using route actions in the config files
def send_webrequest(webrequest, request):
    url = "http://localhost:5000%s" % webrequest['url']
    headers = {}
    if 'headers' in webrequest:
        for header,value in webrequest['headers'].items():
            tempheader = ""
            tempbody = ""
            if header.startswith('$form'):
                tempheader = request.form[header[6::]]
            elif header.startswith('$session'):
                tempheader = request.session[header[9::]]
            else:
                tempheader = header
            if value.startswith('$form'):
                tempbody = request.form[value[6::]]
            elif value.startswith('$session'):
                tempbody = request.session[value[9::]]
            else:
                tempbody = value
            headers[tempheader] = tempbody
               
    headers['cookie'] = 'session=' + request.cookies['session']
    if 'body' in webrequest:
        if isinstance(webrequest['body'], str):
            bodyArr = webrequest['body'].split(' ')
            for index, val in enumerate(bodyArr.copy()):
                tempval = ""
                if val.startswith('$form'):
                    tempval = request.form[val[6::]]
                elif val.startswith('$session'):
                    tempval = request.form[val[9::]]
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
                    tempkey = request.session[key[9::]]
                else:
                    tempkey = key
                if value.startswith('$form'):
                    tempvalue = request.form[value[6::]]
                elif value.startswith('$session'):
                    tempvalue = request.session[value[9::]]
                else:
                    tempvalue = value
                body[tempkey] = tempvalue


    if webrequest['method'] == 'POST':
            requests.post(url, data=body, headers=headers)
    elif webrequest['method'] == 'GET':
            requests.get(url, headers=headers, params=body)

# make arbitrary sql queries using route actions in the config files
# replace $form and $session primitives with their counterparts in the request
# if designated injectable, pass the parameters into the query as strings, otherwise pass in a prepared statement
# will probably break if you want non-injectable sql and variable tables or column names
def make_sql_query(query, request):
    conn = sqlite3.connect('pygoat.db')
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

def check_success():
    conn = sqlite3.connect('pygoat.db')
    c = conn.cursor()
    for lesson in lessons:
        if lesson.completable:
            colName = "%sCompleted" % lesson.name
            c.execute('''SELECT "%s" FROM users WHERE username = ?''' % colName, [session['username']])
            if c.fetchone()[0] == 1:
                lesson.completed = True
            else:
                lesson.completed = False
    conn.close()

@app.route('/favicon.ico')
def favicon():
    return(redirect(url_for('static', filename='favicon.ico')))

@app.route('/')
def index():
    if 'username' in session:
        check_success()
        return render_template('lesson.html', lessons=lessons, title="Lessons", contentFile="doesn't exist")
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None 
    if request.method == 'POST':
        if valid_login(request.form['username'], request.form['password']):
            session['username'] = request.form['username']
            check_success()
            return redirect(url_for('index'))
    return render_template('login.html', login=True)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

# route for every lesson with a yaml config
@app.route('/lessons/<lesson>')
def lessons_page(lesson):
    if 'username' in session:
        check_success()
        # get lesson with url passed into the route
        current_lesson = next(filter(lambda x:x.url == lesson, lessons))


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
    lesson = next(filter(lambda x:x.url == lessonTitle, lessons))
    colName = "%sCompleted" % lesson.name
    conn = sqlite3.connect('pygoat.db')
    c = conn.cursor()
    c.execute('''UPDATE users SET "%s" = 0 WHERE username = ?''' % colName, [session['username']])
    conn.commit()
    conn.close()
    initialize_db(lesson)
    return redirect(url_for('lessons_page', lesson=lesson.url))

# addtional routes defined in the yaml configs
@app.route('/<routeName>', methods=['POST', 'GET'])
def custom_routes(routeName):
    if 'username' in session:
        check_success()
        routename_with_slash = '/' + routeName

        # determine which lesson this route is attached to. This might be slow with a lot of lessons
        source_lesson = next(filter(lambda x: x.routes is not None and len(list(filter(lambda y: y['path'] == routename_with_slash,x.routes))) > 0, lessons))

        # determine which route in said lesson got us here
        source_route = next(filter(lambda x: x['path'] == routename_with_slash, source_lesson.routes))

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

if __name__ == '__main__':
        # initialize database tables using the 'db-tables' value from the yaml configs
        # there is some insecure SQL going on here, but SQLite doesn't let you parameterize table or column names,
        # so it couldn't be avoided
        initialize_db(lesson)

