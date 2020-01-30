# Geo operations
Materials:
* [Points in polygon](points-in-polygon)

### Library
We need the libraries:
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
baseDir = "~/raw/"
```
### Data
```python
poi = pd.read_csv(baseDir + "poi.csv")
#x,y,name,region,bla bla
```
### Points in polygon
_________________
Coordinates in region:
```python
region = gpd.GeoDataFrame.from_file(baseDir + "gis/geo/bundesland.shp")
region.index = region['GEN']
region = region['geometry']
pL = poi[['x','y']].apply(lambda x: sh.geometry.Point(x[0],x[1]),axis=1)
pnts = gpd.GeoDataFrame(geometry=pL)
pnts = pnts.assign(**{key: pnts.within(geom) for key, geom in region.items()})
for i in pnts.columns[1:]:
    poi.loc[pnts[i],"region"] = i 
```
### Clustering
_______________
Cluster coordinates within a distance
```python
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.cluster.hierarchy import fcluster
Z = linkage(poi[['x','y']], 'ward')
gradMeter = 111122.19769899677
max_d = 1500./gradMeter
poi.loc[:,'id_zone'] = fcluster(Z,max_d,criterion='distance')
```
### Angle
_________________
Calculate orientation of a segment, orthogonal distance from segment to reference point, calculates chirality
```python
dist1 = np.sqrt((nodeL['x1'] - nodeL['x_poi'])**2 + (nodeL['y1'] - nodeL['y_poi'])**2)
dist2 = np.sqrt((nodeL['x2'] - nodeL['x_poi'])**2 + (nodeL['y2'] - nodeL['y_poi'])**2)
nodeL.loc[:,'dist'] = np.min([dist1,dist2],axis=0)
nodeL.loc[:,"orth_dist"] = np.abs((nodeL['x2']-nodeL['x1'])*(nodeL['y1']-nodeL['y_poi'])-(nodeL['y2']-nodeL['y1'])*(nodeL['x1']-nodeL['x_poi']))
nodeL.loc[:,"orth_dist"] = nodeL["orth_dist"]/(np.abs((nodeL['x2']-nodeL['x1'])) + np.abs((nodeL['y2']-nodeL['y1'])))
nodeL.loc[:,"dist"] = nodeL['orth_dist']*nodeL['dist']
v1 = [nodeL['x1'] - metr['deCenter'][0],nodeL['y1'] - metr['deCenter'][1]]
v2 = [nodeL['x2'] - nodeL['x1'],nodeL['y2'] - nodeL['y1']]
crossP = v1[0]*v2[1] - v2[0]*v1[1]
nodeL.loc[:,'chirality_v'] = 1.*(crossP > 0.)
```
### Chirality
Calculates the chirality between two angles
```python
poi.loc[:,'angle'] = np.arctan2((poi['y']-poi['y_mot']),(poi['x']-poi['x_mot']))*180./np.pi
poi.loc[:,'angle'] = - poi.loc[:,'angle']
poi.loc[:,'tang']  = np.arctan2(metr['deCenter'][1]-poi['y'],metr['deCenter'][0]-poi['x'])*180./np.pi
poi.loc[:,'tang']  = 90. - poi.loc[:,'tang']
poi.loc[poi['tang']>180.,'tang'] -= 180.
t = np.abs(poi['tang']-poi['angle'])
t[t>180.] = 360.-t
poi.loc[:,'chirality'] = 1*(t>90)
```
### Tangent point
Calculates the tangent point on a line from a reference point
```python
from shapely.ops import split, snap
from shapely import geometry, ops
motG = gpd.GeoDataFrame.from_file(baseDir + "gis/geo/motorway.shp")
motG = motG[motG['geometry'].apply(lambda x: x.is_valid).values]
line = motG.geometry.unary_union
for i,poii in poi.iterrows():
    p = geometry.Point(poi.loc[i][['x','y']])
    neip = line.interpolate(line.project(p))
    #snap(coords, line, tolerance)
    poi.loc[i,"x_mot"] = neip.x
    poi.loc[i,"y_mot"] = neip.y
```
### Contains
Which polygon contains a point
```python
import shapely.speedups
shapely.speedups.enable()
densG = gpd.GeoDataFrame.from_file(baseDir + "gis/geo/pop_dens_2km.shp")
g = densG['geometry'][0]
p = [sha.geometry.Point(x,y) for x,y in zip(poi['x'],poi['y'])]
poiG = gpd.GeoDataFrame(p,columns=["geometry"])
```
### Polygon to edges
Dissolve a polygon into its edges
```python
tileG = gpd.read_file(baseDir + "gis/tank/tileList.geojson")
tileG.loc[:,'sum'] = tileG.loc[:,'north_in'] + tileG.loc[:,'south_in'] + tileG.loc[:,'east_in'] + tileG.loc[:,'west_in']
dirg = tileG[['tile_id','sum','north_in','south_in','east_in','west_in','north_out','south_out','east_out','west_out']].groupby(['tile_id']).agg(sum)
dirg = dirg.reset_index()
tileL = tileG[['tile_id','col_id','row_id','geometry']].groupby(['tile_id']).head(1)
dirg = pd.merge(dirg,tileL,left_on="tile_id",right_on="tile_id",how="left")
dirg = gpd.GeoDataFrame(dirg)
with open(baseDir + "gis/tank/junction_tile.geojson","w") as fo:
    fo.write(dirg.to_json())
    
