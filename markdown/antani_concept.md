---
title: "Antani"
author: Giovanni Marelli
date: 2019-11-18
rights:  Creative Commons Non-Commercial Share Alike 3.0
language: en-US
output: 
	md_document:
		variant: markdown_strict+backtick_code_blocks+autolink_bare_uris+markdown_github
---

# Antani

Ant - agent/network intelligence 

![antani_logo](../f/f_ops/antani_logo.svg "antani logo")

_ants optimizing paths on a network_

## Efficiency

Why operation efficiency?

* Fill the gap between revenue and cost
* Think as a network, not single operator
* Select the most valuable tasks

## Problem

The closest path facing the warehouse fullfilling the most valuables tasks

![optimization_engine](../f/f_ops/optimization_engine.svg "optimization engine")

_optimization engine requirements_

* Focus on profitability
* Plan shifts
* Consider task time and revenue

## Commercial softwares?

Delivery based, routific:
* Long deviations
* Skipped tasks
* Unclear priorities

![routific_problems](../f/f_ops/prob_prio1.png "routific problems")

_problems with routific_

No resuming, everytime a new simulation

## Google or-tools?

open source software suite for optimization

![problems_ortools](../f/f_ops/problem_ortools.svg "problem ortools")
_or-tools solutions_


Many crossing Incomplete vans, long trajectories:

* incomplete solution (-20%)
* job to be killed
* 0.5-75mins

## In house solution

![optimization engine](../f/f_ops/vid_8.gif "optimization engine")
_in house optimization engine_

Step by step task assignement

## Path optimization
Path like polymers

![phd defense](../f/f_ops/phd_defense.png "phd defense")

_PhD defense – computational biophysics 2012_

## Optimization engine

Ludewa/Tanzania - 2013

![electrical line](../f/f_ops/animation_optimize.gif "electrical line")

_Electrical line design to connect households to the new power plant_

## Building a graph

From detailed street network to an efficient graph

![graph_detail](../f/f_ops/graph_detail.png "graph detail")
_Subset, connect, simplify, subgraph, check directions..._

## weighting

Weight every segment

![graph_weight](../f/f_ops/graph_weight.png "graph weight")

_Maxspeed, streetclass, length, junctions_

## Graph setup

Checking routes

![graph undirected](../f/f_ops/graph_undirected.png "graph undirected")

_checking routes_

Good correlation between spot2spot
routes in graphs and air distance

Osrm – open street routing machine

## Routes

Subset the city in geohashes (~70m)

![routing_info](../f/f_ops/routing_info.svg "routing info")

_routing information_

Calculate all pair distances and build a lookup database

![routing_info](../f/f_ops/routing_database.svg "routing info")

_pair relationship database_

## Tasks

Sum up tasks in the same geohash

![mallink_concept](../f/f_ops/concept_mallink.svg "mallink concept")

_graph edges kept_

Keep only neighbor connections between tasks

# Sense move reward

Ant/colony


![antani_concept](../f/f_ops/antani_concept.svg "antani concept")
_an ant per loop, iterate over the network_



![concept_energy](../f/f_ops/concept_mallink_energy.svg "concept energy")
_energy definition_

Energy:
* +separation
* +task value
* - area
* - task time
* - tot distance

## Path/network

An ant connecting each task

![concept_antani](../f/f_ops/concept_antani.svg "concept antani")

_antani concept_

## Path opt

![opt_graph](../f/f_ops/opt_graph.png "opt_graph")

_optimize sequences_

## Monte Carlo

Single random move

![optimization engine](../f/f_ops/vid_8.gif "optimization engine")

_energy evolution_

Asyntotic energy and move acceptance rate evolution

## Markov Chains

Transition probabilities, limit links

![markov_chains](../f/f_ops/markov_3.png "markov chains")
_markov chains_

We limit the possible moves leaving the most probable

## Enhance moves

single, Markov, distance, extrude

![move mallink](../f/f_ops/move_mallink.svg "move mallink")

_move selection_

Spot selection according different probabilities

## Simulation boost

* Faster convergency
* Higher acceptance

![optimization engine](../f/f_ops/vid_8.gif "optimization engine")

![optimization engine](../f/f_ops/vid_phantom.gif "optimization engine")

Single move, routific optimization, Markov chain, extrusion, grand canonical...

## Calculation time

![execution time](../f/f_ops/execution_time.png "execution time")

_Early simulations were too slow_

## Find a score:

scoring

![kpi_comparison](../f/f_ops/kpi_comparison.png "kpi comparison")

_kpi comparison_

+completion + revenue – distance - time

## Reinforcement learning

Improve acceptance

![reinforce move](../f/f_ops/reinforce_move.svg "reinforce_move")

_reinforce moves_

Single agent reinforcement is too slow and chaotic

## Posterior probability

Improve with real data

