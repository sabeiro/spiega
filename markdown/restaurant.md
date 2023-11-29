# Restaurant Guests

Our scope is to predict restaurant guests from telco data. 

![capture rate](../f/f_food/capture_rate.svg "capture rate")
_deriving capture rate from footfall und activities_

The underlying *model* can be described as

$$ g_{receipts}(t) ../f/f_{people/receipt}(t) = c_{rate}^a(t) a_{act}(t) f_{ext} + c_{rate}^f(t) a_{foot}(t) f_{ext} + b_{bias}(t) $$

Where activities and footfall are not independent.

We have to understand the underlying relationship between telco data and reference data.

## Use case description

Each commercial activities that capture a fraction of the users passing by. The quote of users capture by the activity depends on:

* Type of activity
* Advertising
* Capacity
* Parking places
* Type of street
* ...
	
How exactely the capture rate depends on the specific location features is going to be investigated by training a prediction model.

## Procedure

We will proceed in the following way:

- [x] enirch location information with all the available information we have (public statistical data)
- [x] we define and calculate the score
- [x] we extract and process direction counts
- [x] we create a sensor specific mapping per location
- [x] we iterate the regressor on activities and direction count to match customer data

## Data enrichment

### Degeneracy
[Degeneracy](https://en.wikipedia.org/wiki/Degeneracy_(graph_theory)) is a measure of sparsity or replication of states, in this case we use the term to define the recurrency of pois in a spatial region.

The operative definition is to calculate the distribution of other pois at a certain distance. To reduce the complexity of the metric we perform a parabolic interpolation and define the degeneracy as the intercept of the parabola fitting the radial density distribution.

![spatial degeneracy](../f/f_food/spatial_degeneracy.png "spatial degeneracy")
_spatial degeneracy, only the intercept is taken into consideration_

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

![dens interp](../f/f_food/dens_interp.png "dens interp")
_determination of the density value coming from the neighboring tiles of the official statistics_

## Isochrone

For each location we download the local network and calculate the isochrones

![isochrone](../f/f_food/isochrone.png "isochrone")
_isochrone, selected nodes and convex hulls_

## Footfall

On a regular grid over the whole country we route all the users across the street and associate a footfall count to each tile crossing that street.

![tile footfall](../f/f_food/tile_footfall.png "footfall over a tile")
_footfall over the tiles per hour and day_

## Other metrics

We enrich the location information with street statistics 

* Bast counts: number of cars measured in the closest street 
  * `bast`
* Bast weekend factor: correction factor between workdays and weekdays, distinguish between commuter and touristic stretches
  * `bast_fr`, `bast_su`: correction factors for friday and sunday

## Time series preprocessing
We see anomalous peaks and missing points in reference data which we have substituted by the average

![visit hourly](../f/f_food/visit_hourly.png "Hourly visit seris")
_hourly visits and footfalls over all locations_

We can see that the main difference between in the daily average is the midday peak

![visit daily](../f/f_food/visit_daily.png "Daily visits")
_daily visits and footfalls over all locations_

Customer data are more regular than footfall data

![visit daily values](../f/f_food/visit_series.png "time series of visits")
_total daily visits and footfalls over all locations_

We create a matrix representation of the input data to speed up operations
![matrix representation](../f/f_food/input_data.png "input data in matrix representation")
_matrix representation of footfall and visits and their mutual correlation_

## sensor mapping

We calculate daily values of activities per sensor and we use correlation as scoring to understand how the influence of neighboring sensors can describe visitors.

We first calculate sensor cross correlation and keep only consistent sensors

![cilac crosscor](../f/f_food/cilac_crosscor.png "sensor cross corelation")
_sensor cross correlation_

We than run a regression to estimate the weighting of the sensor activities versus visits. We filter out the most significant weight and we rerun the regression.

We do a consistency check and cluster the cells as restaurant activities.

If we consider all sensor with weight 1 we score 11% (of the location over 0.6 correlation)
![map unweighted](../f/f_food/cilacMap_weighting.png "map weighted")
_unweighted and weighted sensor mapping_

If we weight all sensors performing a linear regression we score 66%

## KPI

We calculate the first score, ~cor~, as the Pearson's r `correlation`:
$$ r = \frac{cov(x,y)}{\sigma_x \sigma_y} $$

We calculate the `relative difference` as:
$$ d = 2\frac{\bar{x}-\bar{y}}{\bar{x}+\bar{y}} $$

And the `relative error` as:
$$ s = 2\frac{\sqrt{\sum (x - y)^2}}{N(\bar{x}+\bar{y})} $$

We have few location where footfall correlates with visitors and we don't see a clear dependency between scoring and location type.

![boxplot foot_vist](../f/f_food/boxplot_foot_vist.png "boxplot foot_vist")
_boxplot foot_vist_

If we consider daily values activities and footfall don't correlate at first with reference data.

![kpi cross](../f/f_food/kpi_cross.png "kpi cross")
_performances over sources_

Activities and footfalls have a good correlation.

## Regression

We perform a regression of measured data versus reference receipts and we calculate the performance over all locations.

The first regressor is country wide, the second is site type specific:

* maps the sensors giving a specific weight (bayesian regressor)
* groups the sensors and sum up the activities for the specific location - performance 10%
* country wide regressor on activity - performance 41%
* location type specific regressor on activity- performace 57%
* country wide regressor on footfall - performance 55%
* location type specific regressor on footfall- performace 68%
* country wide regressor on hybrid - performance 76%
* location type specific regressor on hybrid- performace 76%

![kpi hybrid](../f/f_food/kpi_hybrid.png "kpi hybrid")
_performance over iterations_

We can see that an hybrid model is the best solution to cover 3/4 of the locations.

## Feature selection counts

We have collected and selected many features and we have to simplify the parameter space:
![feature correlation](../f/f_food/feature_correlation.png "correlation of features")
_correlation between features_

We select the features which have the higher variance.
![feature_variance](../f/f_food/feature_variance.png "variance of features")
_relative variance of single features_

We can see that the selected variances are mutally well distributed
![feature selection](../f/f_food/feature_selection.jpg "mutual distribution of selected features")
_mutual distribution of selected features_

## Features knock out

We are interested in understanding which time series is relevant for the training of the model. 
To quantify feature importance instead of using a different model that returns feature importance (like xgboost or extra tree classifier) but might not correspond to the importance of the real model we just retrained the model removing each time one of the feature.

First we fix pair of locations (one train one test) and we retrain the models without one feature to see how performances change depending on that feature.

![feature knock out](../f/f_food/feature_knockout_fix.png "feature knock out")
_feature importance on performances, fix pair_

If we train on one location and we test on a different random location we don't have stable results to interpret

![feature knock out](../f/f_food/feature_knockout.png "feature knock out")
_feature importance on performances_

## Prediction on daily visits

We want to predict the number of visits based on pure geographical data by running a regressor with cross validation 

![re../f/f_vs_pred](f_food/ref_vs_pred.png "reference versus prediction")
_reference vs prediction_

Now we have to iterate the knowledge over unknown locations.

## Time series prediction

We use a long short term memory with [keras](https://machinelearningmastery.com/time-series-forecasting-long-short-term-memory-network-python/) to create a supervised version of the time series and forecast the time series of another location.

We use [train_longShort](/geomadi/blob/master/custom/train_longShort.py) to load and process all the sources.

For each location we take the following time series shifting each series by two steps for the preparing the supervised data set.

![time series](../f/f_food/time_series.png "time series")
_set of time series used_

We can see that in few epochs the test set performance converges to the train set performance.

* Training time: 8 min

![longShort_hist](../f/f_food/longShort_hist.png "long short histogram")
_learning cycle_

The test group consists in a random location taken within the same group. We see that performances don't stabilize over time but rather get worse which depends on the type of location as we can see later.

![score history](../f/f_food/score_history.png "score history")
_score history_

Overall performances are good for relative error and relative difference for correlation we will se that performances are strongly type dependent.

![kpi_fix_valid](../f/f_food/kpi_fix_valid.png "kpi fix valid")
_kpi for fixed validation set_

A fix validation set is not necessary since performances stabilizes quickly over time.

![kpi_err_diff](../f/f_food/kpi_err_diff.png "kpi error difference")
_kpi relative error and relative difference_

Relative error as a regular decay while correlation has a second peak around 0.4

![kpi_hist](../f/f_food/kpi_hist.png "kpi histogram")
_kpi histograms_

We indeed see that we have good performances on a freestander with drive but the satellite significantly drops overall performances

![kpi_boxplot](../f/f_food/kpi_boxplot.png "kpi boxplot")
_kpi distribution per type_

