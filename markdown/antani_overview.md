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

# antani

Ant - agent/network intelligence 

![antani_logo](../f/f_ops/antani_logo.svg "antani logo")
_ants optimizing paths on a network_

Antani is an agent/network based optimization engine for field operations. Antani efficiently associate a series of tasks to the most eligible operator.

## overview

Optimization is about finding one optimal configuration for a given system, in this case we want to look for the best asssesment to dispatch $n$ drivers among $m$ tasks

![optimization_8](../f/f_ops/vid_8.gif "opt_8")
_optimization 8 vans_

## methodology

[basic concepts](antani_concept.html)

The method consists in creating a network connecting tasks and move ants across network edges to find the most convenient solution.

![antani_concept](../f/f_ops/concept_antani.svg "antani concept")
_antani concept_

Each ant can, sense, move, act and based on the reward the best current solution is taken. 

![concet_antani](../f/f_ops/antani_concept.svg  "concept antani")
_definition of an ant_

## graph

[graph building utilities](geomadi_graph.html)

* retrieving a network
* building and fixing a graph

![graph](../f/f_ops/graph_detail.png "graph detail")

_graph formation_

Once created the graph we simplify the computation pre calculating all the routes from geohash to geohash. 

![routing_info](../f/f_ops/routing_info.svg "routing info")
_routing information_

The cached information fills a database storing the most relevant origin destination connection.

![routing_database](../f/f_ops/routing_database.svg "routing database")
_routing database_

## Markov chains

To suggest a move from one spot to the next we use Markov chains based on graph connections, for each spot we find the most relevant links and transition probabilities to the closest spots.

![markov_chain](../f/f_ops/markov_3.png "Markov chain")
_Markov chains_

## posterior probability

While collecting data we can calculate more reliable estimation of transition probabilities considering Bayesian inference on real data

![post_prob](../f/f_ops/post_prob.svg "posterior probabilities")
_posterior probabilities_

## setting up

We sum up all the tasks into the corresponding geohash and calculate the transition probability between two hexagons.

![concept_mallink](../f/f_ops/concept_mallink.svg "concept mallink")
_summing up tasks per geohash and connecting the spots weighting the edges_

## engine

[engine functionalities](mallink_engine.html) 

* list of moves
* performances

![engine](../f/f_ops/vid_phantom.gif "engine")

_engine description_

## reinforcement learning

We use reinforcement learning to find the best move for a given simulation time and task completion

![reinforce_move](../f/f_ops/reinforce_move.svg "reinforce move")
_reinforcement learning for move probability_


## kpi

[kpi comparison](antani_kpi.html)

* definition of kpis
* different kpi per run

![kpi](../f/f_ops/kpi_comparison.png "kpi comparison")

_kpi comparison_

## frontend

We provide a [frontend solution](http://localhost/antani_viz/) under the production vpn

![frontend](../f/f_ops/antani_frontend.png "antani frontend")

And a video explaining the [functioning of the frontend](http://localhost/antani_demo.mp4)

## infra

[infrastructural design](antani_infra.html) 

* backend - endpoints
* frontend
* aws/productization

The solution consists in a series of microservices, many microservices have backup solutions or cached information to garantee operativity.

![engine_design](../f/f_ops/engine_design.svg "engine design")
_design of the engine_

The system is dockerized and linked with docker compose into an instance

![antani_infra](../f/f_ops/antani_infra.svg "antani_infra")
_docker and microservices_

We expose a series of endpoints on different clusters, the backbone application orchestrate the calls.

![infra_design](../f/f_ops/infra_design.svg "infra design")
_infrastructure design_

