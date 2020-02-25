---
title: "ODM via"
author: Giovanni Marelli
date: 2019-02-26
rights:  Creative Commons Non-Commercial Share Alike 3.0
language: en-US
output: 
	md_document:
		variant: markdown_strict+backtick_code_blocks+autolink_bare_uris+markdown_github
---

# ODM

References

* [data](sftp://172.25.100.50/home/gmarelli/lav/motion/raw/statWeek/)
* [script](http://172.25.186.11:8000/gmarelli/geomadi/blob/master/etl/proc_statWeek.py)
* [viz](sftp://172.25.100.50/home/gmarelli/lav/motion/gis/ptv/)

### Geometry issues

On MTC geometry we have only *short range relationships*

![mtc ags8](../f/f_odm/mtc_ags8.png "mtc ags8")
_mtc ags8_

We are loosing a lot of relations but still we are *multiplicating counts* (MTCs cover a larger area than ags8):

![weekday](../f/f_odm/weekday.png "weekday")
_weekday_

on top MTC have a larger *k30 effect*, you can see the difference between a single weekday (sum of 6 days) and a workday (sum of 30 days)

![hourly weekday](../f/f_odm/hourly_weekday.png "hourly weekday")
_hourly weekday_

MTC are +/- as many as ags8

There are some traffic specific geometries 

![re../f/f_geom](f_odm/ref_geom.png "reference geometry")
_reference geometry_

> We shouldn't use not density based mappings nor mappings which are not considering geographical boundaries.

## via report

We run a via report selecting some nodes close to the customer reference data

![pvt vs_odmVia](../f/f_odm/ptv_vs_odmVia.png "pvt vs_odmVia")
_pvt (blue/one direction) vs_odmVia (green)_

Our graph is bidirectional for all secondary streets and for each selected node we count all the traffic in both directions.

### via report origin-destination

We run a report with origin - via - destination metrics on the selected via nodes

![node_location](../f/f_odm/node_location.png "node location")
_selected nodes_

Usege of via nodes on a origin and destination matrix

![od_via](../f/f_mod/od_via.ong "od via")
_origin destination and via point_



But we have reasonable O&D relations

![o and_d](../f/f_odm/o_and_d.png "o and d")
_o and_d_

We picked only residential streets in oberhaching which means that if I start in Augsburg i end only in oberhaching

![origin north](../f/f_odm/origin_north.png "origin north")
_origin north_

But if I come from austria I might end in Munich and use oberhaching as a shortcut.

![origin south](../f/f_odm/origin_south.png "origin south")
_origin south_

If I come to the north I use only few via points

![via north2](../f/f_odm/from_north.png "via north2")
_from north_

If go to the north I have an asymmetrical relation

![via north](../f/f_odm/to_north.png "via north")
_to north_




