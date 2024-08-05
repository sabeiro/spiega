# feature temporal ordering

We want to establish which features preceed the spike and are hence relevant for forecast

## inter feature persistance

We want to check which features are phased together. At first we calculate a correlation on a rolling window of a short period of 16 seconds

![correlation_rolling](../f/f_tele/correlation_rolling.png)
_correlation on a rolling window_

Than we iterate over all features to understand which is the most temporarly correlating, we clearly see that most of the feature don't have a window correlation while vehicle ping does

![sync_violin](../f/f_tele/sync_violin.png)
_violin plot of correlation distribution_

Apart from the trivial correlations we see that the networking features are the ones most correlating

![sync_correlation](../f/f_tele/sync_correlation.png)
_window correlation of features_

If we look at the cross correlation with time delay we see again that `vehicle_ping` has the most persistent temporal correlation with `latency`. We realize that the upsampling creates artificial fluctuations every neighbouring second

![sync_xcor](../f/f_tele/sync_xcor.pong)
_cross correlation with delay_

From the cross correlation we can compute the decay time

![sync_decay](../f/f_tele/sync_decay.png)
_exponential regression on the decay_

We calculate for each feature a decay time

![sync_decay](../f/f_tele/sync_decayExp.png)
_regression on decays_

and calculate the persistance as the sum of the decay curve over the decay interval

![sync_persistance](../f/f_tele/sync_persistance.png)
_persistance among features_

We than iterate over all features and calculate the cross and auto persistance. Large values singalize a bad sampling (artificial similarity) 

![sync_persistanceM](../f/f_tele/sync_persistanceM.png)
_matrix of persistance among features_

We can calculate the persistance for other data sets

![modem_persistance](../f/f_tele/modem_persistance.png)
_persistance for modem features_

We now calculate the peak at the maximum cross correlation delay, smoothing is necessary to remove artefacts

![sync_peak](../f/f_tele/sync_peak.png)
_peak at the maximum cross correlation delay_

Not all phase calculations lead to reasonable results, we see that many phase lag estimations are inconclusive, either null or fluctuating a lot. We are pretty cofindent that over the hundrets of spike events in general few features can anticipate the spike

![sync_previous](../f/f_tele/sync_previous.png)
_features with a negative time delay compared to camera latency_

Data are pretty noisy and we want to establish temporal sorting for at least the average of all the spike events

![phase_lag](../f/f_tele/phase_lag.png)
_phase lag between features_

We can roughly say that rtp and joystick features happen before the camera spike

## phasing

We want to calculate the average delay between features using the cross correlation of two features. In some cases on feature is clearly reacting to the spike

![delay_ram](../f/f_tele/delay_ram.png)
_delay between camera latency and rtp_lost_

In some cases the analysis is inconclusive

![delay_ram](../f/f_tele/delay_jitter.png)
_delay between camera latency and camera_jitter_

Some features anticipate the spike but there is still some lower modus where they happen later

![delay_ram](../f/f_tele/delay_joystick.png)
_delay between camera latency and joystick_

In other cases the features are completely connected

![delay_ram](../f/f_tele/delay_rtt.png)
_delay between camera latency and modem_rtt_

Different methods lead to similar results

![delay_compare](../f/f_tele/delay_compare.png)
_compare delay methods_

For some series (deci seconds on `bytes-Cellular 3`) the different methods disagree on phases

![delay_compare](../f/f_tele/delay_deciCell.png)
_compare delay methods_

If we smooth the time series we see a clear trend

![modem_smooth](../f/f_tele/modem_smooth.png)
_smoothing the time series_

and althought the phase calculation should be more clear methods differ in results

![modem_phase](../f/f_tele/modem_phase.png)
_estimation of phase for smoothed features_

We than calculate the phase difference using cross correlation and looking at the camera latency we conferm the euristic impression that `josystick_latency` and `vehicle_cpu` happen before the spike and `room_ram`, `vehicle_ram`, `force_lon`, `brake_pressure` after. `modem_tx` is slghtly before the spike.

![delay_fourier](../f/f_tele/delay_fourier.png)
_delay between features using cross correlation phase difference_

On the deci second scale the modem features are clearly preceeding the spike. Arrival time is really noisy and shouldn't be considered. Bytes are clearly preceeding the spike

![delay_fourier](../f/f_tele/delay_fourierDeci.png)
_delay between features using cross correlation phase difference_

We want to calculate now the phasing for each time series

![series_dot](../f/f_tele/series_dot.png)
_each series has slightly different data points_

What works for the denoised time series doesn't work for the sum of the single series where the determination of the phase difference is pretty chaotic

![spike_offset](../f/f_tele/delay_violin.png)
_phase difference between camera latency and other features_

The same for the deci second dataset

![spike_offset](../f/f_tele/spike_offset.png)
_phase difference between camera latency and other features_

Time lag between modem features and `camera_latency`

![modem_lag](../f/f_tele/modem_lag.png)
_time lag for modem features_

We clearly see in average when which features preceed the latency and which follow, basically the round trip time is slower than the latency calculation while the signal is more advanced

![modem_lagM](../f/f_tele/modem_lagM.png)
_time lag for modem features_

