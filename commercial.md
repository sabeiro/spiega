# Activities and ODM

Per user we collect a series of events that contain the information about the cell where the user was seen:

* *IMSI* - hashed sim card of a user (one day life time)
* *event* - time and cell information about a user
* *chain* - series of events connected to an imsi

![event collection](f_comm/event_collection.svg "event collection")
_We collect an handover between cells per device (D1-Netz)_

We interpret this information defining:

* *activity* - cluster of events limited in space, continous in time
* *trip* - series of events connecting two activities

![event activity](f_comm/event_activity.png "event and activity")
_a chain is divided into activities and trips_

We can aggregate the event information with cell specifications which consist in:

* *ci-lac*: id composed by the mast id and the specific antenna id
* *BSE*: best server estimate, simulation about the best coverage for the specific antenna
* *centroid*: centroid of the polygon describing the BSE
* *tech*: particular cell's technology (gsm, umts, lte) and frequency

Currently an activity is defined flat over the BSE polygon for the most frequent cell inside the events set.

Depending on the particular situation (cell's position, time of the day, geographical information) we can interpret user's behaviour.

![daily_mappings](f_comm/daily_movements.svg "daily mappings")
_interpreting users behaviour_

## zone mappings

We define where an activity took place by calculating the intersection of a zone polygon with the cell's BSE. We overimpose a geometry on the BSE and we assign the intersection between the two geometries as fraction of activity.

![geometries](f_comm/zone_mapping.png "zone mappings")
_geometries used to calculated activities_

All the mentioned geometries are available to [download](sftp://172.25.100.50/home/gmarelli/lav/motion/gis/geo)

* [ags5](sftp://172.25.100.50/home/gmarelli/lav/motion/gis/geo/ags5.shp)
* [ags8](sftp://172.25.100.50/home/gmarelli/lav/motion/gis/geo/ags8.shp)
* [mtc](sftp://172.25.100.50/home/gmarelli/lav/motion/gis/geo/mtc.shp)
* [zip](sftp://172.25.100.50/home/gmarelli/lav/motion/gis/geo/zip5.shp)


## time mappings

We write hour 14 meaning all the activities between 13 and 14.

![time_mapping](f_comm/time_mapping.svg "time mappings")
_example of time mappings_

We have to convert the time zone depending on the legal time [time zone converter](https://www.worldtimebuddy.com/utc-to-est-converter).

![zone_converter](f_comm/zone_converter.png "zone converter")
_different conversions between summer and winter time_

# Statistical week

The statistical week is a collection of statistical days which consists in a series holiday free days grouped by weekday type.

|weekday|date list|
|---------|----------------------------------------------------------------------------------|
|monday   |"2018/04/16", "2018/06/11", "2018/06/18", "2018/09/17", "2018/09/03", "2018/09/10"|
|tuesday  |"2018/06/05", "2018/06/12", "2018/06/19", "2018/09/18", "2018/09/04", "2018/09/11"|
|wednesday|"2018/06/06", "2018/06/13", "2018/06/20", "2018/09/19", "2018/09/05", "2018/09/12"|
|thursday |"2018/04/19", "2018/06/07", "2018/06/21", "2018/09/20", "2018/09/06", "2018/09/13"|
|friday   |"2018/04/20", "2018/06/08", "2018/06/15", "2018/09/21", "2018/09/07", "2018/09/14"|
|saturday |"2018/04/21", "2018/06/09", "2018/06/16", "2018/09/22", "2018/09/08", "2018/09/15"|
|sunday   |"2018/04/22", "2018/06/10", "2018/06/17", "2018/09/23", "2018/09/09", "2018/09/16"|

## activity report
An activity report consists in a `dominant_zone` which is where a user was seen during the day. Usually we filter according to a dwelling time which sets the minimum or maximum duration of a stay.

We can extract other attributes like:

|Feature|ID|content|
| :------------- | --: | :-------------------------------------------------------------------- |
|*Area*|`dominant_zone`| Area in which an activity was measured|
|*Hour*|`time`| Hour in which the activity was started in UTC (Hint: Add one hour to convert to ECT)|
|*weekday type*|`day`| Monday (MON), Tuesday (TUE), Wednesday (WED), Thursday (THU), Friday (FRI), Saturday (SAT), Sunday (SUN)|
|*count*|`count`| sum of subscribers per geometry/time. Extrapolated to the total population|
|*first signal*|`home_zone`|first signal of the day|
|*last signal*|`last_zone`|last signal of the day|
|*Age group*|`label`| Age group in steps of 10|
|*gender*|`label`| M = male, F = female|
|*area of ​​origin*|`overnight_zip`| Zip Code|
|*country of origin*|`country`| Name of the country of origin of the Roamer (outside Germany)|
|*country code*|`country_code`| Country code according to [mobile classification](https://en.wikipedia.org/wiki/Mobile_country_code)|
|*Share*|`share`|Share of age, gender or region of origin in relation to the total number of activities measured in the area|



The first consistency check is done visualizing the data
![statWeek duesseldorf](f_comm/statWeek_duesseldorf.png "statWeek duesseldorf")
_statWeek duesseldorf_

## ODM
An ODM is an origin-destination matrix where we consider every single trip to create an origin-destination relationship. 

Data tables description:

|Feature|ID|content|
| :------------ | --: | :-------------------------------------------------------------------- |
|*Area*|`dominant_zone`| Area in which an activity was measured; Tile identifier in the MTC grid requirement: previous stay of min. 2h|
|*Hour*|`time`| Hour in which the activity was started in UTC (Hint: Add one hour to convert to ECT)|
|*weekday type*|`day`| Monday (MON), Tuesday (TUE), Wednesday (WED), Thursday (THU), Friday (FRI), Saturday (SAT), Sunday (SUN)|
|*Count*|`count`| Average based on mobile radio counts Extrapolated to the total population|
|*Age group*|`label`| Age group in steps of 10|
|*gender*|`label`| M = male, F = female|
|*area of ​​origin*|`overnight_zip`| Zip Code|
|*country of origin*|`country`| Name of the country of origin of the Roamer (outside Germany)|
|*country code*|`country_code`| Country code according to [mobile classification](https://en.wikipedia.org/wiki/Mobile_country_code)|
|*Share*|`share`|Share of age, gender or region of origin in relation to the total number of activities measured in the area|

We compare people behavior with different statistics.

München suburbs many people travel to München to work.

![statWeek oberhaching](f_comm/statWeek_oberhaching.png "statWeek oberhaching")
_statWeek odm for oberhaching_

In Stuttgart there is a clear pattern of commuters during the day.

![statWeek stuttgart](f_comm/statWeek_stuttgart.png "statWeek stuttgart")
_statWeek odm for  stuttgart_

Hannover has a lower dense neighborhood, people travel less.

![statWeek hannover](f_comm/statWeek_hannover.png "statWeek hannover")
_statWeek odm for  hannover_

Berlin is harder to interpret.

![statWeek berlin](f_comm/statWeek_berlin.png "statWeek berlin")
_statWeek odm for  berlin_

# footfall

The most important quantities to consider are:

* *nodes* are the openstreetmap nodes describing a street
* *tile* is a 250x250m grid containing nodes
* *Footfalls* is the number of _non unique_ trajectories crossing a tile

*Nodes* can be verified on [openstreetmap](https://www.openstreetmap.org/node/3739354140) 

Building an [overpass query](http://overpass-turbo.eu/) returns all the nodes and ways returning the same label

![overpass query](f_prod/overpass_query.png "overpass query")
_overpass query_

We build a network for routing all trips into trajectories.

![routing highweight](f_route/routing_highweight.png "routing highweight")
_routing, improve in weighting_

and we take into account all the events to calculate the best trip.

![detour_avoided](f_route/detour_avoided.png "detour avoided")
_detour avoided discarding neighboring events_

We count than the number of trajectories for the nodes contained in the tile and obtain the footfalls.

From each tile we collect the information and we apply it to the geometry under study
![edge count](f_route/edge_count.png "edge count")
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

## POSTGRES

All the information concerning the tile are contained into a postgres database. The data can be extracted serializing SQL queries

```python
tileU = np.unique(tileL['tile_id'])
query = "select * from tdg.tile_direction_daily_hours_sum_20170703 where tile_id in ("
for i in tileU:
    query += "" + str(i) + ","
query = query[:-1] + ");"
```
