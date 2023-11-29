---
title: "Train Mapping"
author: Giovanni Marelli
date: 2019-01-17
rights:  Creative Commons Non-Commercial Share Alike 3.0
language: en-US
output: 
	md_document:
		variant: markdown_strict+backtick_code_blocks+autolink_bare_uris+markdown_github
---

# Trained mapping

We create a mapping based on some reference data referring to a small geographic area we can't resolve with our data. 

![capture_rate](../f/f_mot/capture_rate.svg "capture rate")
_explanation on capture rate_

We don't know a priori how each cell contributes to the measurement of visitors and we create an iterative process to estabilsh the contribution of each cell.

## Consistency in reference data

Reference data have internal consistency that varies from location to location.

We first control how stable is the correlation adding noise.

![noise_stability](../f/f_mot/noise_stability.png "noise stability")
_stability of correlation introducing noise_

We can show as well that noise at the hourly level does not change correlation as fast as for daily values.

![noise_reference](../f/f_mot/noise_stability_hour.png "noise reference")
_noise on reference data_

We see the effect of noise on reference data

![noise_reference](../f/f_mot/noise_reference.png "noise reference")
_noise on reference data_

Already with 15% noise we can't match the reference data with correlation 0.6 at a constant relative error.

If we look at historical data (variance of days with the same isocalendar date) we see that holiday have a big contribution in deviation.

![isocalendar deviation](../f/f_mot/isocalendar_deviation.png "isocalendar deviation")
_deviation on isocalendar_

### forecastability

We quantify the forcastability of a customer time series running a long short term memory on reference data.

We can see that some reference data are easy forcastable by the model

![forecastable_good](../f/f_mot/forecastable_good.png "forecastable good")
_example of good forecastable model_

While some are not understood from the neural network

![forecastable_bad](../f/f_mot/forecastable_bad.png "forecastable bad")
_example of bad forecastable model_

## Data preparation

We use the following [job file](/geomadi/blob/master/job/activity/qsm.activity_report.tank_cilac_t1.json) to produce the activity with the filters:

![act_filter](../f/f_mot/act_filter.svg "filter on activities")
_filter on activities_

* max 2 hours stay
* 20 km previous trip distance
* chirality (previous direction)

Filtering does not change the overall curves but just the niveau

Filtering options:

|name|tripEx|distance|duration|chirality|
|----|------|--------|--------|---------|
| t4        |10.5|20km|30min-2h|True|
| t4_10     |10.5|10km|15min-2h|True|
| t4_p11    |11.6|20km|15min-2h|True|
| t4_p11_d20-notime|11.6|20km|15min-2h|True|
| t4_p11_d10|11.6|10km|15min-2h|True|
| t4_p11_d20|11.6|20km|15min-2h|True|
| t4_p11_d30|11.6|30km|15min-2h|True|
| t4_p11_d40|11.6|40km|15min-2h|True|

![filter_line](../f/f_mot/filter_line.png "effect of filters on curves")
_effect of filters on curves_

![filter_boxplot](../f/f_mot/filter_boxplot.png "effect of filters on curves")
_counts changed by filtering_

We calculate daily values on cilac basis.

The tarball is downloaded and processed with an [etl script](/geomadi/blob/master/etl/proc_tank.py) which uses the a [function](/geomadi/blob/master/geomadi/proc_lib.py) to unpack the tar and process the output with spark.

## Mapping weighting
We filter the cells using only the first 20 ones whose centroid is close to the poi. 

![cilac_correlation](../f/f_mot/cilac_correlation2.png "correlation between cilac")
_some cells are not correlating within each other_

At first sight the sum of activities doesn't mirror the reference data, neither in sum nor in correlation.

![mapping_raw](../f/f_mot/mapping_raw.png "raw data")
_sum of overall activities and visits_

