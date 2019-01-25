#!/usr/bin/python

from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
import cgi
import json
import requests

spark_ep = "https://api.ciscospark.com"
spark_ep_version = "v1"

gif_ep = "http://www.coegroupllc.com"
gif_path = "/media/images/coegifbot/"

PORT_NUMBER = 8081
BOT_EMAIL = "coegifbot@sparkbot.io"
BOT_ID = ""
BOT_ACCESS_TOKEN = ""
AUTH_TOKEN = ""
A_HEADER = ""
A_MESSAGE = "A message from some Code by Coe, Hello Spark"
A_ROOMID = ""
A_BOTNAMEASTYPED = "Coe "
tmp_header = {"Content-Type" : "application/json"}
tmp_sparkBody = {}
mUrl = spark_ep + "/" + spark_ep_version + "/messages"

class coeBotHandler(BaseHTTPRequestHandler):
    def choose_gif(verb):
        return menu_option(verb)

    def menu_option(itemselected):
        switcher = {
            "allgood" : "allgood",
            "finesse" : "finesse",
            "nothinlikeit" : "nothinlikeit",
            "oh_my" : "oh_my"
        }
        return switcher.get(itemselected, "allgood")
    
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
	print("****\n\n\n\n")
	print(result)
	print("****\n\n\n\n")
        print(result["id"] + ", " + result["name"] + ", " + result["targetUrl"] + ", " + result["data"]["id"] + ", " + result["resource"] + ", " + result["event"])
        print(self.client_address)
        print(self.command)
        mUrl_mod = mUrl + "/" + result["data"]["id"]
        A_ROOMID = result["data"]["roomId"].encode("ascii","replace")
        m_params = {}
        tmp_header["Authorization"] = "Bearer " + BOT_ACCESS_TOKEN
        response = requests.get(mUrl_mod, headers=tmp_header)
        print( "GET %s" % response.status_code)
        print( "GET %s" % response.text)
        result=json.loads(response.text)
        m_filename = result["text"].replace(A_BOTNAMEASTYPED, "") + ".gif"
        m_fileURL = gif_ep + gif_path + m_filename
        print( m_filename)
        print( m_fileURL)
        A_MESSAGE = result["text"].replace(A_BOTNAMEASTYPED, "")
        tmp_sparkBody["text"] = A_MESSAGE
        tmp_sparkBody["roomId"] = A_ROOMID
        tmp_jsonBody = '{"roomId" : "' + A_ROOMID + '", "markdown" : "' + A_MESSAGE + '", "files" : ["' + m_fileURL + '"]}'
        if result["text"].replace("Coe ", "")  == "help":
            # tmp_jsonBody = {}
            # tmp_jsonBody["roomId"] = A_ROOMID
            markdown = ["**You can say:**", "- allgood", "- nothinlikeit", "- oh_my", "- finesse", "- bop", "- thehellyousay"]
            A_MESSAGE = "**You can say:** - allgood - nothinlikeit - oh_my - finesse"
            print( A_MESSAGE)
            #tmp_jsonBody = '{"roomId" : "' + A_ROOMID + '", "markdown" : "' + A_MESSAGE + '"}'
            for message in markdown:
                tmp_jsonBody = '{"roomId": "' + A_ROOMID + '", "markdown": "' +  message + '"}'
                # tmp_jsonBody["markdown"] = message
                #    print( tmp_jsonBody)
                #    print( mUrl)
                response = requests.post(mUrl, data=tmp_jsonBody, headers=tmp_header)
                print( response.status_code)
                print( response.text)
                self.send_response(200)
                self.end_headers()
            return
        response = requests.post(mUrl, data=tmp_jsonBody, headers=tmp_header)
        print("%s, %s" % (response.status_code, response.text))
        print("%s" % tmp_sparkBody)
        print("%s" % tmp_jsonBody)
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
