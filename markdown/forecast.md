# spike forecast

Code: [forecast_spike](src/forecast_spike.py).

To forecast a spike we start first with a good prediction

![prediction forecast](../f/f_tele/prediction_forecast.png)
_difference between prediction and forecast_

We see that the training process runs smoothly
![prediction_history](../f/f_tele/prediction_history.png)
_traning history_

## traning recipe

To train the model we proceed in the following way:

* We flatten all peaks at 300ms
* We normalize the features between -1 and 1 excluding the 5 and 95 percentile interpolating the outliers
* We train 10 epochs on the complete data set
* We train 20 times 20 epochs on denoised series using rolling windows between train and test splits
* We train 500 times 20 epochs on single series on rolling windows between train and test splits
* We train 500 times 20 epochs on single series on cross validating series
* We train 20 times 20 epochs on denoised series using rolling windows between train and test splits


### denoised

Than we roll different spike advance times until the spike is forecasted

![forecast_advance](../f/f_tele/forecast_advance.png)
_forecast advance effectivity_

We can see that around -0.5 seconds the spike is forecasted correctly

![forecast_prior](../f/f_tele/forecast_prior.png)
_forecast prior to the spike_

To speed up a bit the exploration we analyze the sec pace series. We see that the forecast for the denoised series is pretty accurate 

![forecast_anticipation](../f/f_tele/forecast_anticipation.png)
_rolling forecast on the next 6 seconds_

In some cases forecast results are different for neighboring starting points

![forecast_anticipation](../f/f_tele/forecast_anticipation1.png)
_rolling forecast on the next 6 seconds_

Some models are really accurate on the denoised series

![forecast_anticipation](../f/f_tele/forecast_aligned.png)
_rolling forecast on the next 6 seconds_

We see that in some cases we have false positive

![false_positive](../f/f_tele/false_positive.png)
_false positive, a spike is forecasted where there is none_

If we analyze the maximum of the peak forecast we see that some models can forecast 3 seconds in advance

![forecast_max](../f/f_tele/forecast_max.png)
_maximum forecast on a rolling windows of 12 seconds_

Using modem features we can have an earlier estimation

![modem_foreAv](../f/f_tele/modem_foreAv.png)
_latency maximum forecast on a 6 seconds, modem features_

### single series

We iterate over every single series and forecast from every single `from_peak` value and compute the maximum of the forecasted latency

![forecast_series](../f/f_tele/forecast_series.png)
_maximum latency forecast per series, deci seconds_

We than calculate the forecast curves per series and per starting point and calculate the maximum for each curve. For some models the forecast returns many false positives

![forecast_flat](../f/f_tele/forecast_flat.png)
_maximum forecast on a rolling windows of 6 seconds_

Using modem features we can forecast earlier on average

![modem_foreMax](../f/f_tele/modem_foreMax.png)
_latency maximum forecast on modem features, single series_

We than calculate the maximum latency per series per `time_to_peak`, we identify a peak setting a threshold

![modem_truePos](../f/f_tele/modem_truePos.png)
_true positive rate, modem features_

We show the tradeoff using different type of thresholds

![modem_threshold](../f/f_tele/modem_threshold.png)
_true positive rate, dependence on threshold_

### derivative

Now we take the derivative of the signal

![diff_series](../f/f_tele/diff_series.png)
_derivative of camera latency_

And we train a model on the with all features derived

![diff_truePos](../f/f_tele/diff_truePos.png)
_latency forecast on single series and starting point_

We than calculate the accuracy depending on the threshold

![diff_truePos](../f/f_tele/diff_accuracy.png)
_accuracy of forecast depending on the threshold_

We see that substantiall changing the size of the window doesn't change much the results

![diff_ahead](../f/f_tele/diff_ahead.png)
_forecast on different rolling windows_

### double history

We now use a double history points to forecast the next point

![diff_double](../f/f_tele/diff_double.png)
_forecast on double history_

Forecast on single series and rolling windos

![double_foreSeries](../f/f_tele/double_foreSeries.png)
_double forecast series_

Accuracy on single series forecast

![double_accuracy](../f/f_tele/double_accuracy.png)
_double forecast accuracy_

# feature knockout

Feature importance by substituing the feature by random values

![diff_knock_out](../f/f_tele/diff_knock_out.png)
_difference knock out_

# forecast validation

For the validation we take calendar week 39 and we perform a pre trained model. We check that the model deliver reliable forecasts on a time window of 6 seconds

![rolling_forecast](../f/f_tele/rolling_forecast.png)
_forecast on a rolling window of 6 seconds on a denoised series_

were we used the simple non derivative single step model for sake of speed.
We take the maximum of each forecast and build the forecast line

![validation_performance](../f/f_tele/validation_forecast.png)
_maximum forecast on the rolling window_

We than perform a forecast for each second of the week and compare its maximum with the signal maximum on a rolling window of 1, 6, 12 and 30 seconds

![validation_series](../f/f_tele/validation_series.png)
_time series of camera latency considering the maximum of the next `n` steps_

We than set a threshold and we count how many data points are above this threshod (spike) in a time bin of 4 seconds

![confusion_3sec](../f/f_tele/confusion_4sec.png)
_confusion matrix about the presence of spikes in the next 4 seconds_

and compute the same for the next 30 seconds

![confusion_30sec](../f/f_tele/confusion_30sec.png)
_confusion matrix about the presence of spikes in the next 30 seconds_

We see that the false negative rate is around 0.5% and that the model is pretty conservative since there are no false positive. That means that around 10% of the spikes are still undiscovered. 

# forecast alternatives

We started performing some naive forecasting on the time series and we compare the results of facebook prophet, a multi layer perceptron regressor and a arima. The first two models take into consideration the sensor features too. 

We see that the peaks are really abrupt and the naive models can't forecast it.

![first_peak](../f/f_tele/first_peak.png "first peak")
_first peak_

