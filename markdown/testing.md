# tests and checks

For each service there is a folder called testing with different tests to add to the CI/CD pipe.

During the software development pieces of code used to develop are essential to write short tests. Those routines are put in a separate folder and called prior to commit or during deployment. 
Ideally the deployment should fail if the test didn't pass. 

Those routine can be unit tests of single functions (especially using classes) or REST request to a service. 



## test in actions





## test db connection

```python
import os, sys, gzip, random, csv, json, datetime, re, time
import urllib3, requests
import psycopg2
from sqlalchemy import create_engine

if __name__=="__main__":
  db_name, db_user, db_pass = os.environ['DB_NAME'], os.environ['DB_USER'], os.environ['DB_PASS']
  db_host, db_port = os.environ['DB_HOST'], os.environ['DB_PORT']
  db_string = 'postgresql://{}:{}@{}:{}/{}'.format(db_user, db_pass, db_host, db_port, db_name)
  db = create_engine(db_string)
  
  res = db.execute("SELECT datname FROM pg_database;")
  for r in res: print(r)
  res = db.execute("select * from pg_catalog.pg_tables where schemaname = 'public';")
  for r in res: print(r)
```

## test endpoints

```python
import os, sys, gzip, random, csv, json, datetime, re, time
import urllib3, requests, jwt

def printOutput(resq):
  if resq.status_code < 400:
    print(resq.json())
  else:
    print(resq)
    print(resq.text)

url = "http://0.0.0.0:5005"

if __name__=="__main__":
  print("test db middleware")
  url = "http://0.0.0.0:5006"
  resq = requests.get(url+"/apidocs/")
  print(resq.status_code)
  print("test messaging middleware")
  url = "http://0.0.0.0:5005/"
  resq = requests.get(url+"/apidocs/")
  print(resq.status_code)
  print("test push message")
  inMex['id'] = inMex['id'] + 1
  resq = requests.post(url+"/push/"+topic,json=inMex,headers=headers)
  printOutput(resq)
  print("test consume message")
  resq = requests.get(url+"/consume/"+topic,headers=headers,params={"offset":1})
  printOutput(resq) 
  print("test consume message")
  resq = requests.get(url+"/latest/"+topic,headers=headers,params={"offset":5})
  printOutput(resq)
  print("test consume message")
  resq = requests.get(url+"/latest_time/"+topic,headers=headers,params={"offset":60*1})
  printOutput(resq)
  print("test list topics")
  resq = requests.get(url+"/topics/",headers=headers)
  printOutput(resq)
  print("test delete")
  resq = requests.get(url+"/delete/"+topic,headers=headers)
  printOutput(resq)
```
## test a backend

```python
import os, sys, gzip, random, csv, json, datetime, re, time
import urllib3, requests, jwt
from requests.auth import HTTPBasicAuth
import requests, base64

url = "http://0.0.0.0:5006"
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
payload = {"id":1,"action":"(name, price) values ('test_product',11.25)","table":"products","filter":""}
usrPass = ""

def printOutput(resq):
  if resq.status_code < 400:
    print(resq.json())
  else:
    print(resq)
    print(resq.reason)
    print(resq.text)

if __name__=="__main__":
  print("test auth")
  b64Val = base64.b64encode(usrPass.encode()).decode()
  resq = requests.get(url+"/authenticate",headers={"Authentication": "%s" % b64Val})
  print(resq.status_code)
  token = resq.json()
  headers["Authentication"] = token
  print("test entry")
  resq = requests.get(url+"/book/page/4",headers=headers)
  printOutput(resq)
  resq = requests.get(url+"/book/page/1",headers=headers)
  printOutput(resq)
  print("test create")
  resq = requests.get(url+"/")
  print(resq.status_code)
  payload = {"id": 1, "action": "*", "table": "products", "filter": ""} 
  payload['action'] = "(name, price) values ('test_product',%f)" % random.uniform(1,30)
  payload['filter'] = ""
  resq = requests.post(url+"/create",json=payload,headers=headers)
  printOutput(resq)
  print("test read products")
  payload = {"id": 1, "action": "*", "table": "products", "filter": ""} 
  resq = requests.post(url+"/select",headers=headers,json=payload)
  printOutput(resq)
  prodL = resq.json()
  print("test sql ingestion")
  payload = {"id": 1, "action": "1; drop products;", "table": "products", "filter": ""} 
  resq = requests.post(url+"/select",headers=headers,json=payload)
  printOutput(resq)  
  print("test delete message")
  resq = requests.delete(url+"/delete/"+payload['table']+"/1",headers=headers)
  for i in prodL:
    resq = requests.delete(url+"/delete/"+payload['table']+"/"+str(i['id']),headers=headers)
    printOutput(resq)

```

## test kafka
```python
import json, datetime, base64, sys, os
from time import sleep
import requests, mailparser
from kafka import KafkaConsumer, KafkaProducer, TopicPartition, KafkaAdminClient

KAFKA_SERVER = "kafka:9093"
topic = "test_topic"
inMex = {
  "content": "base64-encoded message raw content (unparsed)",
  "sender": "sender@example.com",
  "recipients": ["recipient1@gmail.com","recipient2@yahoo.com"],
}
GROUP_ID = "mail-group"

def get_producer():
  return KafkaProducer(bootstrap_servers=[KAFKA_SERVER],api_version=(0,11,15)
                       ,value_serializer=lambda v: json.dumps(v).encode('utf-8'))

def get_consumer():
  return KafkaConsumer(bootstrap_servers=[KAFKA_SERVER],auto_offset_reset='earliest'
                       ,consumer_timeout_ms=1000,group_id=GROUP_ID,api_version=(0,11,15)
                       ,value_deserializer=lambda v: json.loads(v.decode('ascii'))
                       #,key_deserializer=lambda v: json.loads(v.decode('ascii'))
                       ,enable_auto_commit=True)#,auto_commit_interval_ms=1000)

admin_client = KafkaAdminClient(bootstrap_servers=[KAFKA_SERVER],api_version=(0,11,15))
topic = 'unknown'
topic = 'outbound'

consumer = get_consumer()
topicL = list(consumer.topics())
topic_partition = TopicPartition(topic, 0)
consumer.assign([topic_partition])
consumer.seek_to_beginning()
consumer.seek(partition=topic_partition, offset=0)
pos = consumer.position(topic_partition)
resL = []
for msg in consumer:
  resL.append(msg)

print(len(resL))

```

## checks in docker

Docker can test at regular intervals if a service is active 

```
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "api_ingest"]
      interval: 5s
      retries: 5

```
