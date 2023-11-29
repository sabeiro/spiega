---
title: "Motion"
author: Giovanni Marelli
date: 2019-07-02
rights:  Creative Commons Non-Commercial Share Alike 3.0
language: en-US
output: 
	md_document:
		variant: markdown_strict+backtick_code_blocks+autolink_bare_uris+markdown_github
---

# scheduler

Alternative schedulers and their usage.

## airflow

Airflow is probably the most used scheduler with many features and pretty demanding in terms of resources.

[airflow](../f/f_sawmill/airflow_scheduler.png "scheduler")
_overview of airflow scheduler_

## deployment

We use the following [`docker-compose.yaml`](https://github.com/sabeiro/sawmill/blob/master/docker/airflow/docker-compose.yml) to deploy airflow which includes the following containers

* redis
* webserver
* scheduler
* workers
* init db
* flower

## DAGs

Each job is composed by a Direct Acyclic Graph which can be scheduled with a given frequency and starting time. 

We use the crontab syntax to schedule the jobs:

`min h day month day_name`

The DAG can be called in python with the following operator which calls the function `parseS3`


```python
with DAG(dag_id="s3_pull",start_date=datetime.datetime(2022,11,14),tags=["froms3"],schedule='30 3 * * *') as dag:
    def s3_pull():
        parseS3(day=yesterday)
    PythonOperator(task_id="s3_pull", python_callable=s3_pull)
```

Here some [python examples](https://github.com/sabeiro/sawmill/tree/master/dags)

