import json
import re
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib import parse

# from DeployableServer.github_issue import make_github_issue

from DeployableServer.ElasticSearchClient import ElasticSearchClient

es = ElasticSearchClient()
# This class will handles any incoming request from
# the browser
class myHandler(BaseHTTPRequestHandler):

    # Handler for the GET requests
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()





        #Decode path
        path = parse.unquote(self.path)

        # Check to see if the URL matches
        search = re.match('/\?search=(?P<query>.*)', path)
        # issue = re.match('/issue/')


        # Try to grab the command group from the match object
        try:
            query = search.group('query')

        except AttributeError:
            query = ''

        #Send query to Elasticsearch Client
        results = es.search(query)

        # self.wfile.write(json.dumps(results).encode())
        print(results)
        return

    def do_POST(self):
        content_len = int(self.headers.getheader('content-length'))
        post_body = self.rfile.read(content_len)
        self.send_response(200)
        self.end_headers()

        print(content_len)
        print(json.dumps(post_body, indent=True))

try:
    # Grab the port number from the command line argument
    port_number = int(9220)

    # Create a web server and define the handler to manage the
    # incoming request
    server = HTTPServer(('', port_number), myHandler)
    print('Started httpserver on port ', port_number)

    # Wait forever for incoming http requests
    server.serve_forever()

except KeyboardInterrupt:
    print('^C received, shutting down the web server')
    server.socket.close()