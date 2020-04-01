""" 
Put your custom validator and setup functions here. 
You can access them in the lesson configs using $custom.functionName(params).
They will always receive a request object. It can receive other things, just put that as a parameter before the request.
"""

import sqlite3, os, pickle, filecmp, urllib, time
from flask import flash
from xml.dom.pulldom import parseString, START_ELEMENT
from xml.sax import make_parser
from xml.sax.handler import feature_external_ges

# used to store the phoneHome value from the xss lesson
phVal = None

path = os.path.dirname(os.path.realpath(__file__))

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
    response = (request.method == 'GET' and 'X-Request-Intercepted' in request.headers and request.headers['X-Request-Intercepted'] and 'changeMe' in request.args and request.args['changeMe'] == 'Requests are tampered easily')
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
            conn.close()
            return len(rows) >= length

# parse xml unsafely (allowing external entities) and add comment to database
def xxecomment(username, request):
    parser = make_parser()
    parser.setFeature(feature_external_ges, True)
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
    phVal = request.form['phVal']

# validator function for the xss lesson. Ensures the value you pass in matches last value received from the phoneHome function
def phoneHomeValidate(request):
    return request.form['xsscommentresponse'] == phVal

def csrf_validate_and_comment(username, request):
    if request.method == "POST":
        if  'Referer' in request.headers and 'localhost:5000' in request.headers['Referer']:
            flash(('danger', 'It appears your request is coming from the same host you are submitting to.'))
            return False
        elif 'validateReq' in request.form and request.form['validateReq'] == '2aa14227b9a13d0bede0388a7fba9aa9':
            conn = sqlite3.connect('pygoat.db')
            c = conn.cursor()
            c.execute('''INSERT INTO csrf_comments VALUES (?,?,?)''', (username, request.form['csrfcontent'], request.form['stars']))
            conn.commit()
            conn.close()
            return True

def insecure_deserialization_validate(request):
    if request.method == "POST":
        try:
            os.remove('%s/passwdclone' % path)
        except OSError as error:
            print(error)
        # had to remove url encoding and unescape backslashes. See https://stackoverflow.com/questions/1885181/how-to-un-escape-a-backslash-escaped-string
        og_result = request.get_data()[7::]
        result = urllib.parse.unquote_to_bytes(og_result).decode('unicode_escape')
        # nbspaces were added by parsing unicode escape, remove them
        result = result.encode('utf-8').replace(b'\xc2', b'')
        obj = pickle.loads(result)
        time.sleep(0.5) 
        if 'passwdclone' in os.listdir(path) and filecmp.cmp('/etc/passwd', '%s/passwdclone' % path):
            print('done')
            flash(('success','lesson completed'))
            return True
    return False
