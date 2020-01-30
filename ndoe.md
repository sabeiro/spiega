---
title: "ndoe"
author: Giovanni Marelli
date: 2019-09-11
rights:  Creative Commons Non-Commercial Share Alike 3.0
language: en-US
output: 
	md_document:
		variant: markdown_strict+backtick_code_blocks+autolink_bare_uris+markdown_github
---

# ndoe

Ndoe is a collection of utils for motion analysis and spatial evaluation

## demand prediction

[demand prediction](activation.md)

* theoretical activation potential
* aggregation of demand and offer on geohash

![demand_prediction](f_act/map_urev.png "unit revenue")

## location 

* enrichment of geo features on geohash
* prediction on single geohash

[spatial operations and geographical transformation](location.md)

![pop_dens](f_act/popDens_interp.png "population density")

## evaluate operations metrics

* restructuring data based on quantities of interest
* motion patterns

[evaluates operations](ride.md)

![ride_map](f_mov/ride_map.png "ride maps")

## optimization engine

* Monte Carlo and Markov chains
* convergent solutions

[optimization engine](optimization.md)

![opt route](f_ops/optimization_8.gif "optimization route")

## dynamics of motion

[dynamics of motion](motion.md)

* from coordinates to dynamic of motion
* city mobility

![motion](f_mov/dwelling_city.png "dwelling city")

## routing and graphs

[routing and graphs](routing.md)

* building an efficient graph based on mean of transportation
* finding the most optimal path and calculating weighting matrices

![dwelling and motion](f_ops/graph_weight.png "dwelling city")
