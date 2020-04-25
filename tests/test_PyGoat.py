import os, sys
import subprocess
import tempfile

import pytest, sqlite3, hashlib

sys.path.append('../')
import main

#test database name (must be different from actual database name)
dbname='testing_pygoat.db'

#sample test user for test database
username = 'testBlankUser'
password = '12345'

#############################################################################################
####################      |          Unit Testing          |     ############################
#######################   ▼   ##########################   ▼   ##############################

#Start new database
def newDatabase():
    assert(not(dbname == 'pygoat.db'))
    try:
        os.remove(dbname)
    except FileNotFoundError:
        pass # already removed, do nothing

    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    c.execute('''CREATE TABLE if not exists users
                    (username text, password blob, salt blob)''')
    conn.commit()

def newUser():
    salt = os.urandom(32)

    m = hashlib.sha256()
    m.update(salt)
    m.update(password.encode('utf-8'))
    pass_hash = m.digest()

    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    c.execute('''INSERT INTO users (username, password, salt) VALUES (?, ?, ?)''', (username, pass_hash, salt))
    conn.commit()
    conn.close()

def test_init_database():
    #create and initialize empty database in test directory
    newDatabase()
    for lesson in main.lessons:
        main.initialize_db(lesson)

    #assert that username doesn't exist in table
    assert(main.valid_login(username, password, dbname=dbname, testing=True) == False)

    newUser()
    
    #assert that the test user exists and starts with no lesson completions
    assert(main.valid_login(username, password, dbname=dbname, testing=True) == True)
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

#returns number of completed lessons
def numCompleted():
    num = 0
    for lesson in main.lessons:
        if lesson.completable == True and numCompleted == True:
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

    dir = path+'/solutions/curl_scripts/'
    scriptlist = os.listdir(dir)

    #launch test server and login?
    #TODO
    actualDir = path + 'run_no_proxy.sh'
    rc = subprocess.Popen(actualDir, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    if main.valid_login(username, password, dbname=dbname, testing=True) == False:


    #tests that each solution script adds a new (unique) completed lesson
    oldNum = numCompleted()
    for solution in scriptlist:
        #navigate to the correct subdirectory
        #TODO

        rc = subprocess.call(dir + solution, shell=True)
        newNum = numCompleted()
        print(solution) # prints the solution that failed trigger a success condition
        assert(newNum == oldNum + 1)
        oldNum = newNum


# test_init_database()
# test_solutions()