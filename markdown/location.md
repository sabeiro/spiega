---
title: "location"
author: Giovanni Marelli
date: 2019-10-02
rights:  Creative Commons Non-Commercial Share Alike 3.0
language: en-US
output: 
	md_document:
		variant: markdown_strict+backtick_code_blocks+autolink_bare_uris+markdown_github
---

# city features

We run a series of queries on overpass turbo to get the most important features per city

![overpass_query](../f/f_act/overpass_query.png "overpass query")

_running a query on overpass_

We create a buffer around the new points and we dissolve the layer into a single multipolygon

![map_state](../f/f_act/map_state_layer.png "map error")

_we have different layers showing the most important city features_

We calculate the distance from the closest polygon and label them by customer segment

![map_public](../f/f_act/map_public.png "map error")

_we have different layers showing the public spaces_


We calculate correlation between features

![map_public](../f/f_act/feat_correlation.png "map error")

_correlation between features and distances_

![spot_feature](../f/f_act/spot_feature.png "")

_feature and spot overlapping_

### Population density
We enrich poi information with official statistical data like:

* population density 
* men/women asymmetry
* foreigner percentage
* flat density
* land use
* age asymmetry

We don't know a priori which parameter is relevant for learning and we might have surprisingly perfomances from features that do not seem to have connection with the metric.

![blue de](../f/f_food/blue_de.png "blue de")

_distribution of official census data_

To obtain the value of population density we interpolate over the neighboring tiles with official census data using a stiff multiquadratic function.

Distribution of expense power across the city

![kaufkraft_berlin](../f/f_act/kaufkraft_berlin.png "kaufkraft")

_expense power_

![dens interp](../f/f_food/dens_interp.png "dens interp")

_determination of the density value coming from the neighboring tiles of the official statistics_

We than obtain an approximation on smaller geometries

![popDens](../f/f_act/popDens_interp.png "popdens")
_population density interpolation_

And obtain an estimation on percentage of foregners, flat use, land use...

![foreign](../f/f_act/foreign_interp.png "foreign")

_foreign distribution_

### Degeneracy
[Degeneracy](https://en.wikipedia.org/wiki/Degeneracy_(graph_theory)) is a measure of sparsity or replication of states, in this case we use the term to define the recurrency of pois in a spatial region.

The operative definition is to calculate the distribution of other pois at a certain distance. To reduce the complexity of the metric we perform a parabolic interpolation and define the degeneracy as the intercept of the parabola fitting the radial density distribution.

![spatial degeneracy](../f/f_food/spatial_degeneracy.png "spatial degeneracy")

_spatial degeneracy, only the intercept is taken into consideration_

## Isochrone

For each location we download the local network and calculate the isochrones

![isochrone](../f/f_food/isochrone.png "isochrone")

_isochrone, selected nodes and convex hulls_

## prediction

In the literature there are different examples of spatial forecast prediction [property values](https://www.techinasia.com/machine-learning-estimate-singapore-property-value).

![prop_pred](../f/f_act/property_prediction.png "property prediction")

_property prediction_
