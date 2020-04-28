import os, sys
import subprocess
import tempfile

import pytest, sqlite3, hashlib
import requests

sys.path.append('../')
import main
#import main creates new instance of pygoat.db in tests directory, delete
#os.remove('pygoat.db')

#sample test user for test database
username = 'test'
password = '12345'

dbname = 'testing_pygoat.db'

def newUser(_dbname = dbname):
    #only try to add new user to database if user doesn't already exist
    if main.valid_login(username, password, _dbname, testing=True) == False:
        requests.post('http://localhost:5000/register', data={'username':username, 'password':password})

    else: #user already exists in database,
        pass

#TODO: actually get correct number of completed lessons by interfacing with running flask server
#returns number of completed lessons
def numCompleted():
    num = 0
    #requests.get('http://localhost:5000/lessonstatus')
    assert(False)
    for lesson in main.lessons:
        if lesson.completable == True and lesson.completed == True:
            num += 1
    return num

#test curl script solutions in ../solutions/curl_scripts/
#must have actual server running
#TODO: verify curl scripts work with test account
#TODO: verify curl scripts work
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