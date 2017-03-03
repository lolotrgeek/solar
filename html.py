#html.py
#generate html UI, parse inputs

#inject dependencies
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
import geocoder

import settings
import data

class Handler(BaseHTTPRequestHandler):
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

    def do_POST(self):
        form = cgi.FieldStorage(
            fp=self.rfile, 
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })
        inputlocation = form.getvalue("location")
		
        g = geocoder.google(inputlocation)
        settings.lat = g.lat
        settings.lon = g.lng		
		
		
		
        self.wfile.write(inputlocation)
        self.wfile.write(settings.lat)
        self.wfile.write(settings.lon)
		
		#inject data layer
        data.init()
		
        self.wfile.write(settings.info)		
        return
	
server = HTTPServer(('', 8181), Handler)
server.serve_forever()