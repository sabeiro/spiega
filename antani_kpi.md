---
title: "antani_kpi"
author: Giovanni Marelli
date: 2019-07-02
rights:  Creative Commons Non-Commercial Share Alike 3.0
language: en-US
output: 
	md_document:
		variant: markdown_strict+backtick_code_blocks+autolink_bare_uris+markdown_github
---

# optimization engine comparison

An optimization engine find the best combination for assigning tasks to a fleet.
To compare performances we create a set up of around 600 spots, 6 task types (with different priorities) and a fleet of 8 drivers

![setup](f_ops/comp_setup.png "comp setup")
_set up for the comparison_

We prepare the job file and we send it to the routific api service and [visualize the solution](http://routific-viewer.herokuapp.com/jobs/k24ozyff68)

![routific](f_ops/routific.png "routific")

_routific solution explorer_

# optimization engine

We can run the optimization engine from a blank system or after a routific solution.

![route engine](f_ops/route_engine.png "route engine")

_comparison between routing engine_

Starting from a routific solution we see that the optimization engine at first improves big springs

![routific_evaluation](f_ops/prob_2.png "routific evaluation")

_optimization improves big springs_

We use the following kpi:

* `completion`: percentage of van capacity filled
* `duration`: time spent
* `potential`: value of the van
* `distance`: distance of the route

The score is calculated via:

$$ score = \frac{occupancy * potential}{duration * distance} $$


![kpi comparison](f_ops/kpi_comparison.png "kpi comparison")

_comparison of kpi between engines_

<!-- If we consider routed distances the figure change -->

<!-- ![kpi comparison routed](f_ops/kpi_compRouted.png "kpi comparison routed") -->

<!-- _comparison of kpi between engines using routed distances_ -->


# run time

Routific was sending a complete solution within 3 minutes, the optimization engine was sending a better solution in 30 minutes, to speed up the process we introduced new moves

![execution time](f_ops/execution_time.png "execution time")

_execution time_

