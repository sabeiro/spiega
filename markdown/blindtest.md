# blind test
Our function can be expressed as:

$$ x_{act}(t) m_{share}(t_{d}) = y_{ref}(t) ../f/f_{people}(t) + y_{out}(t) $$

_where $x_{act}$ is the number of activities, $m_{share}$ is the market share, $y_{ref}$ reference data - cachier receipts, $../f/f_{people}$ people per receipt, $y_{out}$ people outside the shop, $t$ time, $t_{d}$ day_

## reference vs reference
To check the capability of the prediction we take as reference the customer data and as activities the customer data multiplied by a random noise

![reference](../f/f_mot/ref_vs_ref.png "reference vs reference")
_reference vs reference + gaussian noise, a single location might have low correlation_

![reference](../f/f_mot/ref_vs_ref_sum.png "reference vs reference sum")
_reference vs reference + gaussian noise, overall sum neutralizes the gaussian noise_

![scor1](../f/f_mot/score1.png "score gauss noise 0.5")
_score gauss noise 50%_

![scor1](../f/f_mot/scor_ref2ref.png "score gauss noise 0.9")
_score gauss noise 90% no smoothing, final score on 30 days_

<!-- ![scor_ref](../f/f_mot/scor_ref_vs_ref.png "score gauss noise 0.9") -->
<!-- _score gauss noise 90% with smoothing, final score on 30 days_ -->

![scor_ref](../f/f_mot/ref_vs_ref_30g.png "score gauss noise 0.3")
_score gauss noise 30%, final score on june_

![scor_ref](../f/f_mot/ref_vs_ref_20g.png "score gauss noise 0.2")
_score gauss noise 20%, final score on june_

## day correlation mapping
We take the first [20 cilacs](/tank/act_cilac.csv.gz) close to a [poi](/tank/poi.csv) and we [calculate activites](/activity/qsm.activity_report.tank_cilac_t1.json) on daily basis.

Activities are processed with a 20km previous distance filter and we [match activity chirality with the poi chirality](/etl/proc_tank.py).

6% of the total cilacs correlates over 0.6 with [reference data](/f/f_year.csv.gz).

The sum of the activities over all country is

![cilac sum](../f/f_mot/cilac_sum.png "cilac sum")
_no day filtering_

We have to filter out bad days

![cilac sum](../f/f_mot/cilac_sum_filter.png "cilac sum")
_bad day filtering_

We perform a weekday correction

![cilac sum](../f/f_mot/cilac_sum_wday.png "cilac sum")
_weekday correction_

![cilac_cor](../f/f_mot/cilac_2dcor.png "cilac 2d correlation")
_2d correlation between cilac patterns_

![country adjustment](../f/f_mot/country_adjustment.png "country adjustment")
_country adjustment_

etl - lowcount - wday - filter - reg
00 - 04 - 22 - 30 - 41

![scor new mapping](../f/f_mot/scor_new_mapping.png "new mapping scoring")
_iteration of the new mapping scoring_

# blind test on real data

![play equal_learn](../f/f_mot/play_equal_learn.png "play equal_learn")
_test on performance on learn & play on same days_

![learn_play](../f/f_mot/smooth_improvement.png "smoothing improvement")
_smoothing correlates neighboring events and improves the score, june in blind test_

![curve blind](../f/f_mot/curve_blind.png "curve blind")
_curve blind, june_

![curve blind_single2](../f/f_mot/curve_blind_single2.png "curve blind_single2")
_curve blind_single2_

![curve blind_single](../f/f_mot/curve_blind_single.png "curve blind_single")
_curve blind_single_

![learn_play](../f/f_mot/learn_play_june.png "learn play june")
_scoring on the different learning steps until blind test_

![learn play_randomDays](../f/f_mot/learn_play_randomDays.png "learn play_randomDays")
_learn play_randomDays_

![correlation over location](../f/f_mot/correlation_overLocation.png "correlation over location")
_correlation over locations_

