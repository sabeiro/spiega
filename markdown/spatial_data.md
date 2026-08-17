---
title: spatial data
author: Giovanni Marelli
date: 2019-09-12
rights:  Creative Commons Non-Commercial Share Alike 3.0
language: en-US
id: spatial_data
category: #tech
roam_refs: spatial data
roam_aliases: ["spatial data"]
output: 
	md_document:
		variant: markdown_strict+backtick_code_blocks+autolink_bare_uris+markdown_github
---


# spatial

spatial analysis and backup material

## spatial latency

Query: [resample_1sec](queries/spatial_latency.sql).
Code: [etl_spikes](src/geo_latency.py)

We analize the latency data depending on the position of the vehicle. We create a geohash per coordinate pair and calculate the average latency

![latency_geo](../../f/f_tele/latency_geo.png)
_latency per geohash_

We see a similar pattern per modem upload

![latency_geo](../../f/f_tele/modemTx_geo.png)
_upload per geohash_

The most interesting correlations with camera latency are on the spatial level

![geo_correlation](../../f/f_tele/geo_correlation.png)
_spatial correlation_

We clearly see that incidents (`camera_latency` > 400ms) are clustered in space

![geo_incident](../../f/f_tele/geo_incident.png)
_spatial distribution of incidents_

We check the cell handover

![geo_handover](../../f/f_tele/geo_handover.png)
_handover cases spatially distributed_

Handover is strangely highly correlated but not with camera latency

![geo_corr](../../f/f_tele/handover_corr.png)
_correlation between handover_

# backup material

Ongoing analysis

## long short term memory

Code: [stat_reample](src/stat_resample.py)

We want to asset the performances using a LSTM starting with a baseline of a single layer

We first train a model with 16 fold cross validation and we than substitute each time some random value per feature. The performance of the model with a synthetic random feature should significantly drop for the most important predictors.

![lstm_importance](../../f/f_tele/lstm_importance.png)
_performance drop depending on the feature_

## dictionary learning

We create rolling windows of the time series to see how we can cluster these windows into an essential dictionary of elements.

We start first with 18 clusters composed by series of 16 data points and we create some fundamental clusters

![series_dictionay](../../f/f_tele/series_dictionary.png)
_dictionary of time series windows_

We make sure that the dimension of the cluster is pretty much orthogonal

![dictionary_ortho](../../f/f_tele/dictionary_ortho.png)
_orthogonality of dictionary_




# spatial data

Managing spatial data means working with many attributes and efficient indexing to retrieve the information.
Spatial data are defined by a geometry which is usually:

* a point
* a line
* a polygon

Geospatial libraries uses algebraic operations to compute areas, distances and bounding boxes.

Essential for every geospatial project is assigning the right projection for the coordinates to use. At small scales the differences in computation are small (cities) but become pretty relevant at higher scales (countries). The mostly commonly used is the [ESG:4236](https://spatialreference.org/ref/epsg/4236/wkt.html). The idea is mainly to pick one projections which would conserve: distances, areas (administrative) or angles (navigation). 

## attributes


Spatial data have many attributes on top of a location expressed in coordinates or areas

* labelling
* routes
* terrain
* supply lines

