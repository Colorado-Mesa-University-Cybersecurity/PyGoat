filename="../main.py"

export FLASK_APP="$filename"
python3 -m flask run --host localhost >> log.txt 2>&1 & #

sleep 1
python3 -m pytest
