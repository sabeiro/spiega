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

![antani_logo](f_ops/antani_logo.svg "antani logo")

_ants optimizing paths on a network_

## workflow

The optimization engine has user controlled and automated modules

![ops_app](f_ops/ops_app.svg "ops_app")

_ops application_

We retrieve information directly from the fleet console microservices 

![man_console](f_ops/management_console.png "man console")

_management console_

We collect the current status with a single api call

```python
resq = requests.get(url=cred['node_url']+"/users/actions/",headers=headers)
resq = requests.get(url=cred['node_url']+"/geodata/zones/",headers=headers)
resq = requests.get(url=cred['node_url']+"/geodata/zones/"+id_zone+"/areas",headers=headers)
resq = requests.get(url=cred['node_url']+"/geodata/areas/deployment/zone",headers=headers,params={"zoneIdentifier":g['zoneIdentifier']})
```

The fleet engine sits in the middle and steers all operations, tracking and monitoring log the current status

![obj_dev](f_ops/obj_dev.svg "obj_dev")

_development of objectives_

In the fleet engine 4 objects will be defined with an hierarchical structure 

![metric_ops](f_ops/metric_ops.svg "metric_ops")

_metric operations_

The purpose of the optimization engine is to compute profitability for each drive and iterate all over the possible solutions 

![task preparation](f_ops/task_preparation.svg "task preparation")

_field operation assignement_

For each *drive* is calculated a cost and a rating

For Each *task* is calculated a revenue and a risk

<!-- To enable parallel work we need to move from a graph design -->

<!-- ![engine_design_old](f_ops/engine_design_old.svg "engine design") -->
<!-- _engine design, current scheme_ -->

<!-- To a linear design where the engine just orchestrate the calls and there is always a cached table to substitute a broken service -->

<!-- ![engine_design](f_ops/engine_design.svg "engine design") -->
<!-- _engine design, suggested scheme_ -->




## design

To enable parallel work we need to move from a graph design

![engine_design_old](f_ops/engine_design_old.svg "engine design")
_engine design, current scheme_

To a linear design where the engine just orchestrate the calls and there is always a cached table to substitute a broken service

![engine_design](f_ops/engine_design.svg "engine design")
_engine design, suggested scheme_

We draw a cut between field operation and task optimization

![infra_design](f_ops/infra_design.svg "infra design")
_infra design_

