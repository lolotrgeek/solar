#html.py
#Web UI layer

#load dependencies
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

#load layers
import settings
import present

#Server Details
class Handler(BaseHTTPRequestHandler):
    #Generate HTML
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write("""
            <html><head></head>
            <body>
            <form method="POST">
            your location:
            <input name="location">
            </input>
            <input type="submit" name="submit" value="submit">
            </form>
            </body>
            </html>
            """)
        return
    #Parse Response
    def do_POST(self):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })
        #user input
        inputlocation = form.getvalue("location")
        
        settings.location = inputlocation

        #inject presentation layer
        present.init()
        
		#Display inputlocation
        self.wfile.write(settings.location)
        self.wfile.write(settings.lat)
        self.wfile.write(settings.lon)
        self.wfile.write(settings.state)
        self.wfile.write(settings.postal)
        
		#Display Data
        self.wfile.write(settings.weather) 
        self.wfile.write(settings.politics)
        self.wfile.write(settings.economics)
        self.wfile.write(settings.demographics)
        
        return
 
#Create Server and run	
server = HTTPServer(('', 8181), Handler)
server.serve_forever()