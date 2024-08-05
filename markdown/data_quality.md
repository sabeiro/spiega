# data quality

Report on the data quality of the features

## feature extraction

Code: [etl_feature](src/etl_feature.py).

Data are stored in Athena.

![redash_query](../f/f_tele/redash_query.png)
_redash query on telemetry table_

We have 4 relevant tables `['telemetry','network_log','session','incident']` which log all relevant events connected to the drive. Tables are partioned down to the single hour and vehicle.

We have 3 environments `['prod','stg','dev']` where only in `prod` data are complete.

### telemetry

Telemetry contains the most useful information, most of the sensor data concerning vehicle dynamics and board usage. Data are ingested in an unregular way, every sensor calls the backend with different timing. Each 200ms we see a main ingestion of 2 to 5 sensors around 30ms. Information is scattered and uncomplete. 

![telemetry_table](../f/f_tele/telemetry_table.png)
_telemetry table, on record per topic_

We call the `['mean_km_per_hour', 'lateral_force_m_per_sec_squared','longitudinal_force_m_per_sec_squared']` the `sensor_features` and the `['v_cpu_usage_percent', 'v_ram_usage_percent'` the `board features` and the `['e2e_latency', 'camera_latency', 'joystick_latency']` the `predictions`.

## data ingestion

We have different sources populating the `telemetry` table, some coming from the `vehicle`, others from the `control_room`. Data are collected and ingested with a different pace and sent to the backend and follow this a protobuffer schema.

![telemetry_meta](../f/f_tele/telemetry_meta.png)
_telemetry meta information_

Each ROS topic collects the data at a different publishing rate, data are punctual and not averaged on the device. Some data don't get sent or they don't get collected, additional logs are stored on the vehicle but not sent to the backend. 

Each topic has a publisher and a subscriber, the publisher set the timestamp and sends data over the network. 

At first we see that data ingestion pretty irregular.

<!-- ![ingestion_ms](../f/f_tele/ingestion_ms.png "ingestion milliseconds") -->
<!-- _different sources ingest the data with different frequency, phase, amplitude_ -->

We than group the different sources based on their firing behaviour

![ingestion_group](../f/f_tele/ingestion_group.png "ingestion milliseconds")
_grouping sources per frequency range_

We see that even within the same source group we have diffente firing behaviour and syncing the different sources is not trivial. 

We create a heatmap to visualize the firing behaviour

![telemetry_matrix](../f/f_tele/telemetry_matrix.png)
_firing behaviour for telemetry features_

Despite the visualization the features are not ingested regularly and some frequencies are pretty low

![telemetry_frequency](../f/f_tele/telemetry_frequency.png)
_telemetry frequency_

The data is than sent to the backend and arrives at `stream_ingestion_timestamp_ms` and get processed at `processing_timestamp_ms` by kinesis.

## ingestion delay

We see a clear delay between the time the topic publisher sends the data and kinesis process it

![delay_processing](../f/f_tele/delay_processing.png)
_delay in processing the data, around 5 seconds as median_

While the data arriving at the backend has at least 200ms delay till 1s. Streaming data has a curious cycle pattern to be further investigated.

![delay_streaming](../f/f_tele/delay_streaming.png)
_delay in streaming the data_

We finally check that the latency is equal for all cameras

![latency_per_camera](../f/f_tele/latency_per_camera.png)
_all 4 cameras have the same mean latency_

## data stream

Source: [proc_telemetry](src/proc_telemetry)

Data is coming irregularly and values fluctuates artificially because of time buckets. We need to re write the data flow to have consistent data for the predictions.

We take cut the timestamp and calculate the deci seconds to create more consistent time bins

![spark_resample](../f/f_tele/spark_resample.png)
_resampling time bins_

We still have many empty values and we create a rolling window to replace the missing values with the running average 

![spark_runningAv](../f/f_tele/spark_runningAv.png)
_running average over the previous and successive 3 records_

## data extraction

We mainly use **athena** to download the data but we have a strong preference for **spark** since it enables a more careful and complete workflow moving from simple queries to a complete software design

Athena limitations:

* can't handle `null` in averages
* NaN/10. = 0. which is wrong
* can't create libraries
* no user defined functions

