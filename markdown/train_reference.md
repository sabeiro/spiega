# visits vs activities

Our customer knows how many *sales receipts* are issued with an hourly resolution over around 400 gas stations in the country.

We call the reference data *visits* and our measured data *activities*. 

### Skews
To map activities into visits we have to correct different skews:

1.  [*homogenity*](#skew-i---homogenity) missing values
2.  [*hourly*](#skew-ii-hourly) phase shift
3.  [*volatility*](#skew-iii---volatility) big fluctuations
4.  [*learning capability*](#skew-iv---learning-capability) trainable locations
5.  [*holiday*](#skew-v---holiday) tail effects
6.  [*missing sources*](#skew-vi---missing-sources) partial missing data
7.  [*extrapolation factor*](#skew-vii---extrapolation-factor) for motorway drivers
8.  [*market share*](#skew-viii---market-share) business phone users on the motorway
9.  [*weather*](#skew-ix---weather) influences motorway behaviour
10. [*commuter vs touristic*](#skew-x---commuter-vs-touristic) road segment traffic per week day
11. [*population density*](#skew-xi---population-density) high populated areas show large deviations
12. [*directions*](#skew-xii---directions) distinction uncertanty
13. [*distance filter*](#skew-xiii---distance-filter) optimal configuration
14. [*low counts*](#skew-xiv---low-counts) lower precision
15. [*type of device*](#skew-xv---type-of-device) road segment dependent
16. [*people/car vs people/receipt*](#skew-xvi---peoplecar-vs-peoplereceipt) who is driving, who is paying

### Project references
The project considers the following quantities:

| project  | numbers |
|---------------|-----|
|Owned locations | 417 | 
|Total locations | 1184 | 
|clusters | 824 | 
|zones | 503 |
|cilacs | 2508 - 3025 | 
|daily visits < 1k2 | 50% |

The customer expectation are summarized in 4 KPIs:

|KPIs | threshold | goal loc % |
|-----|------|----|
|correlation $\rho$ | > 0.6 | 80%|
|difference $\delta$ |  < 0.2 | 80% |
|capture rate| 0.5% <> 9% | 80% |
|passanger/car| 1.1 <> 1.9 | 80% |

![daily_visit](../f/f_mot/daily_visit.png "distribution of daily visits")
_distribution of daily visits_


## Raw data
Raw data consists in numbers of receipts per hour per location.
We present the data week per week to show the differences between locations:

![raw data](../f/f_mot/ref_series.png "reference time series")
_reference time series, each panel present a different location and a different week. A week is represented as an image of 7x24 pixels_

Locations show different patterns about daily and weekly peaks. Sometimes deviations between two days or two hours are really strong. 

## Skew I - homogenity
#### missing values
We homogenize the data converting the time series into matrices to make sure we have data for each our of the day. We than replace the missing values interpolating:

![replace_nan](../f/f_mot/replace_nan.png "data homogenity")
_replace missing values via interpolation_

## Skew II - hourly
#### smoothing
In order to compensate the effects of time shifting (can counts double within two hours?) we apply a interpolation and smoothing on time series:

![re../f/f_smoothing](f_mot/prep_poly_smooth.png "smoothing of reference data")
_to the raw reference data we apply: 1) polynomial interpolation 2) smoothing_

## Skew III - volatility
#### chi square distribution
Some locations are particularly volatile and to monitor the fluctuations we calculate the $\chi^2$ and control that the p-value is compatible with the complete time series. 
We substitute the outliers with an average day for that location and we list the problematic locations.

![re../f/f_volatility](f_mot/chisq_dis.png "chi square of the reference time series")
_Distribution of p-value from $\chi^2$ for the reference data_

We than replace the outliers:

![replace_volatility](../f/f_mot/replace_volatile.png "we replace volatile days with an average day")
_outliers are replaced with the location mean day, left to right_

## Skew IV - learning capability
#### deep learning autoencoder
We build an autoencoder which is a model that learns how to create an encoding from a set of training images. In this way we can calculate the deviation of a single image (hourly values in a week 7x24 pixels) to the prediction of the model.

![week_image](../f/f_mot/week_img.png "image representation of many weeks")
_sample set of training images, hourly counts per week_

In this way we can list the problematic locations and use the same model to morph measured data into reference data.

We train a deep learning model on images with convolution:
![tensorboard](../f/f_mot/tensorboard.png "sketch of the learning phases")
_sketch of the phases of learning_

We than test how the images turn into themselves after the prediction of the autoencoder.

![raw_vs_predicted](../f/f_mot/ref_pred.png "results of predictor")
_comparison between input and predicted images_

We can than state that **88% of locations** are not well predictable by the model within 0.6 correlation.
![autoencoder_performance](../f/f_mot/autoencoder_performance.png "autoencoder performance")
_distribution of correlation for autoencoder performances: correlation on daily values_


## Skew V - holiday
Holidays have a huge effect on customer side. 
The plot shows activities and visits for the month of March, the last Thursday of the month prior to easter shows a huge variation only on reference data. 

![holiday_effect](../f/f_mot/thursday_series.png "proximity to easter")
_Visits versus activities in Mach approaching easter_

The same effect was seen in March 2017 in the test data.
![test_days](../f/f_mot/correlation_map.png "visits increased closed to easter")
_Easter effect is visible only on reference data, blue line_

## Skew VI - missing sources
Gas stations are sometimes composite, we don't receive complete information about all the visits in the area.

![location_overview](../f/f_mot/location_overview.png "composite gas stations")
_in same cases we don't know the receipt counts for some buildings on the gas station_

## Skew VII - extrapolation factor
We should consider which extrapolation factor has to be used for motorway drivers:

1. *first signal* wrong in case of drivers sleeping in a hotel
2. *local share* wrong for long distance drivers
3. *daily fluctuations* dependent on road type
4. *high density areas* induce a bias

Some road segments have large fluctuations and large mismatch between visits and activities
A81 Stuttgart - Friedrichshafen:
![act_vist](../f/f_mot/act_vist_cor.png "activities vs visits with low correlation")
_for some locations fluctuations are large and activities and visits don't correlate_

## Skew VIII - market share
Our user base is mainly composed by business traveller that during week days might represent over 50% of the market share on the motorway during working days. 
During weekends the number of business traveller is lower represented, especially on sundays.

We see a large discrepancy in the difference between visits and activities depending on week days.
![weekday_deviation](../f/f_mot/weekday_deviation.png "weekday deviations")
_boxplot of the difference between visits and activities depending on the week day_

## Skew IX - weather
Weather has an influence on deviation as well, we can show for example how the minimum temperature influences the mismatch.
![deviation_temperature](../f/f_mot/deviation_temperature.png "deviation temperature")
_deviation vs minimum temperature, binned_

We select the most relevant weather features over a selection of 40.
![weather feature](../f/f_mot/weather_feature.png "weather features")
_correlation between weather features_

Other weather related parameters have an influence on the mismatch.
![weather_correlation](../f/f_mot/weather_correlation.png "weather influences the difference")
_weather has an influence on the deviation: di../f/f_

We use the enriched data to train a regressor to adjust the counts.

## Skew X - commuter vs touristic
Each street has a different pattern concerning the week day. We can simplify the cataloge classifying street segments with the label commuter or touristic. 
We use the [kears library](/geomadi/blob/master/geomadi/train_keras.py) to [load and parse](/geomadi/blob/master/custom/train_convTimeSeries.py) [bast data](/motion/raw/bast).

![bast raw](../f/f_mot/bast_weeks.png "bast raw data")
_BaSt raw data, some locations have a daily double peak, some locations have more traffic on the weekend_

We control the performances of an autoencoder on BaSt raw data:

![bast autoencoder](../f/f_mot/bast_autoencoder.png "bast autoencoder")
_Performances of the BaSt autoencoder, fluctuations are flattened_

Commuter segments show higher counts during the week, the touristicc over the weekends. 
Our reference data are the BaSt counts which provide a correction factor for the weekday, especially friday and sunday:

![correction_dirCount](../f/f_mot/corr_dirCount.png "correction of direction counts")
_correction of direction counts, our numbers counter correlate with reference numbers_

We don't find any significant correlation between BaSt and visits.

## Skew XI - population density
Population density has an influnce on mismatch
![bad_correlation](../f/f_mot/correlation_bad_city.png "bad correlation in dense area")
_we see bad correlation in dense areas (blue diamond) and good correlation in less populated areas (red diamond_

For our training we than consider as well information about population density in an area of 2 km.
![data_enrichment](../f/f_mot/data_enrichment.png "density population data")
_we enrich our data with information about population density_

## Skew XII - directions
Sometimes direction distiction does not perform well
![correlation_direction](../f/f_mot/correlation_1bad_1good.png "direction distinction not performing")
_we have good correlation on one side of the motorway (red diamond) and poor correlation on the other side (blue diamond)_

## Skew XIII - trip distance filter
Motorway drivers show an elasticity effect: their cell phone is bounded in a cell for a distance longer than a walker. In many cases BSEs do not cover the region of the gas station.
We than consider many cells around the gas station:
![curve_overlapping](../f/f_mot/curve_overlapping.png "cilacs and reference data")
_example of reference data (thick line) and the activity counts of the cells in its neighborhood_

We than apply a trip distance filter to select only users that had traveled a certain amount of km prior to the activity.
The filter is optimized on reference data but don't describe the real activities of motorway drivers.
![counts_filter](../f/f_mot/filter_asymmetric.png "counts depending on distance filter")
_trip distance filter optimized on activity counts_

## Skew XIV - low counts
We see that low counts have an higher relative error.

Locations with few visits per day are the hardest to match, precision depends on absolute numbers.

![di../f/f_abs](f_mot/dif_abs.png "low visits, lower precision")
_boxplot of counts deviation relative to number of visitors_

## Skew XV - device type
Tracks are guests of specific gas stations and carry different devices.

![track_stop](../f/f_mot/track_stop.png "preferred track stop")
_huge parking spot for tracks_

## Skew XVI - people/car vs people/receipt
The number of people per car changes over weekday. We expect a similar behaviour in the numer of people per receipt.

![people_car](../f/f_mot/people_car.png "profile of people per car")
_deviation of the mean number of people per car during a week (red line)_

## Feature importance

We studied the statistical properties of a time series collecting the most important features to determine data quality.
![stat prop](../f/f_mot/stat_prop.png "statistical properties")
_most important statistical properties of time series_

We calculate the feature importance on model performances based on statistical properties of time series of reference data.
![importance statistical properties](../f/f_mot/importance_statProp.png "importance of statistic properties")
_we obtain a feature importance ranking based on 4 different classification models_


* `daily_vis`: daily visitors
* `auto_decay`: exponential decay for autocorrelation --> wie ähnlich sind die Tagen
* `noise_decay`: exponential decay for the power spectrum --> color of the noise
* `harm_week`: harmonic of the week --> weekly recurrence
* `harm_biweek`: harmonic on 14 days --> biweekly recurrence
* `y_var`: second moment of the distribution
* `y_skew`: third moment of the distribution --> stationary proof
* `chi2`: chi square
* `n_sample`: degrees of freedom

We try to predict model performances based on statistical properties of input data but the accuracy is low which means, as expected, that the quality of input data is not sufficient to explain the inefficiency in the prediction.
![stat prop traininig](../f/f_mot/statProp_training.png "training on statistical properties")
_training on statistical properties of input data vs model performances_

We now extend our prediction based on pure reference data and location information
![feature importance](../f/f_mot/feature_importance.png "feature importance")
_feature importance based on location information and input data_

Knowing the location information we can predict the performace within 80% of the cases.
![confusion matrix](../f/f_mot/confusion_feature.png "confusion matrix on input feature")
_confusion matrix on performance prediction based on location information_



## Regression
All the skews we have shown are used to train predictors and regressors to adjust counts:
![model_score](../f/f_mot/model_score.png "performance of models")
_ROC of different models on training data_

Thanks to the different corrections we can adjust our counts to get closer to reference data.
![regressor_curves](../f/f_mot/regressor_curves.png "curves after regressor")
_corrected activities after regressor_

We have structure the analysis in the following way:
![year structure](../f/f_mot/year_structure.png "structure for yearly delivery")
_structure of the calculation for the yearly delivery_

We can than adjust most of the counst to meet the project KPIs

![kpi_dist](../f/f_mot/kpi_dist.png "distribution of KPIs")
_distribution of the KPIs $\rho$ and $\delta$_

## Other reference data
We have scraped from internet other reference data to evaluate the accuracy of our models: i.e. google maps, which consists in normalized time series called *popularity*.

![google_popularity](../f/f_mot/google_popularity.png "popularity from google")
_popularity of a gas station and the css attributes we scrape from internet_

Screaping the page we can extract the information about the curves [etl_google.js](/geomadi/blob/master/nodejs/console.js). 
```javascript
var occTime = []
$.each( $('.section-popular-times-graph'), function(i,curveL) {
    $('.section-popular-times-value',curveL).each(function(j,labL) {
	occTime.push(labL.parentNode.attributes['aria-label'].nodeValue);
   });
});
copy(occTime);
```
A more sofisticated project uses selenium [selenium.js](/geomadi/blob/master/nodejs/selenium.js) to create a bot which searches for a location with the same name of the POI. It selects the more plausible result using [Levenshtein distance](https://en.wikipedia.org/wiki/Levenshtein_distance), waits the page to be loaded and reads the css attributes for the popularity curves and saves them.

We can then overlap the curves and calculate the mutal agreement between sources
![vis_act_pop](../f/f_mot/vis_act_pop_curve.png "visits, activities, popularity")
_activities, visits and popularity for a location_

We than see that the agreement between visits and activities is the largest.
![vis_act_pop_dis](../f/f_mot/vis_act_pop_dis.png "accuracy between sources")
_accuracy between activities, visits and popularity_

## Correlation with restaurants
We now see the correlation between a service station and a restaurant.

To build the comparison we build first a *pseudo day*, ex:

* '19-06-08' : calendar week-weekday-hour

Service station and restaurant share the same location
![tank_mc](../f/f_mot/tank_mc.png "service station and restaurant")
_Both activities share the same potential customers_

If we look at the correlation between locations on the same platform:

| `id_poi` | `cor_d` | `cor_h` | `rank_d` | `rank_h` |
|------|------|------|------|------|
|1020| 0.41 |0.57|0.14|0.68|
|1033| 0.39 |0.68|0.30|0.72|
|1043| 0.37 |0.64|0.48|0.71|
|1222| 0.26 |0.63|0.25|0.66|
|1289| 0.60 |0.53|0.51|0.62|
|1518| 0.27 |0.73|0.31|0.78|
|1545| 0.40 |0.62|0.49|0.69|

_`cor_` Pearson correlation, `rank_` Spearman correlation, `_d` daily values, `_h` hourly values_

Althought the hourly values have a good correlation (same daily trend) daily values have an unpredictable result.

Service station and restaurant share the same location
![restaurant_service](../f/f_mot/restaurant_service.png "service station and restaurants")
_difference between the curves, daily values don't correlate on a pseudo day_

If we refer to a real day we have a strong correlation:

|id_poi| cor_d| cor_h |
|--------|---------|------|
|1020  |0.75  |0.66|
|1033  |0.85  |0.77|
|1043  |0.76  |0.71|
|1222  |0.86  |0.66|
|1289  |0.82  |0.66|
|1518  |0.82  |0.82|

![restaurant_service](../f/f_mot/restaurant_service_day.png "service station and restaurants")
_correlation between service and restaurant on equal days_

That means that we have a bad definition of a pseudo day and we have big fluctuations within days.

## Competitor locations
The scope of the project is to count how many motorway drivers stopped by a competitor. 
The current definition of a competitor is weak since a motorway driver has a more dense options to stop for fuel/eating:
![competitor_location](../f/f_mot/competitor_location.png "competitor locations")
_customer locations (blue) and competitor ones (purple), a driver has many more options than the ones pointed (from google maps)_

It would be much more reliable to label all the users who have been routed on a motorway and report all the activity with a short dwelling time:

![heatmap](../f/f_mot/heatmap.png "motorway stoppers heatmap")
_heatmap of motorway drivers stopping during a trip_

## Final remarks
* The mapping between activities and visits need *over 15 correction factors* to balance all the skews seen 
in the data. 
* *Postprocessing corrections* seem to be the only realistic way to correct the mismatch.
* The extreme training of the data *masks important insights* in describing the behaviour of motorway drivers.
