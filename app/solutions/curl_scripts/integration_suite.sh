#!/bin/bash

SCRIPTPATH="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
PAYLOADPATH="$SCRIPTPATH"/../payloads

pickle="$(python3 "$PAYLOADPATH"/pickle_solution.py "$(cd "$PAYLOADPATH"/../../ >/dev/null 2>&1; pwd)")"

pickle=${pickle:2:$(( ${#pickle} - 3 ))}

./register.sh
./login.sh

session=$(cat cookie.txt | tail -n 1 | cut -f7); 

curl "http://localhost:5000/resetall" -b "cookie.txt"

for i in $(ls *.sh); do
	if [ "$i" != "integration_suite.sh" ] && [ "$i" != "login.sh" ] && [ "$i" != "register.sh" ]; then
		if [ "$i" == "pickle_solution_curl.sh" ]; then
			./"$i" "$session" "$pickle";
		else
			./"$i" "$session"; 
		fi
	fi
done

curl "http://localhost:5000/lessonstatus.json" -b "cookie.txt"

curl "http://localhost:5000/lessons/xxe" -b "cookie.txt"

curl "http://localhost:5000/lessonstatus.json" -b "cookie.txt" > "final.json"

echo "$result"
