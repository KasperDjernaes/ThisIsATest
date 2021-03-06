# -*- coding: utf-8 -*-
"""
Created on Thu Jan  3 18:45:00 2019

@author: gusta
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json
from datetime import datetime


path = r'C:\Users\user\Desktop\IT and Cognition\Visualisation\mapboxProject\Placeringshistorik.json'

# Load the data

with open(path, 'r') as read_file:
    data = json.load(read_file)
    
'''Adding duration to each location point ''' 

# Get all time stamps as a numpy array

TimeStamps = np.asarray([int(point['timestampMs']) for point in data['locations'][1:]]) # Get all timestamps beside the last one
TimeStampsShift = np.asarray([int(point['timestampMs']) for point in data['locations'][:-1]]) # get all timestamps beside the first one

# Difference between timestamps in seconds

diff = (TimeStampsShift - TimeStamps) / 1000

# Remove outliers. Certain durations are too high
# Maybe if the phone was turned off for a few days
# Through visual inspection it is clear the the diffs above 415sec can be considered outliers

outlier = 415 # outlier

outlierBool = diff > outlier

# Estimate mean when outliers are not included
newMean = np.mean(diff[diff < outlier])

mask = np.where(outlierBool) # Turn boolean into index of outliers

diff[mask] = newMean # Replace outliers with the mean estimted without outliers

print(diff.shape)


geojson = {
        "type": "FeatureCollection",
        "features":[
                {
                        "type":"Feature","properties":{"durationSec":d[1]}, 
                                "geometry":{"type":"Point",
                                "coordinates": [round(d[0]["longitudeE7"] / 1e7,5), 
                                                round(d[0]["latitudeE7"] / 1e7,5)],
                                },
                                
                                } for d in zip(data['locations'][0:500],diff[0:500])] 
    }
    
print(geojson['features'][0])

# string = json.dumps(geojson, separators=(',', ':'))
    
#with open (r'C:\Users\gusta\Desktop\mapboxProject\placeringsoversigt.geojson', 'w') as text_file:
    #print(string, file=text_file)



