We than **avoid all arithmetic operations** in athena to avoid fake zeros.

## network_log data

Query [network_log.sql](queries/network_log.sql)
Code  [stat_network.py](src/stat_network.py)

We analyze the network data to understand which features should be joined with the telemetry table. 

The series have many empty values

![series_network](../f/f_tele/network_series.png)
_time series network features_

Distributions are pretty narrow and have many outliers, not all cameras have the same network figure.

![boxplot_network](../f/f_tele/network_boxplot.png)
_boxplot of network features_

Some features correlate and can be neglected

![correlation_network](../f/f_tele/network_correlation.png)
_correlation across network features_

Some features work in particular regimes and are multimodal

![joyplot_network](../f/f_tele/network_joyplot.png)
_network joyplot_

Modem data are clearly multimodal

![modem_joy](../f/f_tele/modem_joy.png)
_joyplot for modem data_


We join the the `telemetry` table with the `network_log` table to explore additional features but the new sources are even more noisy

![netlog](../f/f_tele/netlog_series.png)
_joined `network_log` and `telemetry` tables_

## modem data 

Source: [etl_telemetry_deci](src/stat_telemetry.py)
Query: [network_log.sql](queries/resample_deci.sql)

We analyze the time series for the modem features

![modem0_pair](../f/f_tele/modem_series.png)
_time series of features_

and correlate the features

![modem0_pair](../f/f_tele/modem_corr.png)
_correlation between modems_

We show that interpolation on deci seconds creates many artefacts

![modem0_pair](../f/f_tele/modem_corr_interp.png)
_correlation between modems_

We display the feature correlation per modem

![modem0_pair](../f/f_tele/modem4_corr.png)
_feature correlation per modem_

We see that upload and download information is redundant

![modem_updown](../f/f_tele/modem_updown.png)
_modem upload and download_

More interesting is the information in the signal features

* RSSI - Received Signal Strength Indicator
* RSRP - the Reference Signal Received Power
* RSRQ - Reference Signal Received Quality 
* SINR - Signal to Interference plus Noise Ratio

we clearly see a correlation between the two D-netz modems (1 and 2) and we keep `sinr` and `rssi` 

![modem_signal](../f/f_tele/modem_signal.png)
_correlation of the modem signal features_

`sinr` and `rssi` are the most rich features

![pair_rsrp](../f/f_tele/pair_rsrp.png)
_pairplot of the rsrp features_

![pair_rsrq](../f/f_tele/pair_rsrq.png)
_pairplot of the rsrp features_

![pair_rsrp](../f/f_tele/pair_r.png)
_pairplot of the rsrp features_

![pair_rsrp](../f/f_tele/pair_rsrp.png)
_pairplot of the rsrp features_

We see that most of the features have to distinguished regimes

![modem_joy](../f/f_tele/modem_joy.png)
_joyplot of modem features_

We see a different persistance depending on the modem we consider

![modem_persistance](../f/f_tele/modem_persistance.png)
_modem feature persistance_


![modem0_pair](../f/f_tele/modem_boxplot.png)
_boxplot of modem features_

![modem0_pair](../f/f_tele/modem0_pair.png)
_pair plot of modem 0_

![modem1_pair](../f/f_tele/modem1_pair.png)
_pair plot of modem 1_

![modem2_pair](../f/f_tele/modem2_pair.png)
_pair plot of modem 2_

![modem3_pair](../f/f_tele/modem3_pair.png)
_pair plot of modem 3_

## camera index

We see that during a spike (`camera_latency` > 300) all cameras have similar latencies

![spike_per_camera](../f/f_tele/spike_per_camera.png)
_correlation of camera latency during a spike_
## session time

We see that some quantities are dependent from the `session_time` which is the time since the starting of the session. 

![session_correlation](../f/f_tele/session_correlation.png)
_correlation between the `session_time` and other features_

`ram` is steadly growing over `session_time` but it's value never gets critical

![session_evolution](../f/f_tele/session_evolution.png)
_evolution of ram over `session_time`_

Session time doesn't seem to influence the number of spikes

![session_spike](../f/f_tele/session_spike.png)
_spikes over `session_time`_


