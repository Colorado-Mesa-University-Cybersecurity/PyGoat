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

#############################################################################################
####################      |          Unit Testing          |     ############################
#######################   ▼   ##########################   ▼   ##############################

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

    else:
        #user already exists in database,
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


#############################################################################################
####################      |      Integration Testing       |     ############################
#######################   ▼   ##########################   ▼   ##############################

#TODO: actually get correct number of completed lessons by interfacing with running flask server
#returns number of completed lessons
def numCompleted():
    num = 0
    for lesson in main.lessons:
        if lesson.completable == True and lesson.completed == True:
            num += 1
    return num

#test curl script solutions in ../solutions/curl_scripts/
#(Move to bash?)
#use actual server?
def test_solutions():
    #collect all available solution scripts
    subdir = os.getcwd().split('PyGoat',1)[-1]
    if len(subdir) == 0:
        path = './'
    else:
        path = '../'

    dir = path+'solutions/curl_scripts/'
    loginScript = 'login.sh'
    
    scriptlist = os.listdir(dir)
    scriptlist.remove(loginScript)

    #launch server
    #actualDir = path + 'run_no_proxy.sh'
    #subprocess.Popen([actualDir], shell=True)
    
    #add test account to actual database
    newUser(path+'pygoat.db')
        
    #login to test account
    rc = subprocess.call(dir+loginScript, shell=True)
    assert(rc == 0)

    #tests that each solution script adds a new (unique) completed lesson
    oldNum = numCompleted()
    fails = []

    oldNum = 0
    for solution in scriptlist:
        rc = subprocess.call(dir + solution, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        newNum = numCompleted()
        try:
            assert(newNum == oldNum + 1)
        except AssertionError:
            fails.append(solution)
        oldNum = newNum

    if len(fails) > 0:
        print('Failed tests: ')
        print(fails)
        assert(len(fails) == 0)


# test_init_database()
# test_solutions()