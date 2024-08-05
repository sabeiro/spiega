# spatial

spatial analysis and backup material

## spatial latency

Query: [resample_1sec](queries/spatial_latency.sql).
Code: [etl_spikes](src/geo_latency.py)

We analize the latency data depending on the position of the vehicle. We create a geohash per coordinate pair and calculate the average latency

![latency_geo](../f/f_tele/latency_geo.png)
_latency per geohash_

We see a similar pattern per modem upload

![latency_geo](../f/f_tele/modemTx_geo.png)
_upload per geohash_

The most interesting correlations with camera latency are on the spatial level

![geo_correlation](../f/f_tele/geo_correlation.png)
_spatial correlation_

We clearly see that incidents (`camera_latency` > 400ms) are clustered in space

![geo_incident](../f/f_tele/geo_incident.png)
_spatial distribution of incidents_

We check the cell handover

![geo_handover](../f/f_tele/geo_handover.png)
_handover cases spatially distributed_

Handover is strangely highly correlated but not with camera latency

![geo_corr](../f/f_tele/handover_corr.png)
_correlation between handover_

# backup material

Ongoing analysis

## long short term memory

Code: [stat_reample](src/stat_resample.py)

We want to asset the performances using a LSTM starting with a baseline of a single layer

We first train a model with 16 fold cross validation and we than substitute each time some random value per feature. The performance of the model with a synthetic random feature should significantly drop for the most important predictors.

![lstm_importance](../f/f_tele/lstm_importance.png)
_performance drop depending on the feature_

## dictionary learning

We create rolling windows of the time series to see how we can cluster these windows into an essential dictionary of elements.

We start first with 18 clusters composed by series of 16 data points and we create some fundamental clusters

![series_dictionay](../f/f_tele/series_dictionary.png)
_dictionary of time series windows_

We make sure that the dimension of the cluster is pretty much orthogonal

![dictionary_ortho](../f/f_tele/dictionary_ortho.png)
_orthogonality of dictionary_


