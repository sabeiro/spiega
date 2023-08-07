# Activities and ODM

Per user we collect a series of events that contain the information about the cell where the user was seen:

* *IMSI* - hashed sim card of a user (one day life time)
* *event* - time and cell information about a user
* *chain* - series of events connected to an imsi

![event collection](../f/f_comm/event_collection.svg "event collection")
_We collect an handover between cells per device (D1-Netz)_

We interpret this information defining:

* *activity* - cluster of events limited in space, continous in time
* *trip* - series of events connecting two activities

![event activity](../f/f_comm/event_activity.png "event and activity")
_a chain is divided into activities and trips_

We can aggregate the event information with cell specifications which consist in:

* *ci-lac*: id composed by the mast id and the specific antenna id
* *BSE*: best server estimate, simulation about the best coverage for the specific antenna
* *centroid*: centroid of the polygon describing the BSE
* *tech*: particular cell's technology (gsm, umts, lte) and frequency

Currently an activity is defined flat over the BSE polygon for the most frequent cell inside the events set.

Depending on the particular situation (cell's position, time of the day, geographical information) we can interpret user's behaviour.

![daily_mappings](../f/f_comm/daily_movements.svg "daily mappings")
_interpreting users behaviour_

## zone mappings

We define where an activity took place by calculating the intersection of a zone polygon with the cell's BSE. We overimpose a geometry on the BSE and we assign the intersection between the two geometries as fraction of activity.

![geometries](../f/f_comm/zone_mapping.png "zone mappings")
_geometries used to calculated activities_

All the mentioned geometries are available to [download](sftp://172.25.100.50/home/gmarelli/lav/motion/gis/geo)

* [ags5](sftp://172.25.100.50/home/gmarelli/lav/motion/gis/geo/ags5.shp)
* [ags8](sftp://172.25.100.50/home/gmarelli/lav/motion/gis/geo/ags8.shp)
* [mtc](sftp://172.25.100.50/home/gmarelli/lav/motion/gis/geo/mtc.shp)
* [zip](sftp://172.25.100.50/home/gmarelli/lav/motion/gis/geo/zip5.shp)


## time mappings

We write hour 14 meaning all the activities between 13 and 14.

![time_mapping](../f/f_comm/time_mapping.svg "time mappings")
_example of time mappings_

We have to convert the time zone depending on the legal time [time zone converter](https://www.worldtimebuddy.com/utc-to-est-converter).

![zone_converter](../f/f_comm/zone_converter.png "zone converter")
_different conversions between summer and winter time_

# Statistical week

The statistical week is a collection of statistical days which consists in a series holiday free days grouped by weekday type.



The first consistency check is done visualizing the data
![statWeek duesseldorf](../f/f_comm/statWeek_duesseldorf.png "statWeek duesseldorf")
_statWeek duesseldor../f/f_

## ODM
An ODM is an origin-destination matrix where we consider every single trip to create an origin-destination relationship. 

We compare people behavior with different statistics.

München suburbs many people travel to München to work.

![statWeek oberhaching](../f/f_comm/statWeek_oberhaching.png "statWeek oberhaching")
_statWeek odm for oberhaching_

In Stuttgart there is a clear pattern of commuters during the day.

![statWeek stuttgart](../f/f_comm/statWeek_stuttgart.png "statWeek stuttgart")
_statWeek odm for  stuttgart_

Hannover has a lower dense neighborhood, people travel less.

![statWeek hannover](../f/f_comm/statWeek_hannover.png "statWeek hannover")
_statWeek odm for  hannover_

Berlin is harder to interpret.

![statWeek berlin](../f/f_comm/statWeek_berlin.png "statWeek berlin")
_statWeek odm for  berlin_

# footfall

The most important quantities to consider are:

* *nodes* are the openstreetmap nodes describing a street
* *tile* is a 250x250m grid containing nodes
* *Footfalls* is the number of _non unique_ trajectories crossing a tile

*Nodes* can be verified on [openstreetmap](https://www.openstreetmap.org/node/3739354140) 

Building an [overpass query](http://overpass-turbo.eu/) returns all the nodes and ways returning the same label

![overpass query](../f/f_prod/overpass_query.png "overpass query")
_overpass query_

We build a network for routing all trips into trajectories.

![routing highweight](../f/f_route/routing_highweight.png "routing highweight")
_routing, improve in weighting_

and we take into account all the events to calculate the best trip.

![detour_avoided](../f/f_route/detour_avoided.png "detour avoided")
_detour avoided discarding neighboring events_

We count than the number of trajectories for the nodes contained in the tile and obtain the footfalls.

From each tile we collect the information and we apply it to the geometry under study
![edge count](../f/f_route/edge_count.png "edge count")
_edge count_

## API

Data can be collected via API

Usual header and credential:

```python
headers = {"Content-type":"application/x-www-form-urlencoded; charset=UTF-8","Authorization":"OAuth2"}
baseUrl = cred['api-url']+":"+str(cred['api-port'])
```

List of features
```python
optL = {"debug":"debug=true","mtc":"geoType=mtc","days":"aggregation=days"}
repL = {"hello":"/tools/hello","dates":"/tools/availableDates"
        ,"login":"/v1/auth/login"
        ,"location":"/v1/locations/"
        ,"tiles":"/v1/tiles/location/"
        ,"counts":"/v1/reports/counts/overall/location/"
        ,"direction":"/v1/reports/directions/overall/location/"
        ,"odm":"/v1/reports/odm/counts/location/"
        ,"geometry":"/v1/tools/geometries/geoType/mtc?shapeIds=777,789"
        ,"overnight":"/v1/reports/overnight/overall/location/"
        ,"tourist":"/v1/reports/tourists/overall/location/"
}
```

Collecting available dates:
```python
resq = requests.get(baseUrl+repL['dates']+authP,headers=headers,verify=False)
```

We loop over all locations to obtain the specific location information:
```python
for i in range(locL.shape[0]):
    print('processing: ' + str(i))#,end="\r")
    getU = baseUrl + repL['direction'] + str(locL['locationId'].iloc[i]) + "/from/" + str(datem) + "/to/" + str(dateM) + authP
    resq = requests.get(getU,headers=headers,verify=False)
```

 
