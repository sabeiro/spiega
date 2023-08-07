---
title: "mallink_engine"
author: Giovanni Marelli
date: 2019-10-08
rights:  Creative Commons Non-Commercial Share Alike 3.0
language: en-US
output: 
	md_document:
		variant: markdown_strict+backtick_code_blocks+autolink_bare_uris+markdown_github
---

# Optimization

Optimization is finding one optimal configuration for a given system 

![optimization_8](../f/f_ops/vid_8.gif "opt_8")
_optimization 8 vans_

# optimization task

We have to find the most efficient distribution tasks among drivers to minimize costs and maximize revenue

![optimization_engine](../f/f_ops/optimization_engine.svg "optimization engine")

_optimization problem_


## optmimization engine

We need to reduce the drive time and focus on most interesting spots

<!-- <video controls><source src="../f/f_ops/linea.mp4"></video> -->
<!-- _optimization procedure_ -->

### routing efficiency

We first add all the spots a van could see and we calculate the most optimal route connecting the spots

![spot_connection](../f/f_ops/spot_connection.png "spot connection")

_spot connection_

### spot prioritization

Prediction should define the layers where we are most confident about the revenues for a given time and weather condition

We define the revenue as:

![map_pot](../f/f_act/map_pot.png "map potential")

_potential of that area for a given weekday and shift number_

$$ \mu_{deploy}n_{deploy}E_{deploy} + \mu_{collect}n_{collect}E_{collect} $$ 

Where $\mu$ is the potential to add or remove a scooter at a certain spot, $E$ is the revenue per scooter, $n$ is the number of scooters

and the costs as:

$$ l_{ride}c_{lenght} + n_{stops}c_{stops} $$

Where $l$ is the lenght, $n$ the number of stops and $c$ empirical parameters.

The energy calculation considers the single paths and the interaction among them:

[mallink_energy](../f/f_ops/concept_mallink_energy.svg  "mallink_energy")

## class structure

We display the interdepency

[module_mallink](../f/f_ops/module_mallink.svg  "module_mallink")


### solve problem

We can toggle the activation of the spot and recalculate the energy and apply the Metropolis algorithm to see whether the move is convenient

![opt_graph](../f/f_ops/opt_graph.png "opt graph")

_optimization graph_

The total energy of the system decreses

![opt_nrg](../f/f_ops/nrg_small.png "opt nrg")

_optimization energy_

We consider a larger system 

![opt_nrg](../f/f_ops/opt_large.png "opt nrg")

_larger system_

But after many iteration steps the solution is slowly approaching

![opt_nrg](../f/f_ops/nrg_blank.png "opt nrg")

_optimization energy, slowly learning_

# Markov chain

To improve the acceptance rate of moves we introduce Markov Chains

![markov_schema](../f/f_ops/markov_schema.svg "markov schema")

_Markov schema_

We multiply the Markov chain matrix with itself to condense iteration probabilities and set up a threshold to consider only the most important links

We calcualte at first a really dense Markov chain (first power) and we increase the power (until five) to have a sparse Markov chain 

![markov_chain](../f/f_ops/markov_dens.png "markov 1")

_Markov chain densities_

We than use a sparse Markov chain with around 7 links per node

![markov_chain](../f/f_ops/markov_3.png "markov 1")

_sparse markov chain_

From the Markov chain we create a cumulative probability which is getting simpler while increasing the number of iterations

![cumulative probability](../f/f_ops/cumulative_prob.png "cumulative probability")

_cumulative probability on filtering_

## iterating to the solution

We run over 500 spots and 8 drivers

![optimization_8](../f/f_ops/vid_8.gif "opt_8")
_optimization 8 vans_

and iterate over different solutions

![optimization_8](../f/f_ops/vid_8a.gif "opt_8")

_optimization 8 vans_

We can control the energy evolution and check the aymptotic behaviour of the curves.

![nrg_8](../f/f_ops/nrg_benchmark.png "nrg_8")

_energy history with 8 vans_

# single task move

The engine was at first focusing on single task move which was making convergency pretty slow. We started than introducing new moves and initial set up

![single spot move](../f/f_ops/vid_blank.gif "single spot move")

_single spot move, solutions are a bit crowded_

each driver start from a different k-mean cluster

![start_clustering](../f/f_ops/start_cluster.png "start clustering")

_distribution of the closest spot to a cluster_

We have than a better separation of routes

![single spot move](../f/f_ops/vid_newMarkov.gif "single markov")

_single markov chain_

![single move energy](../f/f_ops/nrg_blank.png "single move energy")

_energy evolution for single move engine_


## extrude, phantom, canonical

We define a series of moves to re-sort ants across the network

![series_moves](../f/f_ops/move_mallink.svg "series of moves")
_series of moves_

For speeding up operations we introduce a series of moves to improve run time and convergency.

*Extruding* is suggesting a chain following the Markov Chain probability

![extrude move](../f/f_ops/vid_extrude.gif "extrude move")

_extrude move_

With extrusion we dicrease calculation time to 1/10 getting to the same run time as routific.

We realize that sometimes some routes get trapped in a local minimum and we can't get complete the occupancy of the van. Therefore we introduce *phantom* drivers so we have the option to discard uncomplete runs

![phantom move](../f/f_ops/vid_phantom.gif "phantom move")

_phantom move_

Depending on the stage of the solution certain solutions are more appropriate than others

![nrg_canonical](../f/f_ops/nrg_grand.png "energy canonical")

_energy distribution for canonical simulations_


To further improve convergence of solution we move to *gran canonical* simulation where we continously introduce and remove routes until we get to the best complete solution

![canonical move](../f/f_ops/vid_canonical_trap.gif "canonical move")

_canonical move_

