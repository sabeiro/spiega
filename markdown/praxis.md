---
title: dev practices
author: Giovanni Marelli
date: 2019-09-12
rights:  Creative Commons Non-Commercial Share Alike 3.0
language: en-US
id: dev_praxis
category: #tech
roam_refs: dev practices
roam_aliases: ["dev practices"]
output: 
	md_document:
		variant: markdown_strict+backtick_code_blocks+autolink_bare_uris+markdown_github
---

# dev practices

Software development and deployment imply  contemporary praxis to assure a reliable solution; easy to maintain and debug and expand.

# software life cycle

The analysis proceeds by steps assessing the solidity of the different components:
* Code: check the fulfilment of standards (naming convention, documentation)
* Testing: the tests put in place to mek sure broken application aren't reployed in production and debugging is quicker
* Organization: the code should be organized in sections splitting the different topics into different folders: (API, batch processes, UI, common libraries, tests, examples...)
* Review: which peer review or approval process is in place
* Pipeline: the scripts used to push the code, test the configuration, deploy on a dev server, test the deployment
* Libraries: important functions should compose a library for general usage

# infrastructure

Modern applications require many services to be integrated in the productive environment. Compared to native applications; micorservices need to be incorporated into a bigger infrastructure.

* Authentication: regarding access to a webapp, a backend service, database entries, file stored...
* Security: which kind of access is allowed to which user/application
* Speed: are the services responding quickly enough?
* Scalability: does the infrastructure scale with user usage and data size?
* Protocols: do applications interact with the same standards?
* Storage: is the retetion set up appropriately for the need for speed, reliability and redundancy? Is there an appropriate choice of filesystems, databases and stream data?

# UI/UX

Typical checks for end user applications:
* Speed: is the response time practical?
* Errors: broken links, typos, wrong visualization
* Support: in case of errors or malfunctions how can the user get assistance?
* Features: is the result as expected?
* Exandability: how easy is to expand the app?

# observability
Applications should log important transactions which will be visualized by a BI tool:
* Requests: are the single requests being stored?
* Metrics: are metrics store for quality checks?
* Notification: who is going to be notified for bad performances and what is the process in place?

# batch processing:
Some processes are initiated by a trigger event or a time schedule and perform time demandind operations in the background when the user traffic is a least
* Scheduling: is the frequency/trigger correct?
* Notification: who is going to be notified for bad performances and what is the process in place

# documentation

Documentation is essential for the life span of software

* Dev: dev users should find the proper information regarding APIs
* Deployment: devops should know how to deploy the solution
* End users: all the app consumers should know how to use the main functions and whom to contact in cas of issues

# AI platform

An AI platform should be capable of providing AI solutions in an efficient and reliable fashion:
* Access: data should be accessible
* Fit for purpose: data should contain the relevant information; all sensitive data should be pre-filtered or anonymized
* Aggregation: the strategy to quickly access data by batch processing granular data which can consume unnecessary resources and make training and inference unpractical
* Consistency: a mechanism should check which time frame contain consistent data and whether there is any drift between data an the time of roll out and the current state
* Versioning: models and weights should be versioned to make analysis possible. Training data too
* Ethics: a bias analysis to make sure no decision would be taken based on discrimination
* Measurability: ML outputs should be evaluated and monitored to assure consistent results

# LLM

Large language models can properly fulfill their tasks making sure some configurations are set correctly:
* Prompt: prompts define the type of agent and help in providing coherent answers
* Retrival: the mechanism to search within the knowledge base and correctly rank results
* Fine tuning: are the model parameters correctly configured for the type of agent needed?
* Model: which of the available models performs at best and has a convenient cost?
* Document preprocessing: a wrong preprocessing of the documents will cause the retrieval to fail
* Aggregation: batch processing of the documents allos the creation of multi-level indexing to allow a faster and more consistent retrieval
* Evaluation: the answer should be checked against metrics to stop eventual incorrect results


# programming praxis

The key principles for a proper collaborative programming are:

* clearness - readability
* testing
* debugging
* scalability of code
* modular: reusability of code, libraries

## libraries

## classes

## naming convention

* function names should tell the purpose of the function (not only a feature)
* varibles should contain the structure type when possible (file_path, file_name, file_byte, file_type)


## testing

lint: static code analysis
unit: test of the single unit (function, class)


## collaborative programming

## versioning

# environment

## virtual environment

Using a vitual environment helps handling incompatigle library versions. Usually each service ends into a separated container and hence the virtual is redundant. In some cases for local development can be useful although makes space management more difficult.

## .env

## export variables

# documentation

```python
"""
 function that does a lot
 param:
 


```
