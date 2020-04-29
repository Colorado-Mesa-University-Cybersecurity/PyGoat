import os, sys
import subprocess
import tempfile

import pytest, sqlite3, hashlib
import requests

path = os.path.dirname(os.path.realpath(__file__))
os.chdir(path)
sys.path.append('../')
import main

#test database name (must be different from actual database name)
dbname='test.db'

#sample test user for test database
username = 'test'
password = '12345'

#Start new database
def newDatabase():
    try:
        os.remove(dbname)
    except FileNotFoundError:
        pass # already removed, do nothing
    
    main.initialize_db(dbname=dbname)

def newUser():
    #only try to add new user to database if user doesn't already exist
    if main.valid_login(username, password, dbname=dbname, testing=True) == False:
#        requests.post('http://localhost:5000/register', data={'username':username, 'password':password})
        conn = sqlite3.connect(dbname)
        c1 = conn.cursor()
        salt = os.urandom(32)

        m = hashlib.sha256()
        m.update(salt)
        m.update(password.encode('utf-8'))
        pass_hash = m.digest()

        c1.execute('''INSERT INTO users (username, password, salt) VALUES (?, ?, ?)''', (username, pass_hash, salt))
        conn.commit()
        conn.close()

    else: #user already exists in database,
        pass

def test_init_database():
    #create and initialize empty database in test directory
    newDatabase()
    for lesson in main.lessons:
        main.initialize_lesson_db(lesson, dbname=dbname)

    #assert that username doesn't exist in table
    assert(main.valid_login(username, password, dbname=dbname, testing=True) == False)

    #add username to table
    newUser()
    
    #assert that the test user exists in table
    assert(main.valid_login(username, password, dbname=dbname, testing=True) == True)
    #assert that test user has not completed any lessons
    for lesson in main.lessons:
        if lesson.completable == True:
            assert(lesson.completed == False)

def test_send_webrequest():
    webrequest = {'url': '/url', 'headers':{'Content-Type': 'application/x-www-form-urlencoded'}, 'body':{'name':'bob', 'passw':'1234'}}
    url, headers, body = main.send_webrequest(webrequest, url="http://localhost:5000", testing=True)
    assert(url == 'http://localhost:5000%s' % webrequest['url'] and body == webrequest['body'] and headers == webrequest['headers'])

def test_make_sql_query():
    query = {'injectable':False, 'qstring':"INSERT INTO users ('username', 'password','salt') VALUES('Bob','asdf2q30', '1230sdf030948')"}
    main.make_sql_query(query, dbname=dbname, testing=True)
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    c.execute('''SELECT username FROM users WHERE username="Bob"''')
    rows = c.fetchall()
    assert(len(rows) > 0)

def test_make_response():
    response = {'headers':{'Content-Type':'application/text'},'body':'thisisatest'}
    body, headers = main.make_custom_response(request=None, response=response, testing=True)
    assert(headers == response['headers'] and body == response['body'])

# def test_make_sql_query():
#     query
#     request
#     main.make_sql_query(query, request)
