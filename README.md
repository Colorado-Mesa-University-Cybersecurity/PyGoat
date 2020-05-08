# PyGoat
![travis-build](https://api.travis-ci.com/lawalgren/PyGoat.svg?token=9urrGxcyZzybtwrfmBAk&branch=master)

A Python-based web platform for education in web vulnerabilities. Inspired by WebGoat. https://github.com/WebGoat/WebGoat

Team Members: Lucas Walgren (lawalgren@mavs.coloradomesa.edu), Sean Apsey (ssapsey@mavs.coloradomesa.edu), Taylor Bradshaw (tcbradshaw@mavs.coloradomesa.edu)

Client: Dr. Ram Basnet (rbasnet@coloradomesa.edu)

## Presentation Links

[Showcase Presentation](https://youtu.be/0mHFqdhZoes)

[Showcase PowerPoint Slides](https://docs.google.com/presentation/d/135Wbyiy8HzIIVWsrosy1tvG5uLC9MTfQOtMg5U-h_bY/edit?usp=sharing)

[Addendum Presentation](https://youtu.be/HXRJxJE5eBs)

[Addendum PowerPoint Slides](https://docs.google.com/presentation/d/1_VnXvLU2bU3XCIFi_R8Cf9grZnMgZxvVIuOX-JbrCqI/edit?usp=sharing)

## Installation

* `pip3 install -r requirements.txt --user`

## Running

* `chmod +x run.sh`

* `./run.sh`

* The served web page will be available at http://localhost:5000

## Note About Proxies

* A web proxy like Burp or Zap should work just fine with PyGoat, but if you aren't seeing all the requests, you will have to export the certificate and convert it to a pem file

### Exporting the certificate in burpsuite

* Navigate to proxy->options->import/export ca certificate

* Under export, click 'certificate in DER format' and click next

* choose a location and name for your file and click next to export the certificate

### converting to pem format

* `openssl x509 -inform der -in <new_certificate_name> -out <your_exported_certificate>`

	* e.g. `openssl x509 -inform der -in certificate.cer -out certificate.pem`

### Using the certificate in PyGoat

	* edit run.sh 

		* set "certificate_path" to the absolute path of your newly converted certificate

		* set "http_proxy" to the address and port for your proxy
		
## Creating Custom Lessons

* PyGoat uses yaml files to define its lessons. See [this wiki page](https://github.com/lawalgren/PyGoat/wiki/How-to-create-new-lessons) for more details.
