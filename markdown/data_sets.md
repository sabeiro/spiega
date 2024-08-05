# data sets

Definition and prepartation of the data sets

## deci seconds

Source: [etl_telemetry_deci](src/etl_telemetry_deci.py)
Query: [network_log.sql](queries/network_log.sql)

To analyze the deci second data we can use fewer features (because of sampling rate) like the `computing` features and `vehicle_ping`. Event `rtp` and `modem` features have to be removed. We collect other `networking` features from the `network_log` table where we subset the telemetry data into a series of spikes and we merge the network data information using the `timestamp` and the `vehicle_id`. We pivot the `network_log` table wrt to the modem name.
We also discard `ttl` and `interval_duration` for the low information contained.
We discard `packets` because the hava a correlation of 0.98 with `bytes`.

![network_log_series](../f/f_tele/network_log_series.png)
_time series of the most relevant features_

We see that the quantity of transmitted information slightly correlates between modems signalizing similar networking issues across operators. The correlation between bytes and arrival time is lower than expected

![network_log_corr](../f/f_tele/network_log_corr.png)
_correlation between the network log features_

But in general modems have a different behaviors, cellular 3 is the most stable and transmits more data.

![network_log_joyplot](../f/f_tele/network_log_joyplot.png)
_joyplot of network_log features_


## datasets

We prepare different datasets for different parts of the analysis:

* **latency set** complete august and september data: [etl_telemetry](src/etl_telemetry.py)
  * location
  * networking
  * vehicle dynamics
  * computing
* **spike set** subset of latency set referring to spike events [etl_spike](src/etl_spike.py)
  * location
  * networking
  * vehicle dynamics
  * computing
  
The different sets have a different sampling of events, the `latency set` has few spike events while the `spike set` has all the perturbations before and after a disruption event. 

From the two dataset we can see the different feature distribution and feature importance.

## spike preprocessing

Query: [resample_1sec](queries/resample_1sec.sql)
Code: [etl_spikes](src/etl_spikes.py)

We resample **averaging 1 sec worth of data** but some fields are still uncomplete, around 1% of the timse

![feature_missing](../f/f_tele/feature_missing.png)
_percentage of missing data in certain features_

We identify the peak and split each time series in sub series where all peaks are aligned at the minute 4 and we leave one minute after the spike. 

We artificially exagerate the peak to help the model understand it and set the peak max value to a plateau

![spike_events](../f/f_tele/spike_events2.png)
_series of spikes_

We than abstract the time and create a stack of series where the peak in phase

![spike_stack](../f/f_tele/spike_stack.png)
_stack of spikes where the spike happens at minute 4_

## spike inspection

It is interesting to analyze some spike series to understand qualitatively what might happen during incidents. In this case we see two concurrent spikes in two different sessions

![spike_simultaneous](../f/f_tele/spike_simultaneous.png)
_two spikes at the same time on different cars (*24, *76)_

Averaging the two series it seems that the `room_cpu` has a clear variation prior to the spike. 

![series_simultaneous](../f/f_tele/series_simultaneous.png)
_average of both time series prior to the spike_

We see 3 of such pairs: 2020-08-17T11, 2020-08-24T18, 2020-08-20T08.

## feature selection

At first we discard poor features analyzing:

* low variance
* low frequency
* noise level

Spikes are rare events and some features might be as rare as spikes and than a indication of them but in case of `['td_brake','td_throttle','steering_interval']` we see that data are rare don't happen in high latency cases.

![poor_feature](../f/f_tele/poor_feature.png)
_poor features_

In comparison we see that `rtp_lost` and `rtp_late` have a clear distribution dinstinction although most of the time data are NaNs

![rich_feature](../f/f_tele/rtp_pairplot.png)
_poor features but discriminators for latency_

## feature statistics

Code: [stat_telemetry](src/stat_telemetry.py), [stat_latency](src/stat_latency).

Of the most important feature we visualize the time series

![series_log](../f/f_tele/latency_series.png "time series")
_visualization of the time series_

We collect a day of data and subset the time series prior to a spike

![time_series](../f/f_tele/spike_series.png "time series")
_time series of the most relevant features prior to a spike, we can see that after the disruption the vehicle brakes_

We removed some features because of the obvious cross correlation (ex: `brake_pressure` ~ `wheel_speed`)

![computing_correlation](../f/f_tele/dynamics_correlation.png "feature correlation")
_feature correlation, obvious cross correlation_

We see a dependency between `vehicle` and `control_room` `cpu` and `ram` usage

![vehicle_room](../f/f_tele/computing_correlation.png)
_vehicle and control room interdependency on computation_

