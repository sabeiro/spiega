# lagged metrics

In this project we want to investigate main differences between the metrics on the call and lagged metrics


## difference

The lagged metrics considers a time span of 25 days when the customer could call again and turn around. The lagged metric loses around 10% customers

![lagged_series](../f/f_intertino/lagged_series.png)
_time series of on-call and lagged metrics_

We have different metrics to predict

![lagged_metric](../f/f_intertino/lagged_metric.png)
_metrics to predict, on call and lagged_

We clean the features

![lagged_boxplot](../f/f_intertino/lagged_boxplot.png)
_normalized feature distribution_

We check the feature independency

![lagged_corr](../f/f_intertino/lagged_corr.png)
_correlation between features_

Effect of afiniti agent on feature distribution

![lagged_overlay_on](../f/f_intertino/lagged_overlay_on.png)
_overlay of feature distribution_

Overlay distribution of features on saved customers 

![lagged_overlay](../f/f_intertino/lagged_overlay_saved.png)
_overlay of feature distribution_

Overlay distribution of featured of saved/lost customers

![lagged_corr](../f/f_intertino/lagged_joyplot.png)
_Overlay distribution of features: joyplot_

We build a predictive model for the on-call metric

![lagged_confMatrix](../f/f_intertino/lagged_confMatrix.png)
_confusion matrix on prediction: on-call_

We use the prediction of the previous model to predict the new metric

![lagged_confMat](../f/f_intertino/lagged_confMat.png)
_confusion matrix on prediction: lagged_

We knock-out features to calculate the relative importance of that feature

![lagged_knockCall](../f/f_intertino/lagged_knockCall.png)
_knock-out of features from trained model: on-call_

![lagged_knockLagged](../f/f_intertino/lagged_knockLagged.png)
_knock-out of features from trained model: lagged_

We finally check the relative difference between on-call and lagged

![lagged_featDiff](../f/f_intertino/lagged_featDiff.png)
_relative difference between feature importance in lagged metrics_

We can study the relative feature importance 

![lagged_featImp](../f/f_intertino/lagged_featImp.png)
_feature importance (week overlay)_

and see how it evolves week by week

![lagged_weekImp](../f/f_intertino/lagged_weekImp.png)
_relative importance week by week_

We study over week how the relative importance of that metric dropw over time

![lagged_featImp](../f/f_intertino/lagged_impDiff.png)
_importance difference relative to lagged metrics_

We calculate the lift depending on categorical metrics

$$ lift = SR_{on} - SR_{off}$$

![lagged_featImp](../f/f_intertino/lagged_lift.png)
_lift relative to categorical metrics_

# cohort reshuffling

We look month per month how the association of agents per area varies over time

![cohort_timeSer](../f/f_intertino/cohort_timeSer.png)
_time series volume changes in cohorts_

Shuffling among cohorts

![lagged_sankey](../f/f_intertino/lagged_sankey.png)
_reshuffling of agents cohorts_


