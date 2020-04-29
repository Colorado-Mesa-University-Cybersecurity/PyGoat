filename="main.py"

export FLASK_APP="$filename"

kill $(ps -aux | grep "python3 -m flask run" | cut -d ' ' -f 6 | head -n 1)
rm "./solutions/curl_scripts/final.json" 
python3 -m flask run --host localhost >output.log 2>&1 &
sleep 1
python3 -m pytest
