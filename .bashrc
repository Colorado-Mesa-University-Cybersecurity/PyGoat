filename="main.py"
certificate_path="/mnt/c/Users/Nitro/Programming/Sec/Burp/certificate.pem"
http_proxy="http://127.0.0.1:7070"
export FLASK_APP="$filename"
export REQUESTS_CA_BUNDLE="$certificate_path"
export HTTP_PROXY="$http_proxy"
python -m flask run --host localhost

