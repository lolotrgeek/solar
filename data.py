#data.py
#connect to datasources

#load dependencies
import pandas as pd
import numpy as np
import requests
import json
import sys, os

#load data libraries
from census import Census
from us import states
from censusgeocode import CensusGeocode

#load layers
import settings

def init():
    
    #clean globals
    lat = settings.lat
    lon = settings.lon
    state = settings.state
    postal = settings.postal
    year = settings.year
    
    # --------------------------------------------------------------------------------------------------------------------------------
    # WEATHER DATA - NSRDB  - https://nsrdb.nrel.gov/api-instructions
    # --------------------------------------------------------------------------------------------------------------------------------
    # Declare all variables as strings. Spaces must be replaced with '+', i.e., change 'John Smith' to 'John+Smith'.

    # You must request an NSRDB api key from the link above
    api_key = 'JJQmF8CNU7qDCgGptU1krnjESLAa4RBzH2aOaOrs'
    # Set the attributes to extract (e.g., dhi, ghi, etc.), separated by commas.
    attributes = 'ghi,dhi,dni,wind_speed_10m_nwp,surface_air_temperature_nwp,solar_zenith_angle'
    # Choose year of data
    #year = '2015'
    # Set leap year to true or false. True will return leap day data if present, false will not.
    leap_year = 'false'
    # Set time interval in minutes, i.e., '30' is half hour intervals. Valid intervals are 30 & 60.
    interval = '30'
    # Specify Coordinated Universal Time (UTC), 'true' will use UTC, 'false' will use the local time zone of the data.
    # NOTE: In order to use the NSRDB data in SAM, you must specify UTC as 'false'. SAM requires the data to be in the
    # local time zone.
    utc = 'true'
    # Your full name, use '+' instead of spaces.
    your_name = 'Jon+James'
    # Your reason for using the NSRDB.
    reason_for_use = 'Find+best+places+to+put+solar+panels.'
    # Your affiliation
    your_affiliation = 'simplyenable'
    # Your email address
    your_email = 'jon@simplyenable.com'
    # Please join our mailing list so we can keep you up-to-date on new developments.
    mailing_list = 'false'

    # Declare url string
    nsrdb = 'http://developer.nrel.gov/api/solar/nsrdb_0512_download.csv?wkt=POINT({lon}%20{lat})&names={year}&leap_day={leap}&interval={interval}&utc={utc}&full_name={name}&email={email}&affiliation={affiliation}&mailing_list={mailing_list}&reason={reason}&api_key={api}&attributes={attr}'.format(year=year, lat=lat, lon=lon, leap=leap_year, interval=interval, utc=utc, name=your_name, email=your_email, mailing_list=mailing_list, affiliation=your_affiliation, reason=reason_for_use, api=api_key, attr=attributes)
    # Return just the first 2 lines to get metadata:
    weather = pd.read_csv(nsrdb, nrows=1)
    # See metadata for specified properties, e.g., timezone and elevation
    timezone, elevation = weather['Local Time Zone'], weather['Elevation']

    radiance = weather['Fill Flag 2']

    sky = weather['Fill Flag 3']
    
    settings.weather = weather
    settings.radiance = radiance
    settings.sky = sky
        
    # --------------------------------------------------------------------------------------------------------------------------------
    # POLITICAL DATA - DSIRE - http://www.dsireusa.org/resources/data-and-tools/
    # --------------------------------------------------------------------------------------------------------------------------------

    dsire = 'http://programs.dsireusa.org/api/v1/getprograms/json?fromSir=0&state={state}'.format(state=state)
    
    polreq = requests.get (dsire)
    
    settings.politics = polreq.json
    
    
    # --------------------------------------------------------------------------------------------------------------------------------
    # ECONOMIC DATA - EIA - https://www.eia.gov/opendata/commands.php
    # --------------------------------------------------------------------------------------------------------------------------------
    
    eia_key = 'afe0bc288e7de03842e061ac596b9301'
    
    #series IDs found from data browser - https://www.eia.gov/electricity/data/browser/
    #timeline
    monthly = 'M'
    quarterly = 'Q'
    yearly = 'Y'
    
    timeline = monthly
    
    #sector
    all = 'ALL'
    residential = 'RES'
    commercial = 'COM'
    Industrial = 'IND'
    transportation = 'TRA'
    other = 'OTH'   
    
    sector = residential
    
    #dataset
    avg_price = 'ELEC.PRICE'
    avg_rev = 'ELEC.REV'
    
    dataset = avg_price

    #generate series ID
    series_id = '{dataset}.{state}-{sector}.{timeline}'.format(dataset=dataset, state=state, sector=sector, timeline=timeline)
    
    eia = 'http://api.eia.gov/series/?api_key={eia_key}&series_id={series_id}'.format(eia_key=eia_key, series_id=series_id)
    
    #request
    e = requests.get(eia)
    settings.economics = e.json
    
     # --------------------------------------------------------------------------------------------------------------------------------
    # DEMOGRAPHIC DATA - CENSUS - https://api.census.gov/data/2015/acs5/variables.html
    # --------------------------------------------------------------------------------------------------------------------------------   
    
    #Census geocoder to get regional codes for the location
    cg = CensusGeocode() 
    
    cg_results = cg.coordinates(x= lon, y= lat)
    
    #Census regional codes
    c_state = cg_results[0]['Census Tracts'][0]['STATE']
    c_county = cg_results[0]['Census Tracts'][0]['COUNTY']
    c_tract = cg_results[0]['Census Tracts'][0]['TRACT']
    
    #Census instantiate with API Key
    c = Census("fb10dd39ec721dda4caf2baf5eed40a57f724084")
    
    #Census variables
    #Median Household Income by Household Size
    size = 'B19019_001E'
    
    #Aggregate household income in the past 12 months 
    agg = 'B19025_001E'
    
    #Age of Householder by Household Income
    age = 'B19037_001E'
    
    #INCOME IN THE PAST 12 MONTHS 
    income = 'B06011_001E'
    
    #retrieve the census data
    d = c.acs5.state_county_tract(('NAME', size), c_state, c_county, c_tract)
    
    settings.demographics = d
    
    return
