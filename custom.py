""" 
Put your custom validator functions here. 
You can access them in the lesson configs using $custom.functionName(params).
They will always receive a request object. It can receive other things, just put that as a parameter before the request.
"""

import sqlite3

def find_and_run(action, request):
    end_index = action.find('(')
    func = action[8:end_index:]
    params = action[end_index + 1:-1:].split(',')
    while '' in params:
        params.remove('')
    if len(params) > 0:
        result = globals()[func](*params, request)
    else:
        result = globals()[func](request)
    return result

def validate_proxy(request):
    return request.method == 'GET' and 'X-Request-Intercepted' in request.headers and request.headers['X-Request-Intercepted'] and 'changeMe' in request.args and request.args['changeMe'] == 'Requests are tampered easily'

def sqlValidator(user_data, request):
    if request.method == 'POST':
        if request.form['login'].isnumeric():
            uid = request.form['uid']  
            conn = sqlite3.connect('pygoat.db')
            c = conn.cursor()
            c.execute('''SELECT * FROM user_data where LOGIN_COUNT = %s and USERID = %s''' % (request.form['login'], uid))
            rows = c.fetchall()
            c.execute('''SELECT COUNT() from user_data''')
            length = c.fetchone()[0]
            print(length, rows)
            return len(rows) >= length
