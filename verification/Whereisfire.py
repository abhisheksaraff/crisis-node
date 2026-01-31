
from dotenv import load_dotenv
from pathlib import Path
import os

import pandas as pd
import requests

import pyproj  
from pyproj import Transformer 
import shapely
import shapely.ops as ops
from shapely.geometry.polygon import Polygon
from functools import partial
import math
import openmeteo_requests
import requests_cache
from retry_requests import retry
import pygrib
# Load .env from the same directory as this script (works regardless of cwd)
load_dotenv(Path(__file__).resolve().parent / ".env")
MAP_KEY= os.getenv('NASAFIREPRIVATEKEY')
FLOOD_KEY= os.getenv('FLOOD_KEY')

def firerange(latitude, longitude,uncertainty ):#note: all values in degrees.
    return firesin(longitude-uncertainty, latitude-uncertainty, longitude+uncertainty, latitude+uncertainty, )
def firesin(cb:tuple): #cb being coordinate bounds box. 
    coords=str(cb[0])+','+str(cb[1])+','+str(cb[2])+','+str(cb[3])
    area_url_1 = 'https://firms.modaps.eosdis.nasa.gov/api/area/csv/' + MAP_KEY + '/VIIRS_NOAA20_NRT/'+coords+'/5'
    df_area_1 = pd.read_csv(area_url_1)
    area_url_2 = 'https://firms.modaps.eosdis.nasa.gov/api/area/csv/' + MAP_KEY + '/VIIRS_NOAA21_NRT/'+coords+'/5'
    df_area_2 = pd.read_csv(area_url_2)
    number=len(df_area_1)+len(df_area_2)
    
    geom = Polygon([(cb[0], cb[1]), (cb[0], cb[3]), (cb[2], cb[3]), (cb[2], cb[1])])


    geod=pyproj.Geod(ellps="WGS84")
    lons=[cb[0], cb[0], cb[2], cb[2]]
    lats=[cb[3], cb[1], cb[1], cb[3]]
    poly_area, poly_perimeter = geod.polygon_area_perimeter(lons, lats)
    #print(geom_area)
    likelihood=(number/poly_area**1.75)**0.1*25 #This looks for whether we have a wildfire in enough of the relevant region that we can meaningfully localize it as a 'disaster'.  
    return likelihood

print(firesin((-84.73,  29.965, -84.07, 30.3)))
print(firesin((-83,42,-74,46)))
print(firesin((23.8869795809, 3.50917, 35.2980071182, 12.2480077571)))


def floodsin():


    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://flood-api.open-meteo.com/v1/flood"
    params = {
        "latitude": -24,
        "longitude": 33,
	    "daily": ["river_discharge", "river_discharge_mean"],
        "past_days": 14,
        
	    "forecast_days": 30,
        #"bounding_box": "-25.5,33,-24.1,34",
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process bounding box locations
    for response in responses:
        print(f"\nCoordinates: {response.Latitude()}°N {response.Longitude()}°E")
        print(f"Elevation: {response.Elevation()} m asl")
        print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")
        
        # Process daily data. The order of variables needs to be the same as requested.
        daily = response.Daily()
        daily_river_discharge = daily.Variables(0).ValuesAsNumpy()
        mean_river_discharge=daily.Variables(1).ValuesAsNumpy()
        daily_data = {"date": pd.date_range(
            start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
            end =  pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
            freq = pd.Timedelta(seconds = daily.Interval()),
            inclusive = "left"
        )}
        
        daily_data["river_discharge"] = daily_river_discharge
        daily_data["mean_discharge"] = mean_river_discharge
        daily_dataframe = pd.DataFrame(data = daily_data)
        print("\nDaily data\n", daily_dataframe)
	
floodsin()

import cdsapi
URL = 'https://ewds.climate.copernicus.eu/api'
#key = 
FLOOD_KEY = '766af2ab-a8ab-416a-a332-6b9f98af57e0'
dataset = "cems-glofas-historical"
request = {
    "system_version": ["version_4_0"],
    "hydrological_model": ["lisflood"],
    "product_type": ["consolidated"],
    "variable": ["river_discharge_in_the_last_24_hours"],
    "hyear": [
        "2021",
        "2022",
        "2023",
        "2024",
        "2025"
    ],
    "hmonth": ["01"],
    "hday": ["01"],
     "area": [-24.5, 42.5, -23.5, 43.5],
    "download_format": "unarchived"
}

client = cdsapi.Client(url=URL,  key=FLOOD_KEY)
#client.retrieve(dataset, request).download()
#import xarray as xr
#import cfgrib
#ds = xr.open_dataset("file.grib", engine="cfgrib")

# Print Dataset object

#print(ds)

grbs = pygrib.open("file.grib")
