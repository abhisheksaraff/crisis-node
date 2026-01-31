
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from verification.utils.Whereisfire import firesin
from verification.utils.whereisflood import floodsin
#Obviously every test will expire, because these tests depend on what is actually happening. 
print(firesin((-84.73,  29.965, -84.07, 30.3))) #Some of Wakulla county florida, which probably doesn't have wildfires anymore TBH
print(firesin((-83,42,-74,46)))#Ontario, vaguely: probably no actual fires here. 
print(firesin((23.8869795809, 3.50917, 35.2980071182, 12.2480077571)))#'south sudan', vaguely. Many fires here. 
print(firesin((152, -32.8, 152.6, -31.4)))#A specific part of australia where a specific fire happened. 
print(floodsin(-25.075,33.575)) #an area of the limpopo which recently flooded
print(floodsin(-24.93,33.62)) #an area of the limpopo which recently flooded

print(floodsin(46.33,-72.52))#the St Lawrence: no flooding

#print(floodsin(-33.91,-58.42))#The Uruguay river

print(floodsin(31.78,120.985))#The Yangtze

print(floodsin(49.7, -125))#The Yangtze#Comox Valley Floods