import requests
import json

ip = ""
port = 8888

def get_token():
    url = "http://192.168.10.1:8000/api/v1/token/"
    headers = { "Content-Type" : "application/json" }
    response = requests.get(url=url,headers=headers)
    print(response)
    print(response.text)
    dict_response = json.loads(response.text)
    print(dict_response["token"])
    print(type(dict_response["token"]))
    return dict_response["token"]


from http.server import HTTPServer, BaseHTTPRequestHandler

host = ("", port)

class Resquest(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        data = {"token": get_token()}
        self.wfile.write(json.dumps(data).encode())

def start_server():
    server = HTTPServer(host,Resquest)
    print("Starting server, listen at:%s:%s" % host )
    server.serve_forever()

start_server()