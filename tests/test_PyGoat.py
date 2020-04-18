import os, sys
import tempfile

import pytest

sys.path.append('../')
import main


# @pytest.fixture
# def client():
#     db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
#     flaskr.app.config['TESTING'] = True

#     with flaskr.app.test_client() as client:
#         with flaskr.app.app_context():
#             flaskr.init_db()
#         yield client

#     os.close(db_fd)
#     os.unlink(flaskr.app.config['DATABASE'])

#Start new database
try:
    os.remove('pygoat.db')
except FileNotFoundError:
    pass # already removed, do nothing

# conn = sqlite3.connect('pygoat.db')
# c = conn.cursor()
# c.execute('''CREATE TABLE if not exists users
#                  (username text, password blob, salt blob)''')
# conn.commit()

def test_init_database():
    #create and initialize empty database in test directory
    for lesson in main.lessons:
        main.initialize_db(lesson)

    #create a test user in test database
    username = 'testBlankUser'
    password = '12345'
    
    #assert that the test user starts with no lesson completions
    if not main.valid_login(username, password):
        assert(False)

    #remove database from test directory
    os.remove('pygoat.db')

    

# def test_make_sql_query():
#     query
#     request
#     main.make_sql_query(query, request)
    