---
title: "routific"
author: Giovanni Marelli
date: 2019-07-02
rights:  Creative Commons Non-Commercial Share Alike 3.0
language: en-US
output: 
	md_document:
		variant: markdown_strict+backtick_code_blocks+autolink_bare_uris+markdown_github
---

# routific

We use routific to distribute tasks to drivers

![routific](../f/f_ops/routific.png "routific")

_routific dashboard_

Limitations of routific:

* not improving on revenue
* not optimizing on total drive time
* priority change routes but don't change graphs

# optimization engine comparison

An optimization engine find the best combination for assigning tasks to a fleet.
To compare performances we create a set up of around 600 spots, 6 task types (with different priorities) and a fleet of 8 drivers

![setup](../f/f_ops/comp_setup.png "comp setup")
_set up for the comparison_

We prepare the job file and we send it to the routific api service and [visualize the solution](http://routific-viewer.herokuapp.com/jobs/k24ozyff68)

![routific](../f/f_ops/routific.png "routific")

_routific solution explorer_

We perform a visual inspection of routific work, we see that routes mix a lot

![routific_evaluation](../f/f_ops/prob_1.png "routific evaluation")

_routes have internal intersection and operation areas cross_

Sequences don't make much sense

![routific mix](../f/f_ops/routific_sequence.png "routific mix")

_routifix sequence_

In the city center where is harder to park many drivers cross the same streets

![routific mix](../f/f_ops/routific_mix.png "routific mix")

_routifix mixing drivers_

There are some long deviations and once on the spot routific is ignoring neighboring tasks and skipping important priorities

![routific_evaluation](../f/f_ops/prob_way.png "routific evaluation")

_long routes_

We observe long deviations for a single task

![routific_evaluation](../f/f_ops/prob_single.png "routific evaluation")

_visual inspection of routific_

Even if we have [priority 1 over all tasks](http://routific-viewer.herokuapp.com/jobs/k2g4jwwj197) routes don't make much sense

![routific_evaluation prio1](../f/f_ops/prob_prio1.png "routific evaluation")

_visual inspection of routific_

Long deviations for driving on a tunnel where the scooter is on the ground

![routific_tunnel](../f/f_ops/prob_tunnel.png "routific evaluation")

_routed into a tunnel_

Routific returns more stops than the number of tasks

![routific_capacity](../f/f_ops/routific_cheating.png "routific maximum capacity")

_routific and maximum capacity_


Routific returns only the total drive time and we have to reroute the segments to calculate the actula driven distance

