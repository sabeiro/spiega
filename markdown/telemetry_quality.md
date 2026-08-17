---
title: "activation"
author: Giovanni Marelli
date: 2019-09-12
rights:  Creative Commons Non-Commercial Share Alike 3.0
language: en-US
id: telemetry_quality
category: #tech
roam_refs: telemetry quality
roam_aliases: ["activation potential"]
output: 
	md_document:
		variant: markdown_strict+backtick_code_blocks+autolink_bare_uris+markdown_github
---

# telemetry quality

# camera latency 

Camera and control latencies are a crucial problem for teledriving, we need to understand which features are good predictors for understanding what causes latencies.

![spike_events](../../f/f_tele/spike_events.png)
_camera latency spike events_

In this report we analyse:

* which features are important for **latency prediction**
* which features are important for **spike prediction**
* how early can we reliably **forecast a spike** event

## previous analysis

We start from this previous analysis where 19 features were used to predict `e2e_latency`. 
Data were collected [upsampling](resampled_latencies_1sec_prod.sql) all features up to a second, defining the spike as a [latency](STG_high_latency_agg.sql)  lager than 400ms, filtering out the warehouses and [extracting the features](ml.sql).

![previuos_analysis](../../f/f_tele/prev_analysis.png)
_notebooks of the previous analysis_

Features are [resampled](ta_features_extract.ipynb) every 4 seconds, [plotted](ta_featues_eda.ipynb), and a [xgboost](ta_features_predict.ipynb) classifier is applied on the data. 
The prediction is on 4 seconds bins where the maximum of `e2e_latency` is above 400ms is classified as `label:1`.

# [data quality](telemetry_data_quality.md)

Report on the data quality, ingestion, stream, plausibility

![telemetry_matrix](../../f/f_tele/telemetry_matrix.png)
_firing behaviour for telemetry features_

Every sensor has a topic which fires to the backend at a rate from 1Hz to 50Hz. `networking` information comes every second while `computing` and `vehicle_dynamics` more frequently. 
We spot which features are redundant and we check obvious dependecies with `camera_latency`

# [data sets](telemetry_data_sets.md)

Preparation of the datasets for the training, feature selection and denoising

![series_deci](../../f/f_tele/series_deci.png)
_time series on deci seconds_

We prepare different data sets:

* telemetry data, one second sampling
* telemetry data, one deci second sampling
* network_log data, one deci second sampling

For each we create a series of spike events (+/- 60 seconds from spike) and created a denoised average of all series

# [time ordering of events](feature_relevance.md)

Investigation on time ordering of events, investigating causal dependecy

![series_deci](../../f/f_tele/delay_deciCell.png)
_time series on deci seconds_

We define a method to calculate the time persistance and the time shift between features.
Persistance shows more interesting results than correlation and really points out when two features have a causal relationship. 
Time shift is a delicate measurement since doesn't always lead to consistent results. We show that networking features are mostly preceeding spikes and we compute the time shift for every single series to classify networking related spikes from computing related.

# [prediction](telemetry_prediction.md)

Prediction of `camera_latency` to spot the most relevant features for training the model. 

![series_deci](../../f/f_tele/networking_forecast.png)
_spike prediction with networking features_

We iterate over different models and feature sets to identity the most performant combination. 
We predict as well the risk of a spike.
We end up using a long short term memory with few layers.

# [forecast](telemetry_forecast.md)

We use the prediction model to run a forecast on the `camera_latency` for the next few seconds.

![series_deci](../../f/f_tele/forecast_flat.png)
_forecast for every series, for every starting point_

We calculate the accuracy of the forecast depending on the anticipation time. The reliability of the model increases close to the spike.

# [spatial](telemetry_spatial.md)

We investigate the spatial dependency of spikes.

![latency_geo](../../f/f_tele/latency_geo.png)
_latency per geohash_

We clearly see a spatial pattern where the latency is larger in particular areas of the city.
