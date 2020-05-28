import os, json, subprocess, pytest, time

path = os.path.dirname(os.path.realpath(__file__))
json_name = "final.json"
log_file = "output.log"
os.environ['FLASK_APP']="main.py"

def test_curl_scripts():
    os.chdir('%s/../solutions/curl_scripts/' % path)
    subprocess.run(['./integration_suite.sh'])
    with open(json_name, 'r') as j:
        failed = []
        lessons = json.load(j)
        for name, status in lessons.items():
            print("name")
            if status['completable']:
                if not status['completed']:
                    failed.append(name)
        if len(failed) > 0:
            print(failed)
            assert(False)
        assert(True)
