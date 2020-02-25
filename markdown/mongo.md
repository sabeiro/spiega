# Mongo db

### Library
```python
import os, sys, gzip, random, csv, json, datetime, re
import numpy as np
import pandas as pd
import scipy as sp
import matplotlib.pyplot as plt
import geopandas as gpd
from scipy.spatial import cKDTree
from scipy import inf
import shapely as sh
import pymongo
baseDir = "~/raw/"
```
We initiate the client
```python
with open(baseDir + '/credenza/geomadi.json') as f:
    cred = json.load(f)

with open(baseDir + '/raw/metrics.json') as f:
    metr = json.load(f)['metrics']

client = pymongo.MongoClient(cred['mongo']['address'],cred['mongo']['port'])
coll = client["index_name"]["collection_name"]
```

### Near sphere
Returns all points within a distance
```python
neiDist = 200.
nodeL = []
for i,poii in poi.iterrows():
    poii = poi.loc[i]
    poi_coord = [x for x in poii.ix[['x','y']]]
    neiN = coll.find({'loc':{'$nearSphere':{'$geometry':{'type':"Point",'coordinates':poi_coord},'$minDistance':0,'$maxDistance':neiDist}}}) 
    nodeId = []
    for neii in neiN:
        nodeL.append({'id_poi':poii['id_poi'],'src':neii['src'],'trg':neii['trg'],"maxspeed":neii['maxspeed'],'street':neii['highway']
                ,"x_poi":poii['x'],"y_poi":poii['y']
        })
```
### Intersects
Take all locations inside polygons
```python
motG = gpd.GeoDataFrame.from_file(baseDir + "gis/geo/motorway_area.shp")
cellL = []
for g in np.array(motG['geometry'][0]):
	c = g.exterior.coords.xy
	c1 = [[x,y] for x,y in zip(c[0],c[1])]
	neiN = coll.find({'geom':{'$geoIntersects':{'$geometry':{'type':"Polygon",'coordinates':[c1]}}}})
	neii = neiN[0]
	for neii in neiN:
		cellL.append({"cilac":str(neii['cell_ci']) + '-' + str(neii['cell_lac'])})
cellL = pd.DataFrame(cellL)
```
### Filtering
Filtering by list
```
coll = client["tdg_infra"]["infrastructure"]
poi = pd.read_csv(baseDir + "raw/tr_cilac_sel1.csv")
colL = list(poi.columns)
colL[0] = 'domcell'
poi.columns = colL
poi.loc[:,'ci'] = [re.sub("-.*","",x) for x in poi['domcell']]
poi.loc[:,'lac'] = [re.sub(".*-","",x) for x in poi['domcell']]
queryL = []
for i,p in poi.iterrows():
    queryL.append({"cell_ci":p['ci']})
    queryL.append({"cell_lac":p['lac']})
```

### Boundary Box
```python
neiN = coll.find({'loc':{'$geoWithin':{'$box':[ [BBox[0],BBox[2]],[BBox[1],BBox[3]] ]}}})
```