We use [linLeastSq](/geomadi/blob/master/custom/train_shapeLib.py#L808) to find the best linear weights for each cell contributing to measure the activities at the location.

```python
   def ser_sin(x,t,param): #weights times activities
        return x*t.sum(axis=0)
    def ser_fun_min(x,t,y,param): #minimizing total sum
        return ser_sin(x,t,param).sum() - y.sum()
    x0 = X.sum(axis=0) #starting values
    x0 = x0/x0.mean() #normalization
    res = least_squares(ser_fun_min,x0,args=(X,y,x0)) #least square optimization
    beta_hat = res['x']
```
_function that optimizes cells weights minimizing the total sum difference wrt reference data_

We [iterate over all locations](/geomadi/blob/master/custom/mapping_cilacDay.py) to find the best weight set using a minimum number of cells (i.e. 5)

<!-- We can calibrate the weights to optimize counts -->
<!-- ![mapping_leastSq](../f/f_mot/mapping_leastSq.png "mapping optimizing counts") -->
<!-- _activities after reweighting_ -->

<!-- or optimize correlation -->
<!-- ![mapping_corOpt](../f/f_mot/mapping_corOpt.png "mapping optimizing correlation") -->
<!-- _mapping correlation optimization_ -->

<!-- but leads to negative counts and unrealistic mapping. -->
<!-- We than sum app all the weighted cilac to the respective poi. -->

<!-- ![mapping_reweighted](../f/f_mot/mapping_reweighted.png "reweighted mapping") -->
<!-- _reweighted mapping from cilac level_ -->

![mapping linear regression](../f/f_mot/mapping_linearReg.png "linear regression")
_linear regression on cells_

## effect of filtering

We iterate over the different filters and we see a slight improvement in input data which is, on the other hand, irrelevant after weighting. 

![filter_correlation](../f/f_mot/filter_correlation.png "filter correlation")
_effect of filtering on correlation pre and post mapping_

Among all the different combination we prefere the version 11.6.1, 40 km previous distance, chirality, 0 to 2h dwelling time.

We see that chirality is stable but a third of counts doesn't have a chirality assigned.

![chirality_evolution](../f/f_mot/chirality_evolution.png "chirality evolution")
_daily values of chirality_

## effect of mapping

We monitor the effect of the different steps on the total correlation with reference values.

![correlation steps](../f/f_mot/correlation_step.png "correlation step")
_correlation monitorin after any process step_


## direction counts
We use [etl_dirCount](/geomadi/blob/master/geomadi/etl_dirCount.py) to download with beautifulSoup all the processd day from the analyzer output and create a query to the postgres database.

A [spark function](/geomadi/blob/master/geomadi/proc_lib.py) loads into all the database outputs into a pandas dataframe, take the maximum of the incoming flow and correct the timezone. 

![dir_count](../f/f_mot/dir_count.png "direction count")
_direction counts_

## capture rate

Now we check the stability of the capture rate over time and the min-max interval on monthly and daily values.

![capRate_evolution](../f/f_mot/captRate_evolution.png "capture rate evolution")
_capture rate over different locations which show a common pattern_

We see that the range of maximum and minimum capture rate is similar over different locations and we don't have problematic outliers.

![capRate_boxplot](../f/f_mot/captRate_boxplot.png "capture rate boxplot")
_capture rate boxplot over different locations_

## Software
Over the time different models were tested to select the one with the best performances and stability.

The suite basically consists in:

* [api_temperature.py](/geomadi/blob/master/geomadi/api_temperature.py) enrich location with weather information
* [geo_octree.py](/geomadi/blob/master/geomadi/geo_octree.py) flexible spatial grid and geometric algebric operations
* [kpi_vis.py](/geomadi/blob/master/geomadi/kpi_vis.py) visualization of KPIs
* [train_keras.py](/geomadi/blob/master/geomadi/train_keras.py) training with keras (tensorflow backend)
* [learn_play.py](/geomadi/blob/master/geomadi/learn_play.py) regressor on a learn/play set split with cross validation
* [bot_selenium.py](/geomadi/blob/master/geomadi/bot_selenium.py) bot to enrich location information with maps popularity lines
* [series_lib.py](/geomadi/blob/master/geomadi/series_lib.py) signal processing libraries
* [train_lib.py](/geomadi/blob/master/geomadi/train_lib.py) collections of predictors and dataset utilities
* [train_modelList.py](/geomadi/blob/master/geomadi/train_modelList.py) collection of models
* [train_execute.py](/geomadi/blob/master/geomadi/train_execute.py) routines for data preparation and iterative learning
* [geo_enrich.py](/geomadi/blob/master/geomadi/geo_enrich.py) enrich locations with geographical information
* [kernel_lib.py](/geomadi/blob/master/geomadi/kernel_lib.py) collections of kernels for image processing and convolutions
* [proc_text.py](/geomadi/blob/master/geomadi/proc_text.py) text parsing utilities to sort out research results
* [train_shapeLib.py](/geomadi/blob/master/geomadi/train_shapeLib.py) summarizes curve shapes into their most relevant statistical properties


## learn play
We use [learn_play](/geomadi/blob/master/geomadi/learn_play.py) to run a series of regressor on the time series.

Depending on the temporal resolution we use a different series of 
[train_execute](/geomadi/blob/master/geomadi/train_execute.py)

We use [kpi_viz](/geomadi/blob/master/geomadi/kpi_viz.py) to visualize the performances

![kpi_boost](../f/f_mot/kpi_boost.png "kpi of boosting")
_kpi boost_

## Long short term memory

We prepare a dataset overlapping the following information:

* reference data
* time
* activities
* footfall
* bast (isocalendar)
* historical data (isocalendar)
* mean temperature
* cloud cover 
* humidity

We can see that not only all data sources are presents

![longShort_prep](../f/f_mot/longShort_prep.png "preparation")
_input data_

We than iterate over all locations and run a forecast over 30 days using a long short term memory algorithm [train_longShort](/geomadi/blob/master/geomadi/train_longShort.py) 

![longShort_hist](../f/f_mot/longShort_hist.png "performance history")
_performance history_

We can see that the learning curve is pretty steep at the beginning and converges towards the plateau of the training set performance.


## First location set

We start preparing the data for a first set of location where:

* high number of daily visits
* low chi square, skewness, variance on reference
* high correlation blind test
* low variance long short term memory
* large cell coverage

We summarized the most important metrics in this graph 

![score_range](../f/f_mot/score_range.png "range of scores")
_range of scores, relative values, 0 as minimum, areas represent confidence interval_

and summarized in this [table](/motion/raw/tank/poi_shortlist.csv). 

Performances depend on the regularity of input data over time.

## Production
The cooperation with insight is required for:

* *backup* in the project [short term]
* *validity proof* [short term]
* *optimization* of methods [short term]
* *productization* [long term]
* harmonization of the *xy source* [short term]
* impact of *new infrastructure* on activities and footfall [short term]
* improve *spatial resolution* for activities [long term]
* improve *activity filters* [long term]

TODOs:

* insert google popularity lines
* feature importance for every location
* evaluate the model on isocalendar for feb 2019
* retrain on new reference data and include footfall

## Competitors
After the finalization of the prediction of the reference data another prediction model has to be built to derive motorway guest counts for competitor locations.

This model will take into consideration:

* telco data
* cilac labelling
* geographical data (population density, land use)
* weather data


