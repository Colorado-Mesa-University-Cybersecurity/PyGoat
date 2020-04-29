import os, sys
import subprocess
import tempfile

import pytest, sqlite3, hashlib
import requests

sys.path.append('../')
import main
#import main creates new instance of pygoat.db in tests directory, delete
os.remove('pygoat.db')

#test database name (must be different from actual database name)
dbname='testing_pygoat.db'

#sample test user for test database
username = 'test'
password = '12345'

#Start new database
def newDatabase():
    try:
        os.remove(dbname)
    except FileNotFoundError:
        pass # already removed, do nothing

    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    c.execute('''CREATE TABLE if not exists users
                    (username text, password blob, salt blob)''')
    conn.commit()

def newUser(_dbname = dbname):
    #only try to add new user to database if user doesn't already exist
    if main.valid_login(username, password, _dbname, testing=True) == False:
        requests.post('http://localhost:5000/register', data={'username':username, 'password':password})

    else: #user already exists in database,
        pass

def test_init_database():
    #create and initialize empty database in test directory
    newDatabase()
    for lesson in main.lessons:
        main.initialize_db(lesson, dbname=dbname)

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

# def test_make_sql_query():
#     query
#     request
#     main.make_sql_query(query, request)
