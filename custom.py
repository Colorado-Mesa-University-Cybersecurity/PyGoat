""" 
Put your custom validator and setup functions here. 
You can access them in the lesson configs using $custom.functionName(params).
They will always receive a request object. It can receive other things, just put that as a parameter before the request.
"""

import sqlite3, os
from xml.dom.pulldom import parseString, START_ELEMENT
from xml.sax import make_parser
from xml.sax.handler import feature_external_ges

# used to store the phoneHome value from the xss lesson
phVal = None

# xml parser for xxe lesson
parser = make_parser()
parser.setFeature(feature_external_ges, True)

# Locate the function string passed here and call the function with any parameters
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

# Validator for the Test Proxy lesson
def validate_proxy(request):
    print(request)
    response = (request.method == 'GET' and 'X-Request-Intercepted' in request.headers and request.headers['X-Request-Intercepted'] and 'changeMe' in request.args and request.args['changeMe'] == 'Requests are tampered easily')
    print(response)
    return response

# Validator for the Test SQL lesson. Runs the query unsafely and ensures all rows are fetched
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
            conn.close()
            return len(rows) >= length

# parse xml unsafely (allowing external entities) and add comment to database
def xxecomment(username, request):
    doc = parseString(request.data.decode('utf-8'), parser=parser)
    for event, node in doc:
        if event == START_ELEMENT and node.tagName == 'text':
            doc.expandNode(node)
            text = node.toxml()
    startInd = text.find('>')
    endInd = text.find('<',startInd)
    text = text[startInd+1:endInd:]
    conn = sqlite3.connect('pygoat.db')
    c = conn.cursor()
    c.execute('''INSERT INTO xxe_comments VALUES (?,?)''', (username, text))
    conn.commit()
    conn.close()

def xxeValidator(request):
    with open('/etc/passwd', 'r') as passwd:
        passwdtxt = ''.join(passwd.readlines()).replace(' ','').replace('\n','')
        print(passwdtxt)
        conn = sqlite3.connect('pygoat.db')
        c = conn.cursor()
        c.execute('''SELECT comment FROM xxe_comments''')
        for row in c.fetchall():
            if row[0].replace(' ', '').replace('\n','') == passwdtxt:
                conn.close()
                return True
        conn.close()
        return(False)

# setup function for the xss lesson. Loads all comments from the database and stores them in a tuple
def render_comments(tablename, request):
    conn = sqlite3.connect('pygoat.db')
    c = conn.cursor()
    result = c.execute('''SELECT * FROM %s''' % tablename).fetchall()
    conn.close()
    return result

# custom action defined in a route for the xss lesson. Receives and stores the last value received from the phoneHome javascript function
def phoneHome(request):
    global phVal
    print(request.form['phVal'])
    phVal = request.form['phVal']

# validator function for the xss lesson. Ensures the value you pass in matches last value received from the phoneHome function
def phoneHomeValidate(request):
    print(phVal, request.form['xsscommentresponse'])
    return request.form['xsscommentresponse'] == phVal
