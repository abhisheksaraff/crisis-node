
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


def genrange(latitude, longitude,uncertainty ):#note: all values in degrees.
    ''''
    generates a bounding box from coordinates and a degree of uncertainty. 
    '''
    return firesin(longitude-uncertainty, latitude-uncertainty, longitude+uncertainty, latitude+uncertainty, )
def firesin(cb:tuple): #cb being coordinate bounds box. 
    ''''
    Informs about fires within a given region known via NASA's  Fire Information for Resource Management System (FIRMS).
    '''
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
    likelihood=(number**1.75/poly_area)**0.2*25 # This looks for whether we have a wildfire in enough of the relevant region that we can meaningfully localize it as a 'disaster'.  
    return likelihood


