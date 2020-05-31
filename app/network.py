import os, yaml, sqlite3, hashlib, requests
from flask import session, redirect, flash, Response
import logging
from lesson_handler import lesson



def load_lessons(lessondir: str, lessons: list) -> None:
    """ 
        load in the lessons from the yaml config files
        lessondir = string - the absolute path of the directory where the lesson 
        yaml configs are stored
    """

    for filename in os.listdir(lessondir):
        if filename.endswith('yaml'):
            with open("%s/%s" % (lessondir, filename), "r") as config:
                config_list = yaml.safe_load(config)
                current_lesson = lesson(config_list)
                lessons.append(current_lesson)



def initialize_db(lessons: list, dbname='pygoat.db') -> None:
    """ 
        initialize the 'users' table
        dbname = string - the name of the database to use 
    """

    logging.info('Ignore the duplicate column errors below, I had to catch it as a workaround') # print('Ignore the duplicate column errors below, I had to catch it as a workaround')

    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    c.execute('''CREATE TABLE if not exists users
                     (username text, password blob, salt blob)''')
    conn.commit()

    for lesson in lessons.copy():
        # add columns to users database tracking lesson completion. 
        # There is no ADD column IF NOT EXISTS in SQLite, so just catching the error will have to do for now 
        if lesson.completable:
            colName: str = f'{lesson.name}Completed' # colName: str = "%sCompleted" % lesson.name
            try:
                c.execute('''ALTER TABLE users ADD "%s" integer''' % colName) 
            except sqlite3.DatabaseError as e:
                logging.info(e)  # print(f'logging:{e}')

    conn.commit()
    conn.close()



def initialize_lesson_db(lesson, dbname='pygoat.db') -> None:
    """ 
        initialize the custom database tables defined in the lesson yamls
        lesson = lesson object - a lesson object obtained from reading in a lesson
          yaml file
        dbname = string - the name of the database to use
    """

    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    logging.info('initializing %s' % lesson.name) # print('initializing %s' % lesson.name)
    if lesson.db_tables is not None:
        for table in lesson.db_tables:
            try: 
                c.execute('''DROP TABLE %s''' % table['name'])
                conn.commit()
            except sqlite3.DatabaseError as e:
                print(f'Error Restart program to access following: {e}')
                print('This error always occurs upon first launch, do not worry')
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



def valid_login(username, password, dbname='pygoat.db', testing=False) -> bool:
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

    url: str = f'{url}{webrequest["url"]}' # url: str = "%s%s" % (url, webrequest['url'])
    headers: dict = {}
    body: dict = {}
    if 'headers' in webrequest:
        for header,value in webrequest['headers'].items():
            tempheader: str = ""
            tempbody: str = ""
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
                tempval: str = ""
                if val.startswith('$form'):
                    tempval = request.form[val[6::]]
                elif val.startswith('$session'):
                    tempval = session[val[9::]]
                else:
                    tempval = val
                bodyArr = bodyArr[0:index:] + [tempval] + bodyArr[index+1::]
            body: str = ' '.join(bodyArr)
                    
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



def make_sql_query(query, request=None, dbname='pygoat.db', testing=False) -> None:
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
    parameters: list = []
    qstring = query['qstring']
    # the below line is why each $form and $session primitive need to be surrounded by spaces, 
    # otherwise it will try to read bad form values and throw 400 errors
    qstringArr: list = qstring.split(' ')

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


        qstring: str = " ".join(qstringArr)
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

    headers: dict = {}
    body: dict = {}

    if 'headers' in response:
        for header, value in response['headers'].items():
            tempheader: str = ""
            tempbody: str = ""
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
        headers['cookie'] = f'session={request.cookies["session"]}' # headers['cookie'] = 'session=' + request.cookies['session']

    if 'body' in response:
        if isinstance(response['body'], str):
            bodyArr: list = response['body'].split(' ')
            for index, val in enumerate(bodyArr.copy()):
                tempval: str = ""
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

    colName: str = f"{lesson.name}Completed" # colName: str = "%sCompleted" % lesson.name
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    c.execute('''UPDATE users SET "%s" = 1 WHERE username = ?''' % colName, [session['username']])
    conn.commit()
    conn.close()
    if not testing:
        return(redirect('/lessons/%s' % lesson.url))



def check_success(lessons: list, dbname='pygoat.db') -> None:
    """
        loops through the lessons and checks to see if any of them are completed,
        if so, sets the completed variable in said lesson to true, otherwise, sets it to false

        dbname = string - the name of the database to use
    """

    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    for lesson in lessons:
        if lesson.completable:
            colName: str = f"{lesson.name}Completed" # colName: str = "%sCompleted" % lesson.name
            c.execute('''SELECT "%s" FROM users WHERE username = ?''' % colName, [session['username']])
            result = c.fetchone()
            if result is not None and result[0] == 1:
                lesson.completed = True
            else:
                lesson.completed = False
    conn.close()



def start(lessons: list, path: str) -> None:
    ''' Function initializes database after loading lessons '''
    
    load_lessons(f'{path}/lessons', lessons) # lessondir="%s/lessons" % path
    initialize_db(lessons)
    for lesson in lessons:
        initialize_lesson_db(lesson)
