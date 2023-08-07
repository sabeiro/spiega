# Motorway Stoppers
## Use case description
_______________
On the motorway there are isolated [gas stations](172.25.100.50/home/gmarelli/lav/motion/raw/tank/poi.csv). Few activities but few cells too.

![gas stations on the motorway](../f/f_mot/motorway_01.png "Gas stations")
_Blue arrows show the gas stations and the direction of the traffic and the green dots the position of the centroids of the cell_

We should be able to isolate inhabitants between stoppers on the motorway.
We want to distinguish as well the direction where the drivers come from.
Gas stations might be:

1. Compact
  * Compact with separation
2. Single
3. Composite

![location overview](../f/f_mot/location_overview.png "overview of the different gas stations")
_satellite views of different gas station locations_

And the can be present on both sides.
We can have up to 4 sources of *bills* per side (restaurant, gas stations, rest rooms) and we should be able to attribute a corresponding number of people per bill. We are currently using the maximum per hour between all sources per building.
>**How can we filter our data to detect motorway stoppers?**

We use a combination of filters 

1. *time duration* (between 0.5 to 2 hours)
2. *length* of the previous trip (from 30 or 50 km on)
3. we distinguish the *direction* of the previous trip
4. label cilacs from curve *shapes* 

From our users we know:

* Where they have *activities* (persistance whithin the same cell)
* How they split their journey into *trips* (displacement between activities)

For the test pilot we will consider three days in april '17 to tune and validate the model.
## Procedure
We structure the work in the following way:

