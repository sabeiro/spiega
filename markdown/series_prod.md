---
title: "Forecast delivery pipeline"
author: Giovanni Marelli
date: 2019-05-20
rights:  Creative Commons Non-Commercial Share Alike 3.0
language: en-US
output: 
	md_document:
		variant: markdown_strict+backtick_code_blocks+autolink_bare_uris+markdown_github
---

# Time series forecast
## delivery pipeline

This readme explains the content of the directory and the execution steps to complete the delivery forcasts.

![curves](../f/f_mot/curves.png "delivery_curves")
_delivery curves_

This project folder does not contain any script to retune or re perform a mapping or a prediction or run sanity checks, it just applies already pretrained models. In case of unconsistency please refer to the author.

## setup

In the project directory there is an example docker file for creating an ad hoc container. 

![proj_dir](../f/f_mot/proj_dir.png "project directory")
_project directory_

To install the basic libraries please run [this script](src/setup.py) with python 3.6+. Depending on the required KPIs other graphic libraries might be installed.

All the scripts consider the variable $LAV_DIR which can be set as the current directory. Paths can be otherwise hard coded adjusted.

## tdg/cronon production

![jupyter](../f/f_mot/jupyter.png "jupyter")
_jupyter notebook on Hungarian cluster_

* check data availability for tripEx-act and adjust dates in the [qsm job](/geomadi/blob/master/job/activity/tank/qsm.activity_report.tank_cilac_y19_p11_d40_noChi.json) for activities
* check data availability for analyzer and adjust dates in the [qsm job](/geomadi/blob/master/job/odm_via/qsm.odm_extraction.odm_via_tank_19_04.json) for odm_via
* get permission from QA about submitting the jobs and set priority
* schedule the jobs
* check if the job run without any error [on the server](/tdg/results/20190515_1442_odm_via_tank_19_03)
* use the [following notebook](/notebooks/gio/etl_tank.ipynb) to postprocess the data - activity
* use the [following notebook](/notebooks/gio/etl_via.ipynb) to postprocess the data - odm_via
* download the two files from the [jupyter cluster](/motion/out/)

## local production

![mapping](../f/f_mot/mapping.png "example of mapping result")
_example of mapping result_

* Complete the date list in [this file](raw/dateList.csv)
* apply [this script](api_weather.py) to dowload the weather information for training

* apply mapping with [this script](src/mapping_apply.py) 
  * copy the cilac actRep in the [directory](/raw/tank/act_cilac_prod)
  * the output will be written write to [act_weighted](raw/tank/act_weighted)
  
* apply prediction with [this script](src/regressor_apply.py) on 
  * the prediction will be written in [act_predict](raw/tank/act_predict)
  
![regression](../f/f_mot/regression.png "results after regression")
_results after regression_
  
## KPI

![joyplot](../f/f_mot/joyplot.png "joyplot")
_differences wrt previous delivery_

Apply [this script](src/kpi_tank.py) to sum up the results for the customer delivery and check the following KPIs:

* maunal visualization of activities and via counts for all locations
* consistency with previous month
* consistency with seasonal trends
* spikes in data
* expected range in capture rate
* consistency in ranking 
* comment events that can influence the specific date/location
  
![sankey](../f/f_mot/sankey.png "sankey")
_t-test feb-mar vs t-test mar-apr, change in ranking_
  
## internal meeting

![boxplot](../f/f_mot/boxplot.png "boxplot")
_differences in capture rate between deliveries_

* organize an internal meeting at least two days before the customer delivery
* present the results against the agreed KPIs
* show a presentation similar to this [former delivery](doc/MotorwayStoppers_april.pptx)
* in case of quality issues:
  * assign tickets to the responsibles
  * reschedule the analysis (job, processing...
  * reschedule the delivery
  
![isocalendar](../f/f_mot/isocalendar.png "isocalendar")
_check against isocalender_

## finalize the delivery

Run the script [tank_delivery](src/tank_delivery.py) adjusting the output file name.

![delivery](../f/f_mot/delivery.png "delivery")
_finalize the delivery_

* manual check the numbers and prepare the excel file like in the [former delivery](delivery/act_direction_19_03.xls) (pivot...)
* update [BI dashboard](bi/) (spotfire - tableau)

## customer support

* be available on customer feedbacks and invite the concerned responsible to a meeting
* assign tickets/solve issues
* reschedule the delivery
* update the delivery

