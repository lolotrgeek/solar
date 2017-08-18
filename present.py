# Present data

# load dependencies
import datetime
import geocoder

# load layers
import settings
import data

location = 'St. Louis, Mo'
settings.year = '2015'

def init():
    if location:
        settings.location = location
    # Geocode inputlocation
    g = geocoder.google(settings.location)
    settings.lat = g.lat
    settings.lon = g.lng
    settings.postal = g.postal
    # Reverse Geocode
    reverse = geocoder.google([g.lat, g.lng], method='reverse')
    settings.state = reverse.state
    # If year not input set to current year
    if not settings.year:
        now = datetime.datetime.now()
        settings.year = now.year
    #inject data layer
    data.init()
    # Output variables
    print settings.location
    #print settings.weather
    print settings.radiance
    print settings.sky
    print settings.politics
    print settings.economics
    print settings.demographics
        