"""
    All the routes and the lesson helper functions are stored here
"""

from flask import Flask, render_template, session, redirect, url_for, request, flash, Response
from xml.dom.pulldom import START_ELEMENT, parseString
from xml.sax import make_parser
from xml.sax.handler import feature_external_ges
import os, sys, yaml, sqlite3, hashlib, custom, requests, json
from lesson_handler import lesson
from app import path, app, lessons
from network import load_lessons, initialize_db, initialize_lesson_db, valid_login, send_webrequest, make_sql_query, make_custom_response, lesson_success, check_success



@app.route('/favicon.ico')
def favicon():
    """ 
    path = /favicon.ico
    returns the icon 
    """
    return(redirect(url_for('static', filename='favicon.ico')))


def indexRoute(lessons: list):
    @app.route('/')
    def index():
        """ 
        path = /
        if user is logged in, return home page, otherwise, return login page 
        """ 
        if 'username' in session:
            check_success()
            return render_template('index.html', lessons=lessons, title="Lessons", contentFile="doesn't exist")
        else:
            return redirect(url_for('login'))
    return index 

indexRoute(lessons)

@app.route('/login', methods=['POST', 'GET'])
def login():
    """ 
    path = /login
    if user sends GET to this page, returns login html
    if user POSTs this page, checks provided credentials against database, if they login successfully, add their username to the session cookie and redirect to home page
    """ 

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

def lessonStatusRoute(lessons: list):
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
                finalDict[lesson.name]['url'] = lesson.url
                finalDict[lesson.name]['group'] = lesson.group
                finalDict[lesson.name]['pages'] = lesson.pages
                if lesson.completable:
                    finalDict[lesson.name]['completed'] = lesson.completed
            return (json.dumps(finalDict))
        else:
            return redirect(url_for('login'))
    return lessonstatus

lessonStatusRoute(lessons)

# route for every lesson with a yaml config
def lessons_page_route(lessons: list):
    @app.route('/lessons/<lesson>')
    def lessons_page(lesson):
        """ 
        path = /lessons/<lesson>

        parameters:
        lesson - the url field of the lesson to load

        finds the lesson with the url field of lesson, checks if user has completed it, runs any cutom load scripts, and returns the loaded lesson
        """
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
            return render_template("/content/%s" % current_lesson.content,
                    title=current_lesson.name,
                    contentFile="/content/%s" % current_lesson.content,
                    lessons=lessons)
        else:
            return redirect(url_for('login'))
    return lessons_page

lessons_page_route(lessons)


@app.route('/nav/<page>')
def welcomePage(page):
    return render_template('%s.html' % page)


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
        conn = sqlite3.connect('pygoat.db')
        c = conn.cursor()
        c.execute('''UPDATE users SET "%s" = 0 WHERE username = ?''' % colName, [session['username']])
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
        for lesson in lessons:
            colName = "%sCompleted" % lesson.name
            conn = sqlite3.connect('pygoat.db')
            c = conn.cursor()
            c.execute('''UPDATE users SET "%s" = 0 WHERE username = ?''' % colName, [session['username']])
            conn.commit()
            conn.close()
            initialize_lesson_db(lesson)
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
    return render_template('report.html', title="Reporting", lessons=lessons)


load_lessons()
initialize_db()
for lesson in lessons:
    initialize_lesson_db(lesson)
