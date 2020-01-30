# footfall

Footfall 

## Network

The most important quantities to consider are:

* *nodes* are the openstreetmap nodes describing a street
* *tile* is a 250x250m grid containing nodes
* *Footfalls* is the number of _non unique_ trajectories crossing a tile

*Nodes* can be verified on [openstreetmap](https://www.openstreetmap.org/node/3739354140) 

![example node](f_prod/example_node.png "example node")
_example node_

Building an [overpass query](http://overpass-turbo.eu/) returns all the nodes and ways returning the same label

![overpass query](f_prod/overpass_query.png "overpass query")
_overpass query_

Data can be downloaded in json

![overpass json](f_prod/overpass_json.png "overpass json")
_overpass json to download_

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


## Dashboad

Footfall are diplayed in the [motionlogic dashboard](https://pollux-dev.motionlogic.de/dashboard/).

During login one has to specify the country - customer project: ex se-test
![login dash](f_prod/login_dash.png "login dash")
_login dash_

The first screen shows the counts per tile

![tile location](f_prod/tile_location.png "tile location")
_tile location_
_the dashboard shows the footfalls for the selected tiles_

Data are available in hourly resolution

![hourly values](f_prod/hourly_values.png "hourly values")
_hourly values_

In the front panel one can select the available dates

![date available](f_prod/date_available.png "date available")
_available dates are marked in green_

For each location the tile geometry is plotted plus the reference number, coordinates and number of footfalls.

![footfall locations](f_prod/footfall_locations.png "footfall locations")
_footfall locations_

We have a age and gender split

![age groups](f_prod/age_groups.png "age groups")
_age groups_

On top of footfall we show the incoming and outcoming flow for the 4 edges of the tile:

![direction breakout](f_prod/direction_breakout.png "direction breakout")
_direction breakout, north-east-south-west_

Counts are splitted in mode of transportation

![modal split](f_prod/modal_split.png "modal split")
_modal split_

and we have an overview of the counts per coordinate

![tile movements](f_prod/tile_movements.png "tile movements")
_tile movements_

### locations

We have an overview of all the locations uploaded for the customer project

![location position](f_prod/location_position.png "location position")
_location position_

and the table with the reference numbers for joining tables.

![location table](f_prod/location_table.png "location table")
_location table_

We can extract a report containing all the information we see in the dashboard

![footfall report](f_prod/footfall_report.png "footfall report")
_footfall report_

For each tile we see where the neighboring locate

![tile directions](f_prod/tile_directions.png "tile directions")
_tile directions_

New locations can be uploaded from an external file

![location upload](Pictures//location_upload.png "location upload")
_location upload_


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
