---
title: cloud providers
author: Giovanni Marelli
date: 2019-09-12
rights:  Creative Commons Non-Commercial Share Alike 3.0
language: en-US
id: cloud_providers
category: #tech
roam_refs: cloud providers
roam_aliases: ["cloud providers"]
output: 
	md_document:
		variant: markdown_strict+backtick_code_blocks+autolink_bare_uris+markdown_github
---

# cloud providers

The main cloud providers or hyperscaler for the '20 decade are aws, gcp and azure and they differentiate for their scalability from fixed resource booking data centers like digitalocean, linode and others are used too. 
Here is a good [overview on aws](https://www.youtube.com/watch?v=Z3SYDTMP3ME).

## App deployment on-prem vs AWS

**On prem**: I launch an instance from my cloud provider, I log into it with ssh, I install the libraries and launch the application, install and configure nginx, create certificate with certbot and rerun nginx.
**AWS**:

* I create a VPC
* I create a internet gateway
* I add a subnet and add routes from the public
* I create an EC2 in that VPC
* I create an elastic IP to attach to the EC2
* I create security groups that allow at least ssh and http
* I log into the instance, install libraries, run the application, launch it, install nginx
* I can't use certbot so I need to activate cloudfront
* I create a load balancer
* I create a target group where my EC2 sits
* I create a cloudfront distribution
* request a certificate for your cloudfront domain


# filesystem

Filesystems are a great option for backups, cheap cold storage. Big files are usually stored in parquet 

* _aws_ s3
* _gcp_ filestore
* _azure_ files
* _digitalocean_ space

# query engine 

* _gcp_ big query
* hive

# orchestration

* kubernetes
* microk8s
* openshift
* docker swarm

# spark

* _aws_ EMR
* _azure_ deltashare
* databricks

# storage 

## relational

* _aws_ RDS
* _on prem_ postgres

## document

* mongo
* _aws_ dynamoDB

# instances

* _aws_ Elastic Map Reduce
* _aws_ ec2 instances
* _gcp_ compute engine
* _digitalocean_ droplet

# ML ops

* _aws_ sage maker
* ML flow
* Kubeflow
* _netflix_ metaflow
* Kedro
* _h2o_ autoML

# warehouse, query

* _aws_ athena: a serverless Analytics service to perform interactive queries over AWS S3
* _aws_ redshift: fully managed, petabyte data warehouse service over the cloud
* _gcp_ big query
* _snowflake_
* _hadoop_ hive

# load balancing

* celery 
* _asw_ elastic load balancer
* _aws_ api gateway

# data integration, ETL, batch processing

* _aws_ glue
* _aws_ lambda
* _apache_ airflow
* _gcp_ pubsub
* _hadoop_ yarn
* snowflake (with storage)
* dbt

# logs, tracking

* _on prem_ elasticsearch
* _on prem_ kibana, grafana
* _aws_ cloudwatch
* prometheus

# cloud monitoring

* datadog

# cloud formation

* terraform

# messagging

* _apache_ kafka
* redpanda
* _aws_ kinesis


# business intelligence

* _on prem_ metabase
* _on prem_ superset
* _azure_ powerBI, tableau


