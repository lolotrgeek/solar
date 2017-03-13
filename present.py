#Present data

#load dependencies
import geocoder
import datetime

#load layers
import settings
import data

location = 'chicago'

def init():
        
        if location:
            settings.location = location
            
        #Geocode inputlocation
        g = geocoder.google(settings.location)
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
        
        print settings.location 
        print settings.weather 
        print settings.politics
        print settings.economics
        print settings.demographics
        