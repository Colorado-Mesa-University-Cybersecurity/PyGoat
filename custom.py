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


path = os.path.dirname(os.path.realpath(__file__))

# used to store the phoneHome value from the xss lesson
phVal = None

def find_and_run(action, request):
    """
    Locates the function string passed here and call the function with any parameters
    params:
    action - the function to run
    request - a flask Request object
    """

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
    """
    Validator for the Test Proxy lesson
    request - a flask request object
    """
    response = (request.method == 'GET' and 'X-Request-Intercepted' in request.headers and request.headers['X-Request-Intercepted'] and 'changeMe' in request.args and request.args['changeMe'] == 'Requests are tampered easily')
    if response:
        flash(('success', 'lesson completed'))
    return response

def sqlValidator(user_data, request):
    """
    Validator for the Test SQL lesson. Runs the query unsafely and ensures all rows are fetched
    user_data - irrelevant - TODO delete
    request - a flask request object
    """
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
            response = (len(rows) >= length)
            if response:
                flash(('success', 'lesson completed'))
            return response

def xxecomment(username, request):
    """
    parse xml unsafely (allowing external entities) and add comment to database
    username - username of PyGoat user
    request - a flask request object
    """
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
    """
    checks to see if the XXE lesson is completed. If a comment in the table matches the host's /etc/passwd file, then return True
    request - a flask request object
    """
    with open('/etc/passwd', 'r') as passwd:
        passwdtxt = ''.join(passwd.readlines()).replace(' ','').replace('\n','')
        conn = sqlite3.connect('pygoat.db')
        c = conn.cursor()
        c.execute('''SELECT comment FROM xxe_comments''')
        for row in c.fetchall():
            if row[0].replace(' ', '').replace('\n','') == passwdtxt:
                conn.close()
                flash(('success', 'lesson completed'))
                return True
        conn.close()
        return(False)

def render_comments(tablename, request):
    """
    setup function for lessons with comments. Loads all comments from the database and stores them in a tuple

    tablename - the name of the table to load comments from
    request - a flask request object
    """
    conn = sqlite3.connect('pygoat.db')
    c = conn.cursor()
    result = c.execute('''SELECT * FROM %s''' % tablename).fetchall()
    conn.close()
    return result

def phoneHome(request):
    """
    custom action defined in a route for the xss lesson. Receives and stores the last value received from the phoneHome javascript function
    request - a flask request object
    """
    global phVal
    phVal = request.form['phVal']

def phoneHomeValidate(request):
    """
    validator function for the xss lesson. Ensures the value you pass in matches last value received from the phoneHome function
    request - a flask request object
    """
    response = request.form['xsscommentresponse'] == phVal
    if response:
        flash(('success', 'lesson completed'))
    return response

def csrf_validate_and_comment(username, request):
    """
    validator function defined for the CSRF lesson. checks if request came from same host. If not, and the validateReq field contains the right value, insert a comment and complete the lesson
    request - a flask request object
    """
    if request.method == "POST":
        if  'Referer' in request.headers and ('localhost:5000' in request.headers['Referer'] or '127.0.0.1:5000' in request.headers['Referer']):
            flash(('danger', 'It appears your request is coming from the same host you are submitting to.'))
            return False
        elif 'validateReq' in request.form and request.form['validateReq'] == '2aa14227b9a13d0bede0388a7fba9aa9':
            conn = sqlite3.connect('pygoat.db')
            c = conn.cursor()
            c.execute('''INSERT INTO csrf_comments VALUES (?,?,?)''', (username, request.form['csrfcontent'], request.form['stars']))
            conn.commit()
            conn.close()
            flash(('success', 'lesson completed'))
            return True

def insecure_deserialization_validate(request):
    """
    validator function for the insecure deserialization lesson
    Unpickles the string passed into the field and checks to see if they've created a copy of the /etc/passwd file in their PyGoat install directory
    request - a flask request object
    """
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

def validate_idor(request):
    """
    validator for the IDOR lesson. If they type in the other username they could access (Blackbeard), return true 
    request - a flask request object
    """
    if request.method == "POST" and 'username' in request.form and request.form['username'] == 'Blackbeard':
        flash(('success', 'Lesson completed'))
        return True
    return False
