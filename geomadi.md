# Geomadi
Geomadi is a collection of utils for training on geo data.


## Competitor locations
The scope of the project is to count how many motorway drivers stopped by a competitor. 
The current definition of a competitor is weak since a motorway driver has a more dense options to stop for fuel/eating:
![competitor_location](f_mot/competitor_location.png "competitor locations")
_customer locations (blue) and competitor ones (purple), a driver has many more options than the ones pointed (from google maps)_

It would be much more reliable to label all the users who have been routed on a motorway and report all the activity with a short dwelling time:

![heatmap](f_mot/heatmap.png "motorway stoppers heatmap")
_heatmap of motorway drivers stopping during a trip_

