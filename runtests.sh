#!/bin/bash

. assert.sh

filename="main.py"

export FLASK_APP="$filename"

kill "$(ps -aux | grep "python3 -m flask run" | cut -d ' ' -f 5 | head -n 1)"
rm "./solutions/curl_scripts/final.json" 
python3 -m flask run --host localhost >output.log 2>&1 &
sleep 1
pytest="$(python3 -m pytest)"
echo "$pytest"
assert_raises "echo "$pytest" | grep "failed"" 1
sleep 1
kill "$(ps -aux | grep "python3 -m flask run" | cut -d ' ' -f 5 | head -n 1)"
