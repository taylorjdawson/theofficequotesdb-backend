import cgi
import json

import re
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib import parse
from urllib.parse import urlparse, parse_qs, unquote
# from DeployableServer.github_issue import make_github_issue

from DeployableServer.ElasticSearchClient import ElasticSearchClient
from DeployableServer.github_issue import make_github_issue

es = ElasticSearchClient()
# es.indexES()
# This class will handles any incoming request from
# the browser
class myHandler(BaseHTTPRequestHandler):

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

    # Handler for the GET requests
    def do_GET(self):
        self._set_headers()

        #Grab path parameters
        params = parse_qs(urlparse(self.path).query)

        # issue = params['issue']

        #TODO: Possible Handle a redirect for going to watch video

        # Try to grab the command group from the match object
        try:
            query = params['search'][0]

            # Send query to Elasticsearch Client
            results = es.search(query)

        except AttributeError:
            results = ''

        self.wfile.write(json.dumps(results).encode())
        return

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        self._set_headers()
        request_path = self.path

        request_headers = self.headers
        content_length = request_headers.get('content-length')
        length = int(content_length) if content_length else 0

        data = unquote(self.rfile.read(length).decode("utf-8"))

        data = unquote(data)
        print(data)

        m = re.match("issue_type=(?P<issue_type>.*)&issue_text=(?P<issue_text>.*)&line_id=(?P<line_id>.*)&line=(?P<line>.*)"
                     , data)

        issue_content = dict(zip(("type", "message", "line_id", "line"), m.groups()))

        status = make_github_issue(issue_content)

        self.wfile.write(json.dumps(status).encode())

    #  "issue_type=Broken+Link&issue_text="
    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        # self.send_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

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