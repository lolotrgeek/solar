#Present data

#load dependencies
import geocoder
import datetime

#load layers
import settings
import data

def init():
        
        #Geocode inputlocation
        g = geocoder.google(settings.inputlocation)
        settings.lat = g.lat
        settings.lon = g.lng
        settings.postal = g.postal
        
        r = geocoder.google([g.lat, g.lng], method='reverse')
        settings.state = r.state
        
        #If year not input set to current year
        #if not settings.year:
          #  now = datetime.datetime.now()
            #settings.year = now.year 
        
        #inject data layer
        data.init()