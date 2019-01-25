#!/usr/bin/python

from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
import cgi
import json
import requests

jazz_ep = "https://api.ciscospark.com"
jazz_ep_version = "v1"

gif_ep = "http://www.coegroupllc.com"
gif_path = "/media/images/coegifbot/"

PORT_NUMBER = 8081
BOT_EMAIL = ""
BOT_ID = ""
BOT_ACCESS_TOKEN = ""
AUTH_TOKEN = ""
A_HEADER = ""
A_MESSAGE = ""
A_ROOMID = ""
A_BOTNAMEASTYPED = ""
tmp_header = {"Content-Type" : "application/json"}
tmp_sparkBody = {}
mUrl = jazz_ep + "/" + jazz_ep_version + "/messages"

class coeBotHandler(BaseHTTPRequestHandler):
    #Handle GET requests
    def do_GET(self):
        self.send_error(404,'File Not Found:')
        return

    def do_POST(self):
        # My Post Code will go here
        print(self.headers)
        print(self.path)
        content_len = int(self.headers.getheader('content-length'))
        result=json.loads(self.rfile.read(content_len))
	print("*******\n\n\n\n")
        print("%s" % (result))
	print("************\n\n\n\n\n")
	print("%s\t\t\t\t%s\t\t\t\t\t%s\t%s\n%s\t\t\t%s\t\t\t%s\t%s" % ("Customer ID","User ID","Threat Score","Alarm Type","-------------------","--------------------","-------------","-----------"))
	print("%s\t%s\t%s\t%s" % (result["customer"],result["juid"],result["score"],result["alarm_type"]))
	print("| Sensors")
	print("|-----------")
	for sensor in result['sensors']:
		print("|\n \\\n  -- %s" % (sensor['description']))
	print("%s" & (sensor['agent_uuid']))
        self.send_response(200)
        self.end_headers()
        return

try:
    server = HTTPServer(('', PORT_NUMBER), coeBotHandler)
    print( 'Started httpserver on port %s ' % PORT_NUMBER)
    server.serve_forever()

except KeyboardInterrupt:
    print( 'Kill signal received.  Terminiating server...')
    server.socket.close()