- [x] select neighbouring cells
- [x] calculate activity profile
- [x] [filter](#filtering) by duration, trip distance
- [x] multiply user count by duration of activity
- [x] [load and format](#etl) customer inputs 
- [x] cluster locations within analysis resolution
- [x] [enrich](#data-enrichment) location information with geo data
- [x] [cluster](#shape-clustering) activity by curve shapes
- [x] define [scores](#scoring) based on correlation and regression
- [x] [train](#training) the model and label the whole dataset
- [x] [select](#training-results) the best scoring cells
- [x] sum up cells within the same location and [recompute the score](#training-results)
- [x] calculate [correction factors](#correction-factors) location dependant
- [x] [analyze](#result-visualization) the reasons for low correlation/low match
- [x] calculate activity profiles for locations with no reference data
- [x] route all users on the country infrastructure
- [x] select the tiles crossing the motorway in front of the gas station
- [x] count the car drivers on the route
- [x] calculate [capture rate](#capture_rate)


## Data quality
We performed some quick check about consistency in the data.

The distribution of the trip distance is regular
![distance distribution](../f/f_mot/trip_distance_distribution.png "distribution of the trip distance")
_Distribution of the trip distance_

Duration as irregular distribution apart from half hour binning
![duration distribution](../f/f_mot/duration_distribution.png "distribution of the duration")
_Distribution of duration_

We can than observe that chirality wihtin a day is conserved:
![chirality distribution](../f/f_mot/chirality_distribution.png "distribution of chirality")
_$\chi$=0 and $\chi$=1 are equally distributed, chirality 1 and 2 are two alternative definitions_

## ETL
We preprocess customer data with [etl_tank.py](http://172.25.186.11:8000/gmarelli/geomadi/blob/master/etl/etl_tank.py) where we load customer bills counts and locations:
```python
vist = pd.read_csv(baseDir + "raw/tank/poi_tank_visit.csv")
bist = pd.read_csv(baseDir + "raw/tank/poi_tank_visit_bon.csv").fillna(method='ffill')
tvist = pd.read_csv(baseDir + "raw/tank/poi.csv")
```
We filter out only the typical heavy traffic hours and convert the timestamp:
```python
bist = bist.loc[ [x>5 for x in bist['hour']] ]
bist = bist.loc[ [x<24 for x in bist['hour']] ]
bist.loc[:,'time'] = bist[['day','hour']].apply(lambda x:'2017-04-%sT%02d:00:00' % (x[0][0:2],x[1]),axis=1)
```
We sort all the cilacs within a certain sphere in the same cluster:
```python
disk = ((cells['X']-x_c)**2 + (cells['Y']-y_c)**2)
disk = disk.loc[disk <= max_d**2]
cellL.loc[dist.index,"cluster"] = c["cluster"]
```
We prepare then the data to be structure on a matrix, cells on the rows, time along columns.
![input data](../f/f_mot/input_data.png "representation of the input data")
_matrix representation of the input data_

## Filtering
We apply a distance filter to select only the motorway stoppers among all the activities captures by the cell in the area [etl_tankAct.py](http://172.25.186.11:8000/gmarelli/geomadi/blob/master/etl/etl_tankAct.py).

We apply different trip distance filters on the input data:
* prev: on the previous trip
* sym: symmetric, previous + following trip
* asym: asymmetric, previous ~and~ following trip

![trip distance filter](../f/f_mot/trip_filter.png "trip distance filter")
_Trip distance filter_

Trip distance filter has different effect on every single cell.
![distance filter](../f/f_mot/distance_filter.png "filter on the trip distance")
_Effect on the trip distance filter on correlation with reference data, the smaller the circle the higher the trip distance filter, the redder the color the higher the correlation_

We can see that for some cells we have a positive effect of the filter while in some case even counterprodictive effect. Some cells are not correlated at all with the activities at the gas station.

### Direction distinction
To distinguish between directions on the motorway we use a metric that distinguish the orientation which can be clockwise or counter clockwise wrt a reference point which we put in the center of the country. The metric is called chirality and is calculated by:
$$\chi = \frac{\vec v \times \vec w}{||v|| + ||w||} > 0  $$
Where $\vec v$ is the vector connecting the previous activity to the current activity and $\vec w$ the center of the country with the previous activity. 

![direction dinstinction](../f/f_mot/direction_distinction.png "distinction by direction")
_The color of the arrows show the opposite chiralities_
We see that chirality distinguishes both sides of the motorway and is independent on the current angle.
```python
deCenter = [10.28826401, 51.13341344]
start = self.events[0].coordinates
end = self.events[-1].coordinates
v1 = [start[0] - deCenter[0],start[1] - deCenter[1]]
v2 = [end[0] - start[0],end[1] - start[1]]
crossP = v1[0]*v2[1] - v2[0]*v1[1]
return 1.*(crossP > 0.)
```
_vector product between trip and conjunction to the center of Germany_

We can see that we have correctly distinguished the trips dependent on the chirality.
![chirality trajectory](../f/f_mot/chirality_trajectory.png "trajectories colored by chirality")
_trajectories colored by chirality_

## Shape clustering
We want to recognize the type of user clustering different patterns:

![user patterns](../f/f_mot/shapeCluster.svg "different patterns for kind of user")
_different patterns for kind of user_

We calculate characteristic features by interpolating the time series. We distinguish between a *continous time series* where we can calculate the overall trends via the class [train_shapeLib.py](http://172.25.186.11:8000/gmarelli/geomadi/blob/master/py/train_shapeLib.py)

![time series](../f/f_mot/time_series.png "example of a time series")
_time series of a location_
and the daily average where we can understand the typical daily activity.

![daily average](../f/f_mot/time_series_day.png "daily average")
_daily average of a location_
Many different parameters are useful to improve the match between mobile and customer data, parameters as position of the peak, convexity of the curve, multiday trends help to understand which cells and filters are capturing the activity of motorway stoppers.

![shape clustering](../f/f_mot/shape_clustering.png "We cluster curves by shapes")
_clustering curves (average per cluster is the thicker line) depending on different values of: intercept, slope, convexity and trend_

Unfortunately no trivial combination of parametes can provide a single filter for a good matching with customer data. We need then to train a model to find the best parameter set for cells and filter selection.

## Feature selection
We need to find a minimal parameter set for good model performances and spot a subset of features to use for the training.
We realize that some features are strongly correlated and we remove highly correlated features

![correlation matrix](../f/f_mot/correlation_matrix.png "correlation matrix between features")
_correlation between features_

|name           | description        | variance     |
|-------------  | :---------------   | -----------: |
|trend1         | linear trend       | 5.98 |
|trend2         | quadratic trend    | 4.20 |
|sum            | overall sum        | 1.92 |
|max            | maximum value      | 1.47 |
|std            | standard deviation | 1.32 |
|slope          | slope $x_1$        | 1.11 |
|type           | location facility  | 1.05 |
|conv           | convexity $x_2$    | 0.69 | 
|tech           | technology (2,3,4G)| 0.69 |
|interc         | intercept $x_0$    | 0.60 |
|median         | daily hour peak    | 0.34 |

High variance can signify a good distribution across score or a too volatile variable to learn from.

We select five features which have larger variance to increase training cases.

![selected features](../f/f_mot/selected_features.png "final selection of features")
_final selection of features_

## Scoring
We use the class [train_shapeLib.py](http://172.25.186.11:8000/gmarelli/geomadi/blob/master/py/train_shapeLib.py) to calculate the score between users data and customer data. 
We calculate the first score, ~cor~, as the Pearson's r *correlation*:
$$ r = \frac{cov(X,Y)}{\sigma_x \sigma_y} $$
This parameter helps us to select the curves which will sum up closely to the reference curve. 

![scoring explanation](../f/f_mot/scoring.png "scoring graphical visualization")
_the superposition of many curves with similar correlation or many curves with heigh regression weights leads to a good agreeement with the reference curve_
The second parameter, the *regression* ~reg~, is the weight, $w$, given by a [ridge regression](http://172.25.186.11:8000/gmarelli/geomadi/blob/master/py/train_shapeLib.py#L317) 
$$ \underset{w}{min\,} {{|| X w - y||_2}^2 + \alpha {||w||_2}^2} $$
where $\alpha$ is the complexity parameter.

The third and last score is the absolute *difference*, ~abs~, between the total sum of cells and reference data:
$$ \frac{|\Sigma_c - \Sigma_r|}{\Sigma_r} $$ 
per location

## Training
We loop over different model using the class [train_lib.py](http://172.25.186.11:8000/gmarelli/geomadi/blob/master/py/train_lib.py) on the script: [train_tank.py](http://172.25.186.11:8000/gmarelli/geomadi/blob/master/py/train_tank.py)

First of all we have to bin the scores into classes using the function [binOutlier](http://172.25.186.11:8000/gmarelli/geomadi/blob/master/py/train_filter.py#L14) which clamps the outliers into boundary bins. For each score we choose the propriate threshold for the outliers.
```python
n = nBin
ybin = [threshold] + [x*100./float(n-1) for x in range(1,n-1)] + [100.-threshold]
pbin = np.unique(np.nanpercentile(y,ybin))
n = min(n,pbin.shape[0])
delta = (pbin[n-1]-pbin[0])/float(n-1)
pbin = [np.nanmin(y)] + [x*delta + pbin[0] for x in range(n)] + [np.nanmax(y)]
t = np.array(pd.cut(y,bins=np.unique(pbin),labels=range(len(np.unique(pbin))-1),right=True,include_lowest=True))
t[np.isnan(t)] = -1
t = np.asarray(t,dtype=int)
return t, pbin
```

![score binning](../f/f_mot/bin_correlation.png "binning the correlation score")
_distribution of the correlation score and the corrisponding binning_

We compare the different models and select the best perfroming for the purpose.

![model score](../f/f_mot/model_score.png "result and score of the models")

We further [tune](http://172.25.186.11:8000/gmarelli/geomadi/blob/master/py/train_lib.py#L178) the best performing model.
Alternatively we use keras for high performace model tuning: [train_neural.py](http://172.25.186.11:8000/gmarelli/geomadi/blob/master/py/train_neural.py)

We observe different performances between models, we use the model with best train score and area under curve. 

We observe that all the scores have a good post prediction agreement (apart from regression)

![box plot post prediction](../f/f_mot/boxplot_post.png "box plot post prediction assignment")
_for each variable score we see how the predicted bins (b prefix) classify the input scores (y prefix)_

## Training results

The steps are mainly performed in this script [train_tank.py](http://172.25.186.11:8000/gmarelli/geomadi/blob/master/py/train_tankTest.py). 

The first score we want to optimize is the correlation. We can indeed see how the model filtered the cells leaving the ones with higher correlation.

![correlation distribution after filtering](../f/f_mot/correlation_distribution.png "correlation distribution after filtering")
_density plot of correlation before and after the filter and dependent on different metrics_

We select the cells that have the highest correlation scores and we limit the number of cells by the highest regression.

We then sum up all the cells within the same cluster and recalculate the correlation between locations.

![matrix correlation](../f/f_mot/matrix_correlation.png "reference and predicted matrix correlation")
_matrix representation of the predicted and reference time series, correlation between the two matrices_

## Score optimization
Once we have labelled all the cells with a score we can filter the cells whose score is above a certain threshold.
We have in total three scores, each score has a continous version (calculated on reference data) a the discrete version (model prediction).

|variable|quantity|type|values|
|--------|--------|----|------|
|`y_cor`   |correlation |continous  |$[-1,1]$       |
|`b_cor`   |correlation |binned     |${1,2,3,4,5,6}$|
|`y_reg`   |regression  |continous  |$[0,1]$        |
|`b_reg`   |regression  |binned     |${1,2,3,4,5,6}$|
|`y_dif`   |difference  |continous  |$[0,5]$        |
|`b_dif`   |difference  |binned     |${1,2,3,4,5,6}$|

We investigate the cumulative distribution of the scores plotting on the same graph _correlation_ and _difference_

We select all cells and we plot the cumulative distribution
![kpi zone](../f/f_mot/kpi_id_zone_all.png "cumulative distribution of correlation and difference")
_cumulative distribution of correlation and difference_

We then select the best performing filter although we cannot optimize both correlation and difference at the same time.
![kpi cor](../f/f_mot/kpi_id_zone_cor.png "we select only the cells whose correlation is above 0.30")
_we select only the cells whose correlation is above 0.30 (lhs) and those whose binned correlation is above 4 (rhs)_

If we apply direction dinstinction locations become 325 instead of 201 but correlation drops 
![kpi zone](../f/f_mot/kpi_id_clust_all.png "cumulative distribution of correlation and difference")
_cumulative distribution of correlation and difference_

We can still improve the correlation by apply a score selection
![kpi zone](../f/f_mot/kpi_id_clust_cor.png "cumulative distribution of correlation and difference")
_we select only the cells whose correlation is over 0.30 (lhs) and those whose binned correlation is above 4 (rhs)_

## Data enrichment
We enrich location information with geographic information which can give us addtional information on the specificity of the particular location.

![geographic information enrichment](../f/f_mot/data_enrichment.png "Geographic information enrichment for troubleshooting")
_value of the population density on large clusters_
We added information as the population density or the mean flat area per person for investigating the mismatch within predictions, i.e. in denser area filtering has to be more effective.

For each location we can add as information:

* population density
* members in an house hold
* average flat area per person
* share of male/women
* share of young/old people
* share of foreigners
* distance to the motorway
* distance to the junction
* type of streets

## Correction factors
We need to further adjust our results depending on the external parameters, first of all the number of sources available. 
![regression tree](../f/f_mot/regression_tree.png "regression tree location dependent")
_example of a regression tree on prediction results_

We analyzed the influence of some features on the counts mismatch [train_decisionTree.py](http://172.25.186.11:8000/gmarelli/geomadi/blob/master/py/train_decisionTree.py) and spot the most important features for the *predictor*.

## Counts correction
We analyze the variables dependance on counts mismatch and we calculate a correction factor for all locations

![difference dependence](../f/f_mot/difference_dependance.png "dependance of the mismatch on the variables")
_dependance of the mismatch on the variables_

We see indeed that the mismatch between activities and reference data is not independant on:

* `t_type`: type of location (binary encoding)
* `t_sum`: sum of the cell selection
* `t_n_source`: number of reference sources available
* `t_n_cell`: number of selected cells

Where the binary encoding is calculated in the following way:
```python
    stypeL = [str(x).split(", ") for x in list(set(typeV))]
    stypeL = np.unique(list(chain(*stypeL)))
    maskV = []
    for i,p in enumerate(typeV):
        binMask = 0
        for j,t in enumerate(stypeL):
            binMask += 2**(j*bool(re.search(t,str(p))))
        maskV.append(binMask)
    return maskV
```

We choose to use a [bagging regressor on decision tree](http://scikit-learn.org/stable/auto_examples/ensemble/plot_bias_variance.html) to correct the results based on environmental variables.

We can see how the regressor improves the agreement on absolute counts:
![counts corrected](../f/f_mot/kpi_correction.png "counts mismatch after correction")
_counts mismatch after correction for `id_zone`_

## Further corrections
A general issue is that we don't see the same growth as in the reference data:
![chirality distribution](../f/f_mot/chirality_distribution.png "activity and reference")
_activity vs reference_

## Results generation
Applying both predictor and regressor and we generate:
![result no order](../f/f_mot/result_no_order.png "resulting activities per location")
_resulting activities per location_

We then sort the results depending on a $\chi^2$ probability and discard results with an high `p_value`
![result order](../f/f_mot/result_order.png "activities sorted by p-value")
_activities sorted by p-value_

To summarize we generate the results applying the following scheme:
![filter structure](../f/f_mot/filter_structure.png "application of the predictor and regressor")
_application of the predictor and regressor_

The detailed structure of the files and scripts is summarized in this [node-red](http://nodered.org) flow charts:
![flow chart](../f/f_mot/test_flow.png "flow chart of the project")
_flow chart of the project_

## Result visualization
We display overall correlation on a map
![correlation map](../f/f_mot/correlation_map.png "correlation map")
_correlation map_

Isolated spots show good correlation
![good correlation](../f/f_mot/correlation_good.png "good correlation")
_example of good correlation_

Spots close to cities show bad correlation
![bad correlation](../f/f_mot/correlation_bad.png "good correlation")
_example of bad correlation_


Correlation increases when take more locations together
![correlation map spot](../f/f_mot/correlation_map_spot.png "correlation map spot")
_correlation map on a spot_

We can calculate the counts even without reference data
![map counts](../f/f_mot/map_counts.png "counts on a map")
_spatial distribution_

## Capture rate
To calculate the capture rate (number of motorway stoppers over number of drivers on the section in front of the gas station) we route all trips over the motorway network. 

In same cases we find good agreement with customer data, seeing the same asymmetry
![capture rate](../f/f_mot/capture_rate1.png "capture rate of gas station")
_capture rate. Gray:id, blue:section counts, black:predicted activities, red:measured activities, orange:reference data_

We still have to improve the predictions in same cases
![capture rate](../f/f_mot/capture_rate2.png "capture rate of gas station")
_capture rate, high predictions_

We might even see more symmetry than customer
![capture rate](../f/f_mot/capture_rate3.png "capture rate of gas station")
_capture rate, good symmetry_

Section counts show numbers comparable to BAst counts leading to around 1.2 person per car.

## Volume of investigation
_________________
The project considers:

|description|quantity|
|--------|-------:|
|locations  |    937|
|zones      |    191|
|cluster    |    325|
|cells      | 18'190|
|days       |      3|

Resources:

* market share
* [motorway network]()
* [BAst traffic counts](http://www.bast.de/DE/Verkehrstechnik/Fachthemen/v2-verkehrszaehlung/Aktuell/zaehl_aktuell_node.html)
* [Destatis population density]()

Operations:

* cell filtering ```activity_report/run-scripts/start_filter_chains.sh "2017/04/11"```
* trip extractor ```trip_extractor/run-scripts/start_trip_extractor.sh -d 2017/04/11```
* activity report ```activity_report/run-scripts/start_tank_und_rast.sh "2017/04/11"```
* metric aggregator
* direction counts