dirl = gpd.GeoDataFrame(columns=["in","out","dir","geometry"])
for i,a in dirg.iterrows():
    l = a['geometry'].boundary
    ll = LineString([(l.xy[0][0],l.xy[1][0]),(l.xy[0][1],l.xy[1][1])])
    dirl.loc[str(a['tile_id']) + 'a'] = [a['east_in'],a['east_out'],"e",ll]
    ll = LineString([(l.xy[0][1],l.xy[1][1]),(l.xy[0][2],l.xy[1][2])])
    dirl.loc[str(a['tile_id']) + 'b'] = [a['north_in'],a['north_out'],"n",ll]
    ll = LineString([(l.xy[0][2],l.xy[1][2]),(l.xy[0][3],l.xy[1][3])])
    dirl.loc[str(a['tile_id']) + 'c'] = [a['west_in'],a['west_out'],"w",ll]
    ll = LineString([(l.xy[0][3],l.xy[1][3]),(l.xy[0][4],l.xy[1][4])])
    dirl.loc[str(a['tile_id']) + 'd'] = [a['south_in'],a['south_out'],"s",ll]
                                         
dirl = gpd.GeoDataFrame(dirl)
with open(baseDir + "gis/tank/junction_edge.geojson","w") as fo:
    fo.write(dirl.to_json())
```
### Spectral clustering
```python
from sklearn.cluster import SpectralClustering
from sklearn.cluster import KMeans
mat = np.matrix([[1.,.1,.6,.4],[.1,1.,.1,.2],[.6,.1,1.,.7],[.4,.2,.7,1.]])
print(SpectralClustering(2).fit_predict(mat))
eigen_values, eigen_vectors = np.linalg.eigh(mat)
print(KMeans(n_clusters=2, init='k-means++').fit_predict(eigen_vectors[:, 2:4]))
from sklearn.cluster import DBSCAN
DBSCAN(min_samples=1).fit_predict(mat)
```

### Intersect lines and areas
```python
junct = gpd.read_file(baseDir + "junction_area.geojson")
dirc = gpd.read_file(baseDir + "count_dir.geojson")
dirA = [np.arctan(0.),np.arctan(np.pi/2.),np.arctan(np.pi),np.arctan(3.*np.pi/2.),np.arctan(2.*np.pi)]
def getAng(dx,dy):
    ang = int(np.arctan2(dy,dx)*2./np.pi + 0.5)
    cordD = ["east","north","west","south"]
    return cordD[ang], cordD[abs(2-ang)]

def getDir(dtx,dty):
    cordD = [("east","west"),("north","south"),("west","east"),("south","north")]
    ang = 1
    if(dtx < 0):
        ang = 0
    elif(dtx > 0):
        ang = 2
    elif(dty < 0):
        ang = 3
    return cordD[ang]

cordD = [("east","west"),("north","south"),("west","east"),("south","north")]
exits = gpd.read_file(baseDir + "/motorway_exit_axes.geojson")
fluxC = pd.DataFrame(index=range(0,4*24))
exits.loc[:,'exit'] = 0
exits.loc[:,'enter'] = 0
for i,ex in exits.iterrows():
    l = ex['geometry']
    inTile = [a.contains(Point(l.xy[0][0],l.xy[1][0])) for a in dirc['geometry']]
    outTile = [a.contains(Point(l.xy[0][1],l.xy[1][1])) for a in dirc['geometry']]
    dircI = dirc.loc[inTile]
    dircO = dirc.loc[outTile]
#    ang1, ang2 = getAng(l.xy[1][1] - l.xy[1][0],l.xy[0][1] - l.xy[0][0])
    dtx = dircI.iloc[0]['col_id'] - dircO.iloc[0]['col_id']
    dty = dircI.iloc[0]['row_id'] - dircO.iloc[0]['row_id']
    ang1, ang2 = getDir(dtx,dty)
```
### Resampling
```python
densG = gpd.GeoDataFrame.from_file(baseDir + "gis/geo/pop_density.shp")
centL = densG['geometry'].apply(lambda x: x.centroid)
densG.loc[:,"hash"] = centL.apply(lambda x: geohash.encode(x.xy[0][0],x.xy[1][0],precision=5))
def clampF(x):
    return pd.Series({"pop_dens":x['Einwohner'].sum()
                      ,"flat_dens":x['Wohnfl_Bew'].sum()
                      ,"foreign":x['Auslaender'].sum()
                      ,"women":x['Frauen_A'].sum()
                      ,"young":x['unter18_A'].sum()
                      ,"geometry":cascaded_union(x['geometry'])
                      ,"household":x['HHGroesse_'].sum()
                      ,"n":len(x['Flaeche'])
    })
densG = densG.groupby("hash").apply(clampF).reset_index()
densG.loc[:,'geometry'] = densG['geometry'].apply(lambda f: f.convex_hull)
for i in ['pop_dens','flat_dens','foreign','women','young','household']:
    densG.loc[:,i] = densG[i]/densG['n']
densG = gpd.GeoDataFrame(densG)
densG.to_file(baseDir + "gis/geo/pop_dens_2km.shp")
```