![posterior probabilities](../f/f_ops/post_prob.svg "posterior probability")

_posterior probabilities_

## Demand

![demand_forecast](../f/f_act/map_urev.png "demand forecast")

_demand forecast_

## Microservice design

Backbone +microservices

![engine design](../f/f_ops/engine_design.svg "engine design")

_engine design_

## Asynchronicity

Docker, flask, redis,celery

![antani_infra](../f/f_ops/antani_infra.svg "antani infrastructure")
_antani infrastructure_

Client – broker/worker design

## Frontend

OpenLayers, d3, ajaxDocumentation

![frontend](../f/f_ops/antani_frontend.png "antani frontend")
_antani frontend_

## Documentation

![module mallink](../f/f_lib/module_mallink.svg "module mallink")

_module mallink_

## Code

![module library](../f/f_lib/module_library.svg "module library")

_library ecosystem_

...started in 2006

## Outlook

* Ready for spring
* Drivers feedback
* Process real data
* Compare with rideos
* ...

## Summary

* Start, stop, resume
* First draft within few seconds
* Clear operating areas
* Weighting potential revenues
* Focus on profitability

## Acknowledgement

Circ – fleet engine team
Carlo Mazzaferro – productization of antani


# Theory

## Gibbs sampling

We describe a probability distribution via its moments $\vec{\mu}$

$$ p(\vec{x};\vec{\mu}) $$

We have a system $\vec{x}$ where each $x$ is in a certain state $s$. We define a energy function which depends on the states of system and a set of parameters $\theta$. In our case the system is a series of field tasks on a map and the state is the agent who is fulfilling the task. 


The energy of the system is the sum of the revenue per task minus the cost: task time and path length. The parameter set $\theta$ defines the revenue and cost factor + external factors (temperature $T$, traffic time $h$,...). Ideally we will express the parameter set in terms of external factors $\theta(T,h)$ or change the metric (distance) of the system $d(T,h)$

$$ E_a(\vec{x}|\theta) = n_s\cdot r_s - c_d \cdot d_a - n_s\cdot t_s $$

where $n_s$ is the number of spots, $r_s$ the total revenue per spot, $t_s$ is the total operation time, $d_a$ the distance of that agent.

The probability distribution for a certain state and parameter follows the Boltzmann distribution

$$ p(\vec{x}|\theta) \propto exp(-E(\vec{x})/kT)

Target probability distribution

$$ p(\vec{x}) = \frac{w(\vec{x})}{Z} = \frac{1}{Z} \prod_c \phi_c(x)$$

estimator

$$ \frac{1}{T} \sum_{t=1}^{T} \phi(\vec{x}) \qquad E_{p(x)}|\phi(x)| = \sum_x p(x)\phi(x) $$ 

From the state $\vec{x}$ we create a state $\vec{x}'$ where we create a sample $x_j \rightarrow x_j'$, basically: $\vec{x}' = {x_1,x_2,...,x_j',...,x_n}$

$$ p(x) = \frac{exp(E(x)/T)}{Z} $$

$$ A(x'|x) = min(1,p(x')/p(x)) = min(1,exp(\frac{ E(x') - E(x)}{T})) $$

## Bayesian statistics

We want to calculate the posterior probability [doc](https://people.duke.edu/~ccc14/sta-663/MCMC.html) which is the probability of a parameter set $\theta$ from a given state $X$

$$ p(\theta|x) = \frac{l(x|\theta)p(\theta)}{p(x)} $$ 

where $l(x|\theta)$ likelihood, $p(\theta)$ prior, $p(x'|x)$ the probability to move from state $x$ to state $x'$ and $p(X)$ normalization factor

$$ p(X) = \int d\theta* p(X|\theta*) p(\theta*)$$

The likelihood is about finding the momenta of the distribution for a given data set (usually via regression), the probability distribution is the theoretical distribution for the system (independent on the data acquired). In a correct sampling the two match.

proposal distribution $p(x)$ - target distribution $g(x) ~ p(\theta|X)$ 

Step increment $\theta' = \theta + \Delta\theta$ 

$$\rho = \frac{g(\theta'|X)}{g(\theta|X)} \qquad \rho = \frac{p(X|\theta')p(\theta')}{p(X|\theta)p(\theta)}$$




sampling from probability from a state x [doc](http://www.stat.ucla.edu/~sczhu/Courses/UCLA/Stat_202C/lecture_note/Ch1_MC_Intro.pdf)

$$ x \tilde \pi(x) $$

High dimensional computing (over all states)

$$c = E[f(x)] = \int \pi(x) f(x) ds $$

optimization

$$ x* = argmax \pi(x) $$

Learning and Bayesian hierarchical modeling for a given parameter set $\Theta$

$$ \Theta * = argmax l(\Theta) ; l(\Theta) = \sum_{i=1}^{n} log p(x_i;\Theta) $$



