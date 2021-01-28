#  coding: utf-8 
import socketserver, os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos, Jialin Xie
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        #print ("Got a request of: %s\n" % self.data)

        parameters = self.data.decode().split()
        self.method = parameters[0]
        self.path = parameters[1]
        self.http = parameters[2]
        self.status_200 = "200 OK"
        self.status_301 = "301 Moved Permanently"
        self.status_404 = "404 Not Found"
        self.status_405 = "405 Method Not Allowed"
        
        if self.method != "GET":
            self.send_405_response()

        if self.path.endswith("/"):
            self.path += "index.html"

        if self.path.endswith("html"):
            content_type = "Content-Type: text/html"
            self.send_file_response(content_type)
        elif self.path.endswith("css"):
            content_type = "Content-Type: text/css"
            self.send_file_response(content_type)
        else:
            self.redirect()
    
    def send_file_response(self, content_type):
        file_dir = "./www"
        file_path = file_dir + self.path

        if os.path.exists(file_path):
            content = open(file_path, "r").read()
            content_length = "Content-Length: "+str(len(content))
            response = "{} {}\r\n{}\r\n{}\r\nConnection: close\r\n\r\n{}\r\n".format(
                self.http, self.status_200, content_type, content_length, content)
            self.request.sendall(bytearray(response,'utf-8'))

        else:
            self.send_404_response()
    
    def redirect(self):
        file_dir = "./www"
        file_path = file_dir + self.path + "/index.html"

        if os.path.exists(file_path):
            host_port = "http://127.0.0.1:8080"
            location = "Location: " + host_port + self.path + "/"
            content_type = "Content-Type: text/plain"
            response = "{} {}\r\n{}\r\n{}\r\n\r\n{}\r\n".format(
                self.http, self.status_301, location, content_type, self.status_301)

            self.request.sendall(bytearray(response,'utf-8'))

        else:
            self.send_404_response()

    def send_404_response(self):
        content_type = "Content-Type: text/plain"
        response = "{} {}\r\n{}\r\n\r\n{}\r\n".format(
                self.http, self.status_404, content_type, self.status_404)

        self.request.sendall(bytearray(response,'utf-8'))

    def send_405_response(self):
        
        content_type = "Content-Type: text/plain"
        response = "{} {}\r\n{}\r\n\r\n{}\r\n".format(
                self.http, self.status_405, content_type, self.status_405)

        self.request.sendall(bytearray(response,'utf-8'))

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
