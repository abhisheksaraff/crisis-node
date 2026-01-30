
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

# Load .env from the same directory as this script (works regardless of cwd)
load_dotenv(Path(__file__).resolve().parent / ".env")
MAP_KEY= os.getenv('NASAFIREPRIVATEKEY')

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
