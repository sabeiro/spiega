---
title: "traffic on motorways"
author: Giovanni Marelli
date: 2019-05-20
rights:  Creative Commons Non-Commercial Share Alike 3.0
language: en-US
output: 
	md_document:
		variant: markdown_strict+backtick_code_blocks+autolink_bare_uris+markdown_github
---

# traffic on motorways

## counting locations

Across germany there are thousands of counting locations on the main roads and the count of vehicle crossing the section of the street is [public](https://www.bast.de/BASt_2017/DE/Verkehrstechnik/Fachthemen/v2-verkehrszaehlung/Stundenwerte.html?nn=1817946)

![bast_germany](../f/f_via/bast_germany.png "BaSt Germany")
_BaSt Germany for motorways and primary streets_

For each of those location we select a pair of openstreetmap nodes (arrows) for the same street class.

![via_tile_selection](../f/f_via/via_tile_selection.png "via tile selection")
_For the same BaSt location the tile intersects more streets_

To stabilize over year we build an isocalendar which represents each date as week number and weekday. We see that isocalendar is pretty much stable over the year with exception of easter time (which shifts a lot).

![isocal_deviation](../f/f_via/isocal_deviation.png "isocalendar deviation")
_standard deviation on same isocalendar day over the year_

## data set preparation

We take hourly values of BaSt counts and we split in weeks.
Every week is represented as an image of 7x24 pixels. 

![time_series](../f/f_via/timeSeries_img.png "time series")
_image representation of time series_

The idea is to profit from the performances of convolutional neural networks to train an autoencoder and learn from the periodicity of each counting location.

Convolutional neural network usually work with larger image sizes and they suffer from boundary conditions that creates a lot of artifacts.

That's why we introduce backfold as the operation of adding a strip to the border from the opposite edge.

![backfold](../f/f_via/backfold.png "backfolding")
_backfolding the image_

In this way we obtain a new set of images (9x26 pixels)

![time_series](../f/f_via/timeSeries_backfold.png "time series")
_image representation of time series with backfold_

And produce a set of images for the autoencoder

![dataset](../f/f_via/img_dataset.png "img dataset")
_image dataset_

## model definition

We first define a short convolutional neural network

![3d](../f/f_via/shortConv_3d.png "short conv net")
_short convNet in 3d_

We than define a slightly more complex network

![3d](../f/f_via/convNet_3d.png "conv net")
_definition of a conv net in 3d_

In case of 7x24 pixel matrices we adjust the padding to achieve the same dimensions.

## training

We fit the model and check the training history.

![history](../f/f_via/history.png "training history")
_training history_

Around 300 epochs the model is pretty stavle and we can see the morphing of the original pictures into the predicted

![morphNo](../f/f_via/morph_noBackfold.png "morph no backfold")
_raw image morphed into decoded one, no backfold_

If we introduce backfold we have a slightly more accurate predictions

![morph](../f/f_via/morph_shortConv.png "morph short convolution")
_raw image morphed into decoded one, with backfold_

The most complex solution comes with the deeper model

![morphConv](../f/f_via/morph_conv.png "morph conv")
_morphing for convNet_

## results

At first we look at the results of the non backfolded time series

![shortConv](../f/f_via/shortConv_noBackfold.png "short convolution")
_results for the short convolution, no backfold_

If we add backfold we improve correlation and relative error

![shortConv](../f/f_via/shortConv_week.png "short convolution")
_results for the short convolution_

The deepest network improves significantly the relative error but as a trade off loose in correlation

![convNet](../f/f_via/convNet_backfold.png "convNet wbackfold")
_convNet results with backfold_

## scores

The deepest network improves drastically the relative error sacrifying the correlation

![boxplot_corErr](../f/f_via/boxplot_corErr.png "boxplot")
_boxplot correlation and error difference between models_

Correlation not being in the loss function is really disperse while optimizing

![confInt](../f/f_via/confInt_score.png "confidence interval scoring")
_confidence interval for correlation and relative error_

Ranking is not stable among the different methods

![sankey](../f/f_via/sankey_backfold.png "sankey diagram")
_Sankey diagram of correlation shift between different methods_

Different methods behave differently wrt the particular location

![sankey](../f/f_via/sankey_error.png "sankey diagram")
_sankey diagram of error reshuffling_

The deepest network tend to amplify the bad performances in correlation

![parallel](../f/f_via/parallel_correlation.png "parallel correlation")
_parallel diagram of correlation differences_

The short backfolded model has the worse performances for locations that had the best performances in the non backfolded version

![parallel](../f/f_via/parallel_error.png "parallel error")
_parallel diagram of relative error_

## dictionary learning

We perform a *dictionary learning* for knowing the minimal set average of time series to describe with good accuracy any location. For that we will use a KMeans

```python3
clusterer = KMeans(copy_x=True,init='k-means++',max_iter=600,n_clusters=4,n_init=10,n_jobs=1,precompute_distances='auto',random_state=None,tol=0.0001,verbose=2)
yL = np.reshape(YL,(len(YL),YL.shape[1]*YL.shape[2]))
mod = clusterer.fit(yL)
centroids = clusterer.cluster_centers_
```

We start with the most common time series and we calulate the score of all locations on that cluster

![cluster](../f/f_via/cluster_1.png "1 cluster")
_most frequent cluster_

We realize the 90% of the locations and weeks have a correlation higher than 0.9

![cluster_histogram](../f/f_via/cluster_kpiDis.png "cluster kpi distribution")
_kpi distribution for single cluster_

A single cluster is already a good description for any other location but we want to gain more insight about the system.
We than move the 2 clusters to classify the most important distintion between locations which we will call "touristic" and "commuter" street classes.

![cluster](../f/f_via/cluster_2.png "2 cluster")
_most 2 frequent clusters, touristic and commuter_

We can extend the number of cluster but we don't significantly improve performances but land to same extreme cases

![cluster](../f/f_via/cluster_24.png "24 cluster")
_most 24 frequent clusters_

If we look at the KPIs distribution 4 clusters are the best trade-off between precision and computation

![cluster_histogram](../f/f_via/cluster_histogram.png "cluster cumulative")
_histogram for correlation and relative error_

If we look at the most 4 frequent clusters we see that they are split in 2 touristic and 2 commuters

![cluster](../f/f_via/cluster_4.png "4 cluster")
_most 4 frequent clusters_

We want than to see how often a single location can swap between commuter and touristic and we see that locations are strongly polarized though all the year

![cluster_polarization](../f/f_via/cluster_polarization.png "cluster polarization")
_cluster polarization_

If we look at the weekly distribution we see that the commuting pattern ressamble our expectation

![commuting_pattern](../f/f_via/commuting_pattern.png "commuting pattern")
_commuting pattern strength through all locations_

To compute a common year we build an isocalendar which is the representation of a year into 

## tuning

We worked to tune the network to avoid the system to fall in a local minimum

![mimimum](../f/f_via/local_minimum.png "local minimum")
_training is trapped in a local minimum_

This local minimum will turn to be the most common cluster which indeed has a good score with all other time series

![boundary_problems](../f/f_via/boundary_problem.png "boundary problems")
_problems caused by boundary conditions_

We work on the dimension of convoluting filters to obtain indentation (the flat daily profile is not strongly penalized).

![series_firstIndent](../f/f_via/series_firstIndent.png "series first indent")
_indentation starts to appear_

## interpolation

What happens if we upscale the image to have a larger dimension of images and we define a more complex network.

![image_interp](../f/f_via/image_interp.png "image interpolation")
_upscaling a time series_

Running time is drammatically increased but the convergence is not better. 

![series_upscaling](../f/f_via/series_upscaling.png "series upscaling")
_results of the upscaled time series_

The upsampling is not adding any useful information that the convolution wouldn't 
We downscale the image and the result suffer from the same 

![series_downscaling](../f/f_via/series_downscaling.png "series upscaling")
_results of the upscaled time series_

## flat convolution

In this case we remove the padding, cropping and up-sampling.
We can see that in early stages the boundary has a big effect in prediction.

![flat_morph](../f/f_via/flat_morph.png "flat morph")
_morphing for flat convolution, earlier steps_

We can see that the prediction is really close to the reference series

![flat_series](../f/f_via/flat_prediction.png "flat series")
_prediction for flat convolution_

We realized as well that the model is drammatically overfitted.

![flat_overfitted](../f/f_via/flat_overfitted.png "flat overfitted")
_overfitted model_

## short convolution

We reduce the number of parameters to try to capture the most essential feature of a weekly time series downscaling the image with a 3x3 pooling. 

We see the modification of the external data into the model trained for the motorway counts.

![short_prediction](../f/f_via/short_prediction.png "short prediction")
_prediction using a short autoencoder_

Some times even the short convNet look like overfitting

![short_overfitted](../f/f_via/short_overfitted.png "short overfitted")
_The prediction in limiting cases look overfitting_

## Performances 

In case of a picture we would have 7x24x256 = 43k values to predict, if we downscale from 8 to 6 bits we still have 10k parameters to predict. 
The dataset has a lot of redundancy and we should size the model to not consider too many parameters to avoid overfitting. 

|method|params|score auto|score ext|
|------|------|-------|-------------|
|max       | 43k |    |    |
|interp    | 12k |    |    |
|convFlat  | 2k4 |    |    |
|shortConv | 1k3 |    |    |

## via nodes

To select the appropriate via nodes we run a mongo query to download all the nodes close to reference point. We calulate the orientation and the chirality of the nodes and we sort the nodes by street class importance. For each reference point we associate two via nodes with opposite chirality.

We can see that the determination of the via nodes is much more precise that the tile selection.

![via_algo](../f/f_via/via_algo.png "identification of via nodes")
_identification of via nodes, two opposite chiralities per reference point_

The difference is particular relevant at junctions

![junction](../f/f_via/junction.png "via nodes on junction")
_via nodes on junctions, via nodes do not count traffic from ramps_

## morph external data

Once we have found the best performing model we can morph our input data into the reference data we need.
We have two sources of data which similarly deviate from the reference data.

![join_plot](../f/f_via/join_plot.png "distribution of via and tile counts")
_distribution of via and tile counts compared to BaSt_

We first take the flat model and we see some good 

![flat_ext](../f/f_via/flat_ext.png "flat ext")
_prediction from external data_

The model is good for denoising spikes in the source

![flat_denoise](../f/f_via/flat_ext_denoise.png "flat denoise")
_denoising functionality of the model_



We don't see a strong improvement in performances due to the overfitting of the flat autoencoder.

![flat_boxplot](../f/f_via/flat_boxplot.png "flat boxplot")
_drop in performances applying the autoencoder on external data_

![short_boxplot](../f/f_via/short_boxplot.png "short boxplot")
_we have good performances with the short autoencoder that avoids overfitting_

## encoder

If we need to write a source dependent model we use the same network to predict from internal data the reference data. 

The encoder helps to adjust the levels especially for daily values

![encoder_series](../f/f_via/encoder_series.png "encoder series")
_prediction with the encoder_

The encoder helps as well to reproduce the friday effect

![encoder_friday](../f/f_via/encoder_friday.png "encoder friday")
_prediction has a better friday effect_

![encoder_boxplot](../f/f_via/encoder_boxplot.png "encoder boxplot")
_the encoder increases performances but the original data already score good performances_