We see that not all the features are distributed regularly and some are pretty noisy. 

![feat_boxplot](../f/f_tele/latency_boxplot.png "feature boxplot")
_distribution of the latency features: boxplots_

In case of the spike subset the distribution get a bit broader

![feat_boxplot](../f/f_tele/spike_boxplot.png "feature boxplot")
_distribution of the spike features: boxplots_

We than calculate the logaritmic of the most dispersed features (e.g. `_force_`) to gain more meaningful information. Changing the latencies to their logaritmic value doesn't change much the distributions

![feat_boxplot](../f/f_tele/feat_boxplot.png "feature boxplot")
_logaritmic transformation for some features_

We see that some quantities are bimodal, interestingly latencies too. It seems there are clear distinguished operating regimes.

![feat_joyplot](../f/f_tele/latency_joyplot.png "feature joyplot")
_distribution of the latency features: joyplots_

Another feature selection takes more into account the networking features, the different time frames change a lot the data distribution. In this case we consider only events in the proximity of a spike and the features become even more bimodal

![feat_joyplot](../f/f_tele/spike_joyplot.png "feature joyplot")
_distribution of the spike features: joyplots_

Looking at the pair plot we see that only `ram_usage` has an interesting dependency on the `camera_latency`, the **purple set is the one corresponding to the larger bin of the `camera_latency`

We analyze the how the networing features distributes in different regimes of camera latency

![feat_pairplot](../f/f_tele/networking_pairplot.png)
_pairplot of the networking features_

Same for the computing features

![feat_pairplot](../f/f_tele/computing_pairplot.png)
_pairplot of the computing features_

Pairplot for vehicle dynamics features don't show a clear dependency on latency

![feat_pairplot](../f/f_tele/feat_pairplot.png)
_pairplot of the vehicle dynamics features_

## latency statistical properties

We want to understand the periodicity and auto correlation of `camera_latency` to understand how to separate different regimes 

![latency_decay](../f/f_tele/latency_decay.png)
_latency decays and frequency behaviour_

We analyze the power spectrum for a normal latency or during a spike

![latency_spectrum](../f/f_tele/latency_spectrum.png)
_latency power spectrum for normal and spike regimes_

During the spike event autocorrelation is a bit larger and more stable than in the normal regime

![latency_autocor](../f/f_tele/latency_autocor.png)
_Autocorrelation for camera latency in normal and spike regimes_


## feature normalization

For a fast and reliable training a good normalization is essential for the performances of the predictions. We need to find a stable normalization to keep across all predictions. If we need to change the normalization than we need to retrain the model.

![flatten_outlier](../f/f_tele/flatten_outlier.png)
_flattening of outlier to let the normalization to operate in a consitently populated regime_

## denoise

To have a clear understanding on what is happening we stack many time series where the spike happens at the 0 second. We take 160+ time series and we calculate the average to denoise and have a more statistical understanding on the process

![series_avExp](../f/f_tele/seriesAv_exp.png)
_average on spike events where the spike happens at second 0_

If we have a clear look at the moment where the spike happens we clearly see that some features show a change previous to the spike and others consequent to the spike

![series_spike](../f/f_tele/series_spikeDetailExp.png)
_detail on the few seconds around the spike event_

Similarly we look at the signal differences

![series_spike](../f/f_tele/series_spikeDiffExp.png)
_series evolution of the feature differences_

and the close up

![series_spike](../f/f_tele/series_spikeDetailDiffExp.png)
_series evolution of the feature differences_

We analyze the variance depending on the time to the spike

![series_latencyVar](../f/f_tele/series_latencyVar.png)
_variance of camera latency_

Another important indicator of causal dependency is the dropping of **variance** before a spike which tell us that `ram` is clearly affected by spikes

![series_variance](../f/f_tele/series_variance.png)
_variance of time series_

For some features the variance is so high that we would consider the averages just random fluctuations

![series_binned](../f/f_tele/series_binned.png)
_variance and mean for time series_

We analyze the time series for the features with an higher firing rate, we see that in average the byte volume drops across all modems

![series_deci](../f/f_tele/series_deci.png)
_time series on deci seconds_

If we look at the few seconds close to the spike we don't see clear signs of incoming spikes 

![series_deci](../f/f_tele/series_deciDetail.png)
_time series on deci seconds, detail_

Neither looking at the derivative we see a clear trigger

![series_deci](../f/f_tele/series_deciDiff.png)
_time series on deci seconds, derivative_

We than smooth the series to have a better picture and start recognizing some patterns

![series_deci](../f/f_tele/series_deciSmooth.png)
_time series derivative on deci seconds, smoothed_

