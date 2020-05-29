filename="main.py"
certificate_path="/home/lucas/certificate.pem"
http_proxy="http://127.0.0.1:8082"
export FLASK_APP="$filename"
export REQUESTS_CA_BUNDLE="$certificate_path"
export HTTP_PROXY="$http_proxy"
python3 -m flask run --host localhost
