import requests
import requests_cache
import openmeteo_requests
import requests_cache
from retry_requests import retry
from dotenv import load_dotenv
from pathlib import Path
import os
import pygrib

import pandas as pd
def floodsin(lat, long):
    ''''
    Informs about flooding at a given latitude and longitude known via the Global Flood Awareness System.
    '''

    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://flood-api.open-meteo.com/v1/flood"
    params = {
        "latitude": lat,
        "longitude": long,
	    "daily": ["river_discharge", "river_discharge_mean"],
        "past_days": 14,
        
	    "forecast_days": 60,
        #"bounding_box": "-25.5,33,-24.1,34",
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process bounding box locations
    for response in responses:
        #print(f"\nCoordinates: {response.Latitude()}°N {response.Longitude()}°E")
        #print(f"Elevation: {response.Elevation()} m asl")
        #print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")
        
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
        
        daily_data["river_discharge "] = daily_river_discharge
        daily_data["mean_discharge"] = mean_river_discharge
        daily_dataframe = pd.DataFrame(data = daily_data)
        maxfloodyet=daily_river_discharge[0:16].max()
        #print("\nDaily data\n", daily_dataframe)
        meanexp=daily_river_discharge[25:].mean()
        
        #print("maxfloodyet",maxfloodyet )
        #print("meanexpected", meanexp )
        floodfactor=maxfloodyet/meanexp
        
        #print("flood factor", maxfloodyet/meanexp)
        #Minor floodin
        prognosis=""
        if(floodfactor<2 or maxfloodyet<2):
            prognosis=("probably not major flooding")
        elif(maxfloodyet<3):
            prognosis=("minor flooding, results depending on vulnerability")
        elif(floodfactor<10 or maxfloodyet<100):
            prognosis=("This is a flood")
        else:
            prognosis=("This is really quite bad. ")

        return floodfactor,prognosis
	

def gribgribbingly(gribbox):# Not actually being used, because even though it would be better, it does take too long to execute. Grib them like they've never been gribbed before. 
    import cdsapi
    URL = 'https://ewds.climate.copernicus.eu/api'
    #key = 
    #FLOOD_KEY = '766af2ab-a8ab-416a-a332-6b9f98af57e0'
    FLOOD_KEY= os.getenv('FLOOD_KEY')
    dataset = "cems-glofas-historical"
    request = {
        "system_version": ["version_4_0"],
        "hydrological_model": ["lisflood"],
        "product_type": ["consolidated"],
        "variable": ["river_discharge_in_the_last_24_hours"],
        "hyear": [
            "2020",
            "2021",
            "2022",
            "2023",
            "2024",
            "2025",
            "2026"
        ],
        "hmonth": ["01"],
        "hday": ["01"],
        "data_format": "grib2",
        "download_format": "unarchived",
        "area": [-24.9, 33.4, -25.1, 33.6]
    }
    client = cdsapi.Client(url=URL,  key=FLOOD_KEY)
    target=("file.grib")
    client.retrieve(dataset, request, target)
    #import xarray as xr
    #import cfgrib
    #ds = xr.open_dataset("fi   le.grib", engine="cfgrib")

    # Print Dataset object

    #print(ds)

    grbs = pygrib.open("file.grib")
    #for grb in grbs:
    #    print(grb)
    #    lats, lons = grb.latlons()
    #    print(lats)
    #    print(lons)
    #    print(grb.values)