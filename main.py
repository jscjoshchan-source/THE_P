#THE_P

from flask import Flask, request, Response
import requests
from urllib.parse import urlparse

app = Flask(__name__)

COOL_DOMAINS = ['example.com', 'github.com']

@app.route('/p/<path:url>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def p(url):

    p_url = urlparse(url)

    if p_url.hostname not in COOL_DOMAINS:
        return "Domain not allowed", 403

    e_headers = ['content_encoding', 'content-length', 'transfer-encoding', 'connection']
    headers ={k: v for k, v in request.headers if k.lower() not in e_headers}

    try:
        r = requests.request(
            method = request.method,
            url = url,
            headers = headers,
            data = request.get_data(),
            cookies = request.cookies,
            allow_redirects = True,
        )
    except requests.exceptions.RequestException as e:
        return f"errrror: {str(e)}..."
    r_headers = [(k, v) for k, v in r.raw.headers.items() if k.lower() not in e_headers]
    return Response(r.content, r.status_code, r_headers)

if __name__ == '__main__':
    app.run(port=5000)
