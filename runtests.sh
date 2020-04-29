#!/bin/bash

. assert.sh

filename="main.py"

export FLASK_APP="$filename"

pid="$(ps axo args,pid | grep "python3 -m flask" | cut -d ' ' -f6)"
if [ "$pid" != '' ]; then
	kill "$pid"
fi

rm "./solutions/curl_scripts/final.json" 
python3 -m flask run --host localhost >output.log 2>&1 &
sleep 1
pytest="$(python3 -m pytest)"
echo "$pytest"
assert_raises "echo "$pytest" | grep "failed"" 1
sleep 1

pid="$(ps axo args,pid | grep "python3 -m flask" | cut -d ' ' -f6)"
if [ "$pid" != '' ]; then
	kill "$pid"
fi
