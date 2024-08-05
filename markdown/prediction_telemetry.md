# prediction

Definition and training of the models, feature importance and feature selection.

## latency prediction

We want to distinguish the camera latency into different danger classes and be able to predict them depending on the other parameters.

If we use 2 or 5 classes the results are different

![pred_2class](../f/f_tele/pred_2class.png)
_prediction on two classes_

Perfomances decrese when we want to increase the number of classes

![pred_5class](../f/f_tele/pred_5class.png)
_prediction on two classes_

If we consider only the incident set we see that training is more difficult

![roc_incident](../f/f_tele/roc_incident.png)
_prediction of spikes on incident time series_

The confusion matrix shows really few counts outside of the diagonal

![confusion_matrix](../f/f_tele/confusion_matrix.png)
_confusion matrix of the spike prediction_

### feature importance

Iterating over different models we see different performances and feature importance. Despite differences we see that most of the model consider modem issues as the most relevant for spike prediction

![feature_importance](../f/f_tele/feature_importance.png)
_feature importance according to different models_

Running a simple regression results are pretty clear

![feature_regression](../f/f_tele/feature_regression.png)
_feature regression_

## spike prediction

Code: [train_spike](src/train_spike.py).

We want to understand which are the most important predictors for camera latency.

We create the most simple regressor as **baseline model** to set the reference performance to test other models

```python
model = Sequential()
model.add(Dense(layer[0],input_shape=(n_feat,),kernel_initializer='normal',activation='relu'))
model.add(Dense(1, kernel_initializer='normal'))
model.compile(loss='mean_squared_error', optimizer='adam')
```

We train the model on the complete dataset and than iterate for each single series

![baseline_performance](../f/f_tele/baseline_performance.png)
_performance of the baseline model_

We see that in the baseline model only a peak is predicted.

![baseline_performance](../f/f_tele/3layer_performance.png)
_Performance of a three layers network on incident data_

With a deeper network few peaks more are detected.

## risk prediction

Code: [feature_etl](src/forecast_spike.py).

We want to calculate the spike risk predicting the `time_to_spike` from the other features and calculate the risk of an upcoming spike. We first train on the denoised average

![prediction_deviation](../f/f_tele/prediction_deviation.png)
_prediction deviation_

We than apply a Cox-Breslow survival estimator to calculate the cumulative dynamic AUC

![cox-breslow](../f/f_tele/cox_breslow.png)
_AUC on Cow Breslow_

We perform than cross validation traning the model on a series and predicting on another one, we see that the cross validation tends towards the average prediction

![risk_prediction](../f/f_tele/risk_prediction.png)
_risk prediction on cross validation_

# spike prediction

We first perform a lmts on the `camera_latency` itself. We perform 20 epochs on the average and than 2 epochs on each single series

![forecast_predict](../f/f_tele/spike_forecast.png)
_different example series on spike forecast_

We see that the learning is pretty unregular

![forecast_learn](../f/f_tele/forecast_learn.png)

We than check how many spkies we can forecast

![forecast_confusion](../f/f_tele/confusion_forecast.png)
_confusion matrix on forecasted spikes_

We finally perform a forecast only with networking features

![forecast_predict](../f/f_tele/networking_forecast.png)
_forecast with networking features_

and calculate the final confusion matrix

![forecast_confusion](../f/f_tele/confusion_matrix.png)
_confusion matrix on forecasted spikes with networking features_

