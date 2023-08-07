# data compliance

Designing an infrastructure implies the fulfilment of general and specific requirements for security, access, data protection, anonymicity, data retention...

# data access

The infrastructure should be design to grant the necessary access to the data and make sure that the infrastructure doesn't violate any data protection law. 
We should first distinguish between:

* **user access**: a human who can see, query, or export data
* **job access**: a routine that parse the data and usually aggregates the output

Users are often not allowed to see any personal-sensitive data (apart from on spot maintenance from dev-ops people who might need to admin the servers, those sessions are time-limited and often recorded).

## sensitive data

There are different categories of data which we can group as:

* **public data**: available on internet, licensed by the emitter
* **personal data**: information about physical persons with different levels of sensitivity
* **synthetic data***: data created by sampling from empirical distributions, useful for development and extended user access
* **sensitive data**: Following gdpr there is an amount of data considered as [sensitive](https://commission.europa.eu/law/law-topic/data-protection/reform/rules-business-and-organisations/legal-grounds-processing-data/sensitive-data/what-personal-data-considered-sensitive_en) [2](https://gdprinformer.com/gdpr-articles/sensitive-data-gdpr-need-know)
* **anonymized data**: A dataset where the sensitive fields are either hashed, masked or deleted


## anonymization

In presence of sensitive data we can act on the database and:

* **hash** the data using an encryption algorythm
* **mask** the data using a dummy value (those data can't be joined)
* **delete** the sensitive fields
* **homomorphic encryption**: the encrypted data has a unique encrypted value (not the case for most of the algorythm)
* **aggregation**: aggregate the personal info in ranges (i.e. 24-35 yo)
* **zero knowledge proof**: purpose specific request for a data range without sharing the exact value

## retention and purpose

Data storage should consider the retention time frame for this kind of data source and the purpose for the storage of data. The retention goes along with purpose, some data producers are obliged to retain data for a certain time period in case of an **audit** or for financial reason.

To data producers and consumers different policies applies, for a **data consumer** without ownership of the data  usually the purpose of the data usage should be clarified before granting the access and a certain retention policy should be put in place. 
A common scenarion for a data consumer is:

* **processing window**: the time to process the granular data (plus few days more as buffer to re-iterate the processing in case of a fault)
* **historical trends**: retention of aggregated reports to compare with trends (year in year)
* **financial data**: data should be retained for billing/cost purposes




