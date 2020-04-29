#!/bin/bash

. assert.sh

filename="main.py"

export FLASK_APP="$filename"

kill "$(ps axo args,pid | grep "python3 -m flask" | cut -d ' ' -f7)"
rm "./solutions/curl_scripts/final.json" 
python3 -m flask run --host localhost >output.log 2>&1 &
sleep 1
pytest="$(python3 -m pytest)"
echo "$pytest"
assert_raises "echo "$pytest" | grep "failed"" 1
sleep 1
kill "$(ps axo args,pid | grep "python3 -m flask" | cut -d ' ' -f7)"
