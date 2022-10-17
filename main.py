from antlr4 import *
from functools import partial
from gen.TablParser import TablParser
from gen.TablVisitor import TablVisitor
from gen.tablLexer import TablLexer
import requests
from http.server import BaseHTTPRequestHandler, HTTPServer
import time

class MyServer(BaseHTTPRequestHandler):
    def __init__(self, picLink, *args, **kwargs):
        self.picLink = picLink
        super().__init__(*args, **kwargs)

    def do_GET(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(self.picLink, 'utf-8'))

class Resource:
    def __init__(self, name, limit, picture):
        self.name = name
        self.limit = limit
        self.supply = limit
        #self.picture = picture
        response = requests.get(f"https://api.pexels.com/v1/search?query={picture}", headers={"Authorization" : "563492ad6f917000010000014363b809657648f1a8b3df00ea4eb9e2"})
        self.pictureUrl = response.json()['photos'][0]['src']['small']
        print(self.pictureUrl)

    def __str__(self):
        return f'{self.name}: {self.supply}, max: {self.limit}'

    def take(self, num):
        if self.limit == 0:
            return num
        if self.supply > 0:
            toRet = min(num, self.supply)
            self.supply = max(0, self.supply - num)
            return toRet
        return False

    def restore(self, num):
        if self.limit != 0:
            self.supply += num

class Player:
    def __init__(self, resources):
        self.resources = {}
        for resource, number in resources.items():
            self.resources[resource] = number

    def __str__(self):
        return f'{self.resources}'

if __name__ == '__main__':
    inputStream = FileStream("sample.txt")
    lexer = TablLexer(inputStream)
    stream = CommonTokenStream(lexer)
    parser = TablParser(stream)
    tree = parser.rules()
    print(tree)
    visitor = TablVisitor()
    visitor.visit(tree)

    myResource = Resource('Gold token', 100, 'gold token')

    player1 = Player({'alma': 10, 'felma': 5})
    print(player1)

    hostName = 'localhost'
    serverPort = 8080

    handler = partial(MyServer, myResource.pictureUrl)
    webServer = HTTPServer((hostName, serverPort), handler)
    print(f'server started, http://{hostName}:{serverPort}')
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print('server stopped')







