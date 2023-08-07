---
title: "Motorway drivers"
author: Giovanni Marelli
date: 2018-03-20
rights:  Creative Commons Non-Commercial Share Alike 3.0
language: en-US
output: 
	md_document:
		variant: markdown_strict+backtick_code_blocks+autolink_bare_uris+markdown_github
---

# Motorway drivers
In this [project](smb://10.210.29.30/motionlogic/Data_Science/Customer_Projects_DE/Nissan) the attention is to know the distribution of cars entering and exiting the motorway.

We have tried [different approaches](http://172.25.100.21:31027/geomadi/timeline_nissan.html) to solve the problem and we have defined some KPIs to have a quantitative evaluation of the perfomances of each model.

1. [*tile counts*](#tile-counts)
2. [*routing and via points*](#routing-and-via-points)
3. [*analyzer*](#analyzer)
4. [*postprocessing*](#postprocessing)
5. [*matrix KPIs*](#matrix-kpi)
6. [*fixing-asymmetry*](#fixing-asymmetry)
7. [*topics on router*](#topics-on-router)
8. [*postprocessing routing*](#postprocessing-routing)

The focus of this project is to understand where motorway drivers enter and exit a particular junction of a motorway as described in this [ticket](https://jira.motionlogic.de/browse/DEL-784?filter=-1).

The overview of the [parquet files ](https://wiki.motionlogic.de/display/PROJ/Nissan) is used to compare the different analyzer runs.

## Filtering
We have selected 12 junctions on a isolated motorway (A4) crossing Germany on the east-west axis. 

![isolated_motorway](../f/f_route/krauthausen_area.png "isolated motorway")
_selected motorway stretch_

Chains from the tripEx are filtered via a [pre validation](http://172.25.100.40:8888/notebooks/abhi/pre_validation_odm.ipynb) script.

## Tile counts
We try to obtain the same information on tile counts.
For each junction we have to correctly report the incoming and outcoming flux.

![junction tile](../f/f_route/junction_tile.png "junction tile")
_counts across tiles_

# Postprocessing routing


## Building the network
We keep junctions in the network which are labelled differently from the other street classes.

![network lines](../f/f_route/network_lines.png "network lines")
_junctions into network_

local motorway structure

![route selection](../f/f_route/route_selection.png "route selection")
_local motorway structure_

routing, wrong weighting

## Weighting the graph

We worked at the correct weighting between highway classes:
![routing highweight](../f/f_route/routing_highweight.png "routing highweight")
_routing, improve in weighting_

empirical definition of weights that led to qualitative good routing solutions.

```python
if edge[2]['highway']=='motorway':
	attrs['weight'] = edge[2]['length']*1
elif edge[2]['highway']=='primary':
	attrs['weight'] = edge[2]['length']*1.5
elif edge[2]['highway']=='secondary':
	attrs['weight'] = edge[2]['length']*1.8
else:
	attrs['weight'] = edge[2]['length']*3
```

## precomputing distances
We took a random node for each zip code and we calculate the shortest route between each other zip code [zip2zip](http://172.25.186.11:8000/gmarelli/geomadi/blob/master/py/route_zip2zip.json).

![distances](../f/f_route/distances.png "distances")
_zip 2 zip distances_

For each zip2zip relation we identified the first and last junction crossed by the route.

## ODM
we than processed an ODM between all zips in Germany for 9 days and we joined it with the precomputed zip2zip junction relation to count how many trips are probably routed via motorway junctions.

![odm](../f/f_route/odm_9days.png "odm 9 days")
_odm on 9 days_

We run an ODM with a short and a long break parameter to see the difference in counts and understand where people could have a break on the way.

## enter2exit table

After iterating on all steps of the process,
![zip2zip explanation](../f/f_route/zip2zip_exp.png "zip2zip explanation")

we have created the enter to exit relationship matrix.

![enter to exit](../f/f_route/enter2exit.png "enter to exit")
_enter2exit via postprocessing_

# routing and via points

We realized with an ODM via that the counts of people leaving the motorway wasn't consistent and we couldn't fix the unbalance between junctions in post processing.
![postprocessing fix](../f/f_route/postprocessing_fix.png "postprocessing fix")
_In post processing we filtered out fuzzy relations caused by detours_

## Via points on junctions
We have manually added unique via nodes on the motorway links into our infrastructure

![via points](../f/f_route/via_junction.png "via point on junction")
_via point on junction_

We associate this points to a location and we group entrances and exits together:
```json
 "input_locations":[
      {"location_id":"exit_32",
        "node_list":[263030540, 2675499063]},
      {"location_id":"entry_32",
        "node_list":[227910516, 25418734]},
```
and created the appropriate [qsm job](http://172.25.186.11:8000/gmarelli/geomadi/blob/master/job/odm_via/qsm.odm_extraction.odm_via_via.json) where all nodes are grouped into via locations.

## Analyzer 
These chains are passed thought the analyzer and we analyze [a few trajectories](http://172.25.100.40:8888/notebooks/Maurice/TestData_Nissan.ipynb#).

At first we spot some strange behaviour:

![first_routing](../f/f_route/strange_routing.png "first routing")
_inspection on routing_

After the second analyzer run:

![second_routing](../f/f_route/improved_routing.png "second routing")
_inspection on routing, second run, improved results_

## Traffic on via nodes
We analyze the number of users passing by entrances and exits and find the relationships between ramps:
[via counts](http://172.25.100.40:8888/notebooks/Maurice/Via_Via_Counts.ipynb), [traffic on some via nodes](http://172.25.219.77:8888/notebooks/gio/Krauthausen_evaluation.ipynb#)

We look at the size of entrances and exits to spot possible asymmetries:
![size_enter_exit](../f/f_route/size_enter_exit.png "volume of entrances and exits")
_The radius show the size of entrances (blue) and exits (red), circles are pretty symmetric_

## Pair relationships
We investigated the relationship between [via nodes on the junctions](http://172.25.219.77:8888/notebooks/gio/Nissan_Evaluation.ipynb#)
and we spot some detours that falsify the counts that we are going to correct in postprocessing.

We [visualize some relationships](http://172.25.100.40:8888/notebooks/Maurice/Nissan_Via_Via_Results.ipynb) using [kepler](http://kepler.gl/)

![pair_relations](../f/f_route/pair_relations.png "pair relationships")
_visulization of pair relationships_

## Postprocessing
We consider the first entrance and the last exit removing all internal loops [etl_nissanVia](http://172.25.186.11:8000/gmarelli/geomadi/blob/master/etl/etl_nissanVia.py)

```
exit_36;entry_36;exit_41b;entry_42 -> entry_36;exit_41b
exit_34;entry_34;exit_36;entry_40b;exit_41a -> entry_34;exit_41a
```
This filters out 26% of all trajectories which have no 1st entry and lst exit.

We remove unrealistic routes:
```
entry_56a;entry_41b
exit_32;exit_42;entry_42
```

We keep strange routes:
```
entry_59, exit_61, entry_60, exit_57
```

In this way we can build a matrix of all the connections between junctions.
![junction connection](../f/f_route/junction_connection.png "junction connection")
_We count all the pair connection between junctions, we see how connections get thinner on larger distances_

We pivot the table and obtain a square matrix showing all the enter and exit relations:

![correlation junction](../f/f_route/correlation_junction.png "correlation between junctions")
_correlation between junctions, neighboring junctions show good correlation, we must investigate the boundaries of the correlation blocks_

## Junctions distance
To obtain the routed distance between junctions we request an [openstreetmap api](http://172.25.186.11:8000/gmarelli/geomadi/blob/master/py/api_route.py).
```python 
    baseUrl = "https://api.openrouteservice.org/directions?"
    nodeD = []
    for i in range(nodeEn.shape[0]):
        for j in range(i+1,nodeEx.shape[0]):
            g1 = nodeEn.iloc[i]
            g2 = nodeEx.iloc[j]
            print("%s - %s : %.2f%%" % (g1['loc'],g2['loc'],(i*j)/(nodeEn.shape[0]*nodeEx.shape[0])))
            queryS = "api_key=" + cred['openroute']['token']
            queryS += "&coordinates="+str(g1['x'])+"%2C"+str(g1['y'])+"%7C"+str(g2['x'])+"%2C"+str(g2['y'])
```
All junctions over 150km from a reference junction are labelled as 996 because the current autonomy of the electric car under study is around 160km. 

![api routing](../f/f_route/api_routing.png "openrouteservice")
_we use openrouteservice to calculate distances between junctions _

## Matrix KPIs
The expected output of the enter2exit matrix should have the expected properties:

* symmetric
* null diagonal
* counts decaying with distance

![size_enter_exit](../f/f_route/en2ex_image.png "removing discrepancies in enter2exit matrix")
_the enter2exit matrix has diagonal counts: 13% and outliers: 5%._

|KPI|single|clamp|
|----|-----|------|
|diagonal|15%|26%|
|asymmetry|26%|21%|
|decay - correlation| -0.3|-0.4|

We display the asymmetry matrix coloring all cells under 10% relative difference with green, all cells between 10% and 20% with yellow and over 20% with red.

We have clamped the odd numbered juntions into the even ones. 

![asym matrix](../f/f_route/asym_mat.png "asymmetry matrix")
_asymmetry matrix with traffic light color code, we compare postprocessing approach (left) with single trajectory sum (right)_

$$ \delta = 2\frac{|c_{AB} - c_{BA}|}{c_{AB}+c_{BA}}\cdot w(m_{AB}) $$

where $c_{AB}$ is the number of cars going from A to B

$$ w(m_{AB}) = b + m_{AB}\frac{1 - b}{max(m_{AB})} $$

and $m_{AB}$ is the maximum between $c_{AB}$ and $c_{BA}$ and $w$ is the weighting function and $b$ the intercept.

![weighting function](../f/f_route/weighting_function_definition.png "weighting function definition")
_definition of the weighting function_

|range|trajectories|zip2zip| 
|-------|-------|------|
|within 10%|39%|  24%|
|within 20%|26%|  12%|
|over   20%|35%|  64%|

We see a small dependency between junction length and number of cars.

![length_decay](../f/f_route/length_decay.png "length decay")
_the number of cars decay with junction distance_

## fixing asymmetry
We have realized that some junctions were particularly asymmetric and we started [investigating few trajectories](http://172.25.100.40:8888/notebooks/gio/Analyze_Junction44.ipynb)

We saw some trajectories be forced to take the junctions

![forced junctions](../f/f_route/forced_junction.png "forced on the junction")
_some routes are forced to proceed on the junction_

We sorted the timestamps and saw a strange arrangements of nodes.

![start end](../f/f_route/start_end.png "start end")
_start (green) end (red) and junction (blue) are not conseguent_

We saw that an unprecise definition of the starting point led to detours.

![unprecise start](../f/f_route/unprecise_start.png "unprecise start")
_the start node competes with other events that might help to distinguish the real start_

B-spline are important to neutralize the swing between cities that are denser in cells which force the trajectory to leave the motorway to approach to a city and go back to continue the trip.

![routing centroid](../f/f_route/routing_centroid.png "routing centroid")
_black: routed trajectory, red: events line, stars: hypothetical cell's centroids, ellipses: hypothetical BSEs, crossing the motorway_

## Topics on router

There are different issues (routing, starting-ending point, graph) from my opinion:

* a trip should not start on a motorway
* direction changes on the motorway shouldn't be allowed
* still many detours
* segments are missing (junctions complete the gaps on motorway stretches)

![motor asymmetry](../f/f_route/motor_asymmetry.png "motor asymmetry")
_starts and ends on the motorway lead to asymmetry_

My suggestion is to update our graph to have a series of parameter which can help the routing:

#### GRAPH

When we transform the complete OSM node collection into our production graph I would add the following attribute to each segments of graph:

* routed distance: helps the routing weights, more realistic distances
* chirality: chirality change is irrealistic
* gyration radius: helps the routing weights, streight segments should be preferred

#### START-END

* start-end points should not be on the motorway
* paths should be included between start and end. the events too far away from start-end bounding box should be filtered out

![start-end](../f/f_route/en2ex_bounding.png "enter and exit bounding box")
_enter and exit bounding box_

#### DETOURS

* do we smooth the events position before routing (B-splines?)
![detour asymmetry](../f/f_route/deroute_asymmetry.png "detours asymmetry")
_detours bring to asymmetry_

## AB routing
To avoid detours we have started using AB routing which drammatically improves the number of loops.

![ab routing](../f/f_route/ab_routing0.png "AB routing")
_AB routing avoid detours_


![detour_avoided](../f/f_route/detour_avoided.png "detour avoided")
_detour avoided discarding neighboring events_

## Improvements
The series of iterations we did helped improving the precision of the enter2exit relations. The last run consists on a more days sum.
![asym history](../f/f_route/asymmetry_history.png "asymmetry history")

The asymmetry matrix view show how the precision of the asymmetry improved from the first to the last analysis. 
![asym_improvement_sign](../f/f_route/asym_improvement_sign.png "asymmetry improvement")

We still can see few problems to solve: 

* junction 32 is not correctly mapped in the infrastructure
* junctions 47, 58 show high asymmetry but no particular reason was found

## Junction labelling automation
To automize the labelling of the nodes of the junctions we write two functions.

* [enrichNissan](http://172.25.186.11:8000/gmarelli/geomadi/blob/master/custom/geo_enrichNissan.py) where we project all nodes on the motorway, calculate the perpendicular distance from the motorway and side of the motorway (via chirality)
* [junctionNodes](http://172.25.186.11:8000/gmarelli/geomadi/blob/master/py/geo_junctionNodes.py) we iterate over `id_jun`, `chi`, `id_zone`, and `dir` to calculate the local center of mass and the orientation depending on the cross product

![junction_labeller](../f/f_route/junction_labeller.png "junction labeller")
_graphical explanation on the selection and identification of nodes works_

The algorithm supposes there are two branches per motorway and one entry and one exit per branch. Everything is splitted in 700m cluster to improve the accuracy if the crossing is large enough.

![complex_junctions](../f/f_route/complex_junctions.png "complex junctions")
_not all topologies can be covered by the algorithm_

## any via after junction labelling

After have labelled all junction nodes to be included in the [infrastructure](celery_t_tdg_infra_18b09@172.25.219.207:31024) we run an [odm any via](http://172.25.186.11:8000/gmarelli/geomadi/raw/master/job/odm_via/qsm.odm_extraction.odm_via_via_thuering.json) for [1M3 chains dataset](http://172.25.100.33:50070/explorer.html#/tdg/2017/09/12/trips/odm) to obtain the number of trajectory crossing the [via points in Thüringen](http://172.25.100.33:50070/explorer.html#/tdg/qsm/20181119_1436_odm_via_via_thuering/2018/custom_aggregations/odm_result/custom_odm_result_application_1538385106982_0705).

We run the kpi calculation based on the results of the data

![thuerin matrix](../f/f_route/thuerin_matrix.png "thuerin matrix")
_count matrices between entry and exits_

![thuerin correlation](../f/f_route/thuerin_correlation.png "thuerin correlation")
_correlation between pair relation counts, on the rhs we magnified the zone with lower correlation_

![thuerin asym](../f/f_route/thuerin_asym.png "thuerin asym")
_most of the relations show asymmetry but it's due to low counts_

![thuerin junSum](../f/f_route/thuerin_junSum.png "thuerin junSum")
_even on junction sum symmetry is not conserved_

No clear picture about result performances can be given with this few trajectories.

## from trajectories to junction pairs
We perform a further correction of the job file and change the definition of the delooper. We break all the trajectories into single pairs. For every uncomplete entry or exit we associate the junction 998.

![enEx_sym](../f/f_route/enEx_sym.png "entrance and exit symmetry")
_if we count the total number of entrances and exits symmetry is conserved, both for all the any via combinations (lhs) and for the 2 via nodes trajectories (rhs)_

We have a fair number of motorway junction crossed during a trajectory in Thüringen. 3 and 4 via node trajectories correspond to shortcuts, U turns and breaks.

![viaProJunction](../f/f_route/viaProJunction.png "via points pro trajectory")
_via points pro trajectory_

We than see that we still have asymmetries on the single junction level but the total asymmetry is conserved
![entryExit_count](../f/f_route/entryExit_count.png "counts of entries and exit")
_counts of entries (blue) and exits (red) pro junction_


