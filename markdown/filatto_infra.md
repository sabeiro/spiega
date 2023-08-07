---
title: "Filatto"
author: Giovanni Marelli
date: 2019-11-18
rights:  Creative Commons Non-Commercial Share Alike 3.0
language: en-US
output: 
	md_document:
		variant: markdown_strict+backtick_code_blocks+autolink_bare_uris+markdown_github
---

# Delivery SaaS

Filatto is a SaaS for micro-mobility based delivery which is able to interact between demand and supply integrating different components

**Principles**:

* cloud based
* full-API
* modular
* open source

**Key components**:

* manage, organize, diplay supply 
* collect and organize the status of the delivery workforce
* provide to the consumer the option to order
* accept the order and pay
* track delivery status

# Infra

In this document we present the infra design for the order and delivery 

![](../f/f_ops/filatto_structure.svg "filatto structure")

_Sketch of the infra suggested_

We are going to use the separate components 

## ERP 

The suggested ERP for the project is [odoo](https://www.odoo.com/), reason is:

* cloud based
* on prem/Saas
* open source, highly configurable
* huge marketplace of apps with many vendors
* website/e-commerce builder
* full-API

![odoo](../f/f_ops/odoo.png "odoo apps")
_view on odoo apps_

In any case the middelware is a separate component and can be integrated with any full-API ERP.

## Middelware 

The middelware is the key component of the project and hadles all the requests between the three parties: 
* consumer app
* provider app 
* delivery app
* ERP

![filatto_infra](../f/f_ops/filatto_infra.svg "filatto infra")
_The middelware will receive and map supply and demand_


## data storage

The data storage strategy consists in using different types of DBs to store and query the data. 

* Demand and supply will be stored in a relational DB
* Maps and areas as geo shapes in mongo 
* Customers preferences as graphs

![filatto_infra](../f/f_ops/filatto_db.svg "filatto infra")
_storage and suggested data bases_

## optimization

An additional service will take care of optimizations:

* delivery availability
* operating areas
* routing: delivery time

Plese refer to [infra](antani_infra.html)

![antani_infra](../f/f_ops/antani_infra.svg "antani infra")
_deployment of antani_


## Apps

The consumer app is designed following this project [intertino](https://github.com/sabeiro/intertino/angular/qr_ang).
In short:

* front-end dev using nodejs (react/angular)
* test with ionic
* compile with ionic

The end result will be an android or ios app.

The users of the app will be:

* suppliers
* delivers
* consumers

# Partnerships

## orders

|company|infra|
|takelocal|??|

## fleets

|company|infra|
|??|??|

# Addressable market

* Restaurants-clients: food delivery
* Shops-clients: grocery delivery
* C2C: parcel delivery

# ERP settings

* Definition of shifts: relative restaurants, operating areas, operating time shifts
* Booking rider's shifts from the ERP
* Fleet management: route the request on other fleets in case riders are booked
* Three categories of rider payments: freelance, monthly salary, weekly salary
* Riders availability calendar, booking system, performance reporting, bonus/malus reporting
* Payment system: e-invoice, direct debit


