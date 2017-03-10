#data.py
#connect to datasources

#load dependencies
import pandas as pd
import numpy as np
import requests
import json
import sys, os

#load layers
import settings

def init():
    
    #clean globals
    lat = settings.lat
    lon = settings.lon
    state = settings.state
    postal = settings.postal
    #year = settings.year
    
    # --------------------------------------------------------------------------------------------------------------------------------
    # WEATHER DATA - NSRDB  - https://nsrdb.nrel.gov/api-instructions
    # --------------------------------------------------------------------------------------------------------------------------------
    # Declare all variables as strings. Spaces must be replaced with '+', i.e., change 'John Smith' to 'John+Smith'.

    # You must request an NSRDB api key from the link above
    api_key = 'JJQmF8CNU7qDCgGptU1krnjESLAa4RBzH2aOaOrs'
    # Set the attributes to extract (e.g., dhi, ghi, etc.), separated by commas.
    attributes = 'ghi,dhi,dni,wind_speed_10m_nwp,surface_air_temperature_nwp,solar_zenith_angle'
    # Choose year of data
    year = '2010'
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
    
    settings.weather = weather
        
    # --------------------------------------------------------------------------------------------------------------------------------
    # POLITICAL DATA - DSIRE - http://www.dsireusa.org/resources/data-and-tools/
    # --------------------------------------------------------------------------------------------------------------------------------

    dsire = 'http://programs.dsireusa.org/api/v1/getprograms/json?fromSir=0&state={state}'.format(state=state)
    
    print dsire
    
    p = requests.get (dsire)
    
    settings.politics = p.json
    
    
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
    settings.economics = e.text
    
    return
