---
title: spiega overview
author: Giovanni Marelli
date: 2019-09-12
rights:  Creative Commons Non-Commercial Share Alike 3.0
language: en-US
id: spiega_overview
category: #tech
roam_refs: spiega_overview
roam_aliases: ["spiega overview"]
output: 
	md_document:
		variant: markdown_strict+backtick_code_blocks+autolink_bare_uris+markdown_github
---

# overview of the spiega blog 

Blog articles and their summaries




# data quality

 Link: [data quality]("../a/data_quality.html")

### Data Quality Report

#### Feature Extraction

**Code:** The feature extraction is done using `etl_feature.py`. Data is stored in Athena. Relevant tables are `telemetry`, `network_log`, `session`, and `incident`.

- **Environments:** Only the `prod` environment contains complete data.

- **Telemetry Table:**
  - Contains sensor data, board usage, and predictions.
  - Features include `mean_km_per_hour`, `lateral_force_m_per_sec_squared`, etc.
  
#### Data Ingestion

**Sources:**
- Various sources populate the `telemetry` table.
- Different ROS topics collect data at varying rates.

**Visualization:**
- Telemetry data is irregular and unregularly ingested. The heatmap shows firing behavior of different sources.
- Features like `e2e_latency`, `camera_latency`, and `joystick_latency` are analyzed.

**Ingestion Delay:**
- Clear delay between topic publication and Kinesis processing, around 5 seconds on average.

#### Ingestion Stream

**Data Source:** `proc_telemetry`.
- Irregular data flow leading to fluctuating values due to time buckets.
- Data is resampled and filled with running averages to improve consistency.

#### Data Extraction

**Tools:**
- Athena for initial queries, but Spark is preferred for a more careful workflow.
  
**Athena Limitations:**
- Can't handle `null` in averages and can return NaN values as 0.
- No user-defined functions or libraries.

**Avoiding Fake Zeros:** Arithmetic operations are avoided to prevent fake zeros.

#### Network Log Data

**Query:** [network_log.sql].
**Code:** `stat_network.py`.

- **Features Analysis:**
  - Many empty values in the time series features.
  - Distributions are narrow with outliers.
  - Correlation analysis shows some features can be neglected.
  - Multi-modal distributions indicate redundancy.

- **Joining Tables:**
  - Joining `telemetry` and `network_log` introduces more noise.

#### Modem Data

**Source:** `etl_telemetry_deci`.
**Query:** [resample_deci.sql].

- **Time Series Analysis:**
  - Correlation between modem features shows redundancy.
  - Interpolation on deci seconds creates many artefacts.
  
- **Feature Correlation:**
  - Most features are multimodal, and `sinr` and `rssi` are the richest.

#### Camera Index

**Analysis:** Cameras exhibit similar latency during spikes, suggesting dependency on a shared condition.

#### Session Time

**Correlation Analysis:**
- Some quantities like RAM depend on session time.
- RAM steadily grows over session time but never reaches critical levels.
- Session time doesn't significantly influence spike occurrences.

### Summary
The report highlights various aspects of data quality, including irregular ingestion patterns, noise introduced by joining tables, and redundancy in certain features. Athena's limitations and Spark's advantages are discussed for efficient data handling and analysis. The report also provides insights into the correlation between session time and other features, suggesting a need for more comprehensive understanding of session behavior.

# antani kpi

 Link: [antani kpi]("../a/antani_kpi.html")

The document is titled "optimization engine comparison" and provides an overview of comparing two different optimization engines. It describes a setup with 600 spots, 6 task types, and an 8-driver fleet. The first section compares the routific API service solution to a visualization using Routific Viewer. 

The second section discusses running the optimization engine from a blank system or after a routific solution. When starting from a routific solution, the optimization engine improves big springs. It then introduces the KPIs: `completion`, `duration`, `potential`, and `distance`. The score is calculated using these KPIs.

Finally, it compares the run time of the two engines. Routific sends a complete solution within 3 minutes, while the optimization engine takes 30 minutes to find a better solution. To improve performance, new moves were introduced.

# llm governance

 Link: [llm governance]("../a/llm_governance.html")

The document "LLM governance" outlines the principles of effective governance for Large Language Models (LLMs). Key components include:

1. **Agentic Workflow**: Shifts focus from operational execution to monitoring and managing agent activities.
2. **Ownership and Traceability**: Clearly defines who owns each component of the system, ensuring decisions are reproducible and traceable.
3. **Metrics and KPIs**: Establishes metrics and key performance indicators (KPIs) for various areas:
   - Backend: Cost and performance control
   - Fitness: Alignment with goals
   - Goodness: Model performances, edge cases, data drifts, and model evaluations
   - Business: Overall system performance and value delivery
4. **Guidelines**: Implements guidelines to ensure consistency across all components.
5. **Stakeholder Monitoring**: Defines areas for monitoring to control the status and success of the system.

The document also provides examples of how to define metrics and export content using Org mode, including:

- A table with lines around cells
- An example flowchart representing data governance responsibilities
- An ELisp function demonstrating an XOR operation
- A Bash script for configuration purposes

Overall, the document aims to provide a structured framework for managing LLMs effectively.

# customer lifetime

 Link: [customer lifetime]("../a/customer_lifetime.html")

The given Markdown file `customer_lifetime.md` appears to be an overview or summary of different aspects related to customer lifecycle management. Here is a structured summary:

## Customer Lifetime

- **Overview**: This section likely provides an introduction or introduction to the concept of customer lifetime in business, which refers to the total period during which a customer interacts with a company.

## Value

- **Explanation**: This portion might discuss the value proposition for customers over their entire interaction with the company. It could cover how the company delivers benefits and experiences that create long-term loyalty or satisfaction.

## Lifetime

- **Definition**: The lifetime section might define "lifetime" in the context of customer engagement, which refers to the total period a customer is considered active or valuable to the company before they may no longer be interested or profitable.

## Churn

- **Exploration**: This part could delve into churn rates, their causes, and strategies for reducing them. Churn typically refers to the loss of customers over time, which can have significant financial implications for companies.

### Additional Considerations:

1. **Customer Acquisition Cost (CAC)**: The document might touch on how businesses calculate CAC and its impact on profitability.
2. **Customer Retention Strategies**: It could discuss various methods and techniques used to retain existing customers, including cross-selling, upselling, and personalized marketing efforts.
3. **Customer Lifecycle Metrics**: Specific metrics related to customer lifecycle management could be mentioned, such as conversion rates, retention rates, and average order value (AOV).

Overall, this summary provides a high-level overview of customer lifecycle concepts, focusing on their value, longevity, and strategies for managing churn effectively.

# geomadi graph

 Link: [geomadi graph]("../a/geomadi_graph.html")

The document discusses various aspects of building and analyzing a graph for routing purposes. Here's a summary:

1. **Graph Construction**:
   - Downloaded the street network from OpenStreetMap.
   - Included detailed information such as different road types (e.g., motorway, primary).
   - Simplified the graph by reducing the number of edges while maintaining distances.
   - Selected only routable street classes and took the largest connected subgraph.
   - Projected the graph onto a lower dimension for more manageable calculations.

2. **Weighting the Graph**:
   - Applied weights to each edge based on factors like speed, street class, and length.
   - Used a formula to calculate the weight: \(\frac{speed \times type}{length}\).
   - This weighted graph helps in determining efficient routes.

3. **Calculating Distance Matrices**:
   - Determined the closest node for each spot using various routing algorithms like Dijkstra's or A*.
   - Compared different graphs and their distances to identify optimal routes.

4. **Graph Analysis**:
   - Analyzed graphs based on different factors like digit used (9, 10, 13) to understand distortion and connectivity.
   - Recognized that some parts of the graph were disconnected and took the largest connected subgraph to improve route efficiency.
   - Compared the symmetry matrices of different graphs to identify asymmetries.

5. **Optimization**:
   - Switched from a directed graph to an undirected one for reasonable routing, as a directed graph can be too complex.
   - Used Markov chains to analyze changes in weights and optimize routes further.

Overall, the document provides insights into various techniques used for building and analyzing graphs for efficient routing applications.

# commercial

 Link: [commercial]("../a/commercial.html")

### Summary of Commercial.md

The document discusses data collection and analysis for commercial activities:

1. **Event Collection**:
   - User events are collected with IMSI (hashed SIM card), event time and cell information.
   - Events are categorized into chains based on the same IMSI.
   - Handovers between cells within the same device are tracked.

2. **Activity and Trip Definitions**:
   - Activities are defined as clusters of continuous events within a space.
   - Trips are sequences connecting two activities.

3. **Geometry Usage**:
   - Geometry files (ags5, ags8, mtc, zip) for zone and time mappings are provided and can be downloaded.
   - Zone mapping involves calculating the intersection of zones with cell BSE polygons to determine activity areas.
   - Time mapping categorizes activities by hour of the day.

4. **Statistical Week**:
   - The statistical week is a collection of holiday-free days grouped by weekday type.
   - A consistency check visualizes data, showing patterns like high footfall in urban centers on workdays.

5. **Origin-Destination Matrix (ODM)**:
   - An ODM represents origin-destination relationships based on all trips.
   - Patterns in people's behavior are compared with different statistics, such as Munich suburbs' commute patterns to work.

6. **Footfall Analysis**:
   - Footfalls are calculated by counting non-unique trajectories crossing tiles.
   - Nodes and ways are identified using OpenStreetMap data and Overpass queries.
   - Trajectories are routed to calculate the best trip, avoiding detours with neighboring events.
   - Footfall information is collected per tile and applied to a study geometry.

7. **API Documentation**:
   - Data can be accessed via API with usual headers and credentials.
   - The API supports various endpoints for location information, reports, and geometries.
   - Examples of data retrieval and processing are provided for collecting available dates and specific location details.

# phonosymbolic

 Link: [phonosymbolic]("../a/phonosymbolic.html")

This document is an outline for creating a phonosymbolic language that uses sounds as symbols to convey meaning rather than direct translations. It describes the alphabet, font, embedding and clustering processes, and output system to create a machine translation utility from Italian into this new language. The final goal is to have native speakers report their perception of the language through exposure.

# antani integration

 Link: [antani integration]("../a/antani_integration.html")

### Antani: Agent/Network Intelligence Framework

Antani is an agent-based network intelligence framework designed for optimizing fleet operations. The system is structured to manage operations through a combination of user-controlled and automated modules.

#### Workflow Overview

1. **User Control and Automation**: The optimization engine includes both manual and automated components.
2. **Data Retrieval**: Information is collected directly from the fleet console microservices using API calls.
3. **Fleet Engine**: This component orchestrates all operations, tracking and monitoring their status. It defines four objects with an hierarchical structure to manage objectives efficiently.

#### Objectives and Metrics

- The optimization engine focuses on calculating profitability for each drive and iterating over possible solutions.
- Each "drive" is evaluated for cost and rating, while each "task" is analyzed for revenue and risk.

#### Design Considerations

To enhance parallel processing capabilities:

1. **Current Graph Design**: Initially, the system uses a graph design for operations.
2. **Suggested Linear Design**: This design simplifies orchestration by managing calls through cached tables that can replace broken services.
3. **Separation of Concerns**: The framework distinguishes between field operation and task optimization, enhancing modularity.

![Engine Design Current](../../f/f_ops/engine_design_old.svg)
**Engine Design (Current Scheme)**

![Engine Design Proposed](../../f/f_ops/engine_design.svg)
**Engine Design (Proposed Scheme)**

![Infrastructure Design](../../f/f_ops/infra_design.svg)
**Infrastructure Design**

### Summary
Antani is a comprehensive framework that leverages agent-based logic for optimizing fleet operations. It includes user-controlled and automated modules, data retrieval from microservices, and an efficient design for handling parallel processing tasks.

# portfolio creation

 Link: [portfolio creation]("../a/portfolio_creation.html")

To create a portfolio, this person has developed an agentic approach to collecting and evaluating information for job applications. They maintain a structured knowledge base containing blog posts (100+ files), source codes (3k3+), images (1k5), resume (resume.yml), project descriptions (portfolio projects.yaml), skills (skills.yml), and personal profile (personal_profile.yml).

To interact with local models and file system, they have created a library (`model_local.py`) and deployed it using `mcp server` on Docker. This integration allows them to run LLMs within Emacs for code generation.

The portfolio creation process involves summarizing blog posts and saving the results as a CSV file. The person also uses the `graph_rag.py` function to create graphs from the data, which includes information like citations, maximum cites, and H-index.

This approach combines manual research with automated processing to ensure that their portfolio is comprehensive and well-organized.

# programming praxis

 Link: [programming praxis]("../a/programming_praxis.html")

The provided document outlines several key programming practices and guidelines that aim to improve software reliability, ease of use, configuration management, function organization, definitions, and collaboration among developers. It also covers the software life cycle, infrastructure considerations, UI/UX design, observability, batch processing, documentation, AI platforms, Large Language Models (LLMs), and versioning strategies.

### Key Practices:

1. **Reliability**: Each project has a `/test` folder for scripts that run tests both during development and production.
2. **Ease**: The code is minimal and easy to browse. Classes are specific, and abstraction is discouraged. Repositories should have an `/example` folder with data loading and function execution.
3. **Configuration**: A master JSON file is used as the source of truth for all configurations, including environment, preprocessing, loading, input/output, stages, and a 'run' key logging important activities during runs.
4. **Functions**: Functions are organized per scope and dependencies, avoiding interdependencies between libraries. The main application should call modules without moving too much between libraries.
5. **Definitions**: No global definitions apart from what is inside the configuration file and environment variables. Special attention is given to async and callback functions.

### Software Life Cycle:

- **Code Review**: Peer review or approval processes are in place.
- **Pipeline**: Scripts for pushing code, testing configurations, deploying on a dev server, and testing deployments are used.
- **Libraries**: Important functions should compose libraries for general usage.

### Infrastructure Considerations:

- **Authentication**: Access to web apps, backend services, database entries, file storage, etc., is controlled.
- **Security**: Access rights and standards are defined.
- **Speed**: Services are checked for fast response times.
- **Scalability**: The infrastructure should scale with user usage and data size.
- **Protocols**: Applications interact using standardized protocols.
- **Storage**: Retention policies ensure speed, reliability, and redundancy. File systems, databases, and stream data are selected appropriately.

### UI/UX:

- **Speed**: Response times are checked to be practical.
- **Errors**: Broken links, typos, and wrong visualizations are addressed.
- **Support**: Users can get assistance in case of errors or malfunctions.
- **Features**: The results are as expected.
- **Expansion**: App expansion is easy.

### Observability:

- Important transactions are logged and visualized using BI tools.
- Requests are tracked, metrics are stored for quality checks, and notifications are set up for bad performances.

### Batch Processing:

- Processes initiated by triggers or time schedules perform background operations with minimal user traffic.
- Scheduling frequencies and notification processes are checked.

### Documentation:

- Developers should find proper information regarding APIs.
- DevOps should know how to deploy the solution.
- End users should understand main functions and contact support in case of issues.

### AI Platform:

- Data accessibility is ensured, and sensitive data is pre-filtered or anonymized.
- Data aggregation allows quick access by processing granular data efficiently. Consistency checks and versioning mechanisms are implemented for reliability.
- Ethical considerations and ML output monitoring are emphasized.

### Large Language Models (LLMs):

- Prompt definitions and retrieval mechanisms ensure coherent answers.
- Model parameters and costs are configured correctly, and model selection is efficient.
- Document preprocessing and batch processing support faster and more consistent retrieval.
- LLM outputs are evaluated and monitored for consistency.

### Collaborative Programming:

- Clarity and readability are emphasized, and testing, debugging, scalability, and modularity are addressed.
- Libraries and classes are organized to ensure reusability and maintainability.

### Versioning:

- Version control is used to manage changes effectively.

### Environment Management:

- **Virtual Environments**: Used for managing library versions, especially in containerized environments.
- **.env**: For storing environment variables securely.
- **Export Variables**: Properly exporting environment variables for use across the system.

### Documentation:

- Comprehensive documentation ensures software longevity, including user guides and developer resources.

Overall, this document provides a structured approach to ensuring robust, maintainable, and scalable software development practices, which aligns with contemporary programming standards.

# antani overview

 Link: [antani overview]("../a/antani_overview.html")

The Antani project is an agent/network-based optimization engine designed to efficiently assign tasks to operators in field operations. It aims to provide better performance and reliability compared to commercial software by implementing a mix of simulation and reinforcement learning techniques.

Key features include:

1. **Task Assignment**: The engine considers task priorities and shift constraints to assign tasks to the most eligible operator.
2. **Fine-Tuning**: Users can interact with the optimization engine, pause, resume simulations, and assess solutions based on KPIs before waiting for timeouts.
3. **Simulation and Reinforcement Learning**: It uses simulation and reinforcement learning to find optimal moves during task assignments.
4. **Graph-Based Approach**: The engine creates a graph connecting tasks and ants move across network edges to find the most convenient solution.
5. **Data-Driven Optimization**: By calculating transition probabilities using Bayesian inference on real data, the system provides more reliable estimates.

The project is designed to handle multiple parallel calls and has been tested with various companies such as Flixbus, Amazon, Bliq, Ridesos, MOIA, and WeShare. It addresses issues related to last-mile delivery inefficiencies by leveraging crowd-based solutions.

The technical components of the project include:

1. **Graph Building**: Retrieving a network, building and fixing graphs.
2. **Markov Chains**: Using Markov chains for moving between spots based on graph connections.
3. **Posterior Probability**: Calculating more reliable estimates of transition probabilities using Bayesian inference.
4. **Backend Design**: A series of microservices with backup solutions or cached information to ensure operativity.
5. **Frontend**: Provides a web-based solution and a video explaining its functioning.

Overall, Antani is an advanced optimization engine designed to improve the efficiency of field operations by leveraging simulation, reinforcement learning, and graph theory.

# skills

 Link: [skills]("../a/skills.html")

The document "skills.md" from the directory contains a list of skills and technologies gained over different years. Here's a summary:

### Skills Overview

- **Years**: From 2014 to 2023
- **Skills**: 
  - R (2014)
  - Hadoop (2014)
  - Sklearn (2015), Hyperparameter tuning, Computer Vision, Natural Language Processing (NLP) (2015)
  - IoT, Autonomous Drive, GIS (2016)
  - AWS, Deep Learning, DevOps (2017)
  - SRE/DE, Jenkins (2018)
  - MLops, Terraform, Generative Adversarial Networks (GAN) (2019)
  - NFT, Web3, Solidity (2020)
  - Metaverse, Generative, Transformers (2021)
  - Large Language Model (LLM), Fine-tuning, Embeddings (2022)
  - LLM Prompting, Snowflake, dbt (2023)

This document provides a chronological overview of the skills and technologies acquired by the individual over several years.

# activation

 Link: [activation]("../a/activation.html")

This document discusses the activation probability of scooters in a given area. The activation probability is defined as the probability of picking the n-th scooter in a given time frame. The authors estimate this parameter for each zone using a proper distribution.

The authors define a function `sumProb` to calculate the cumulative probability of used scooters in an area for a given time frame. They then use a Fermi-Dirac distribution to fit the empirical distributions of activation probabilities and compute the chemical potential.

The authors visualize the areas with the most revenue, where the scooters were deployed, and how many scooters should be deployed in each area. The chemical potential is used to determine this number.

The authors also calculate the potential revenue per location, weekday, and shift, and display the results on a map. They iteratively group by different zooms of geohash to have an estimate in areas where they don't have an accurate measurement of the activation probabilty.

Finally, they calculate the error of the model per zone and obtain a median error of 18%.

# ride

 Link: [ride]("../a/ride.html")

The document "rides" describes various aggregations and visualizations related to scooter usage data. The main focus is on summarizing ride information, clustering user behaviors, analyzing rides over time, calculating geographical statistics, and monitoring customer movements.

### Key Points:

1. **Daily Aggregation:**
   - Organizes time-varying information into a matrix called `tx`.
   - Summarizes dynamic quantities in columns such as `mileage`, `n` (number of steps), and `state`.

2. **Ride Analysis:**
   - Groups rides by timestamp, bounding box, length, energy consumption, cost, zone ID, and firmware.
   - Visualizes ride paths on a map (`ride_map`) and monitoring details (`ride_monitoring`).

3. **Geographical Statistics:**
   - Summarizes rides per geohash (`ride_geohash`).
   - Calculates the origin/destination matrix (`odm_matrix`).

4. **Simplified Graph of Customer Movements:**
   - Visualizes customer movements on a graph (`graph_customer`).

5. **Hardware API:**
   - Contains information about hardware communication and updates every connection.

6. **Scooter Data:**
   - Provides statistics for each scooter, including idle time, total revenue, bounding box, number of rides, firmware version, zone ID, mileage, number of turns, and number of deployments.

7. **Customer Data:**
   - Counts the number of rides, operation area, and revenue for each customer during the day.

8. **Job Script:**
   - Uses PyArrow to read Parquet files from S3, remove unnecessary columns, and save them as a CSV file with gzip compression.

9. **Spark Configuration and Setup:**
   - Sets up SparkContext and SQLContext configurations.
   - Defines data structures and user-defined functions (UDFs) for processing data efficiently.

10. **Visualization:**
    - Generates boxplots for revenue distributions (`rev_boxplot`).

### Summary:
The document provides a comprehensive overview of ride data aggregations, visualizations, and their underlying processing steps using Spark and PyArrow. The focus is on extracting valuable insights into scooter usage patterns and customer behavior.

# data storage

 Link: [data storage]("../a/data_storage.html")

The document provides a comprehensive guide on various types of databases and their usage in data infrastructure projects. It includes detailed information on PostgreSQL, MariaDB, Presto, MongoDB, Neo4j, and vector embeddings. The document is structured with headings for each topic and provides examples and code snippets to help readers understand how to set up and use these tools effectively.

# music composition

 Link: [music composition]("../a/music_composition.html")

# Generative Music Composition

## Introduction

A bot capable of generating melodies and basslines can be beneficial for music composition. A generative model requires a consistent, clean dataset to learn patterns.

### Output Specification

The output of this project should be a tiny model suitable for embedding on an embedded device to generate MIDI files.

## Dataset

To train such a bot, I start with a collection of songs from my repository [viudi.it](https://viudi.it/article/music_composition.html). The dataset includes 21 MIDI files written using Lilypond markup language. Below is an example of one of the generated MIDI files:

![flutto_note](../../f/f_gen/flutto.png "Flut note")

### Data Set

This data set consists of harmonies, piano leads, and basslines. An example song is shown below:

![flutto_note](../../f/f_gen/music_dataset.png "flutto note")

## Tokenization

We decide to use explicit notation instead of the compact one. This approach helps in making the learning process easier by clearly defining chord structures.

### Chord Notation

The tokenization includes specific attributes such as pitch, position, duration, and velocity for notes, and scale, mode, grades, and duration for chords.

```python
def order_chord(chordL, stem_octave=False):
    if stem_octave:
        replace = {",,":"",",":"","'":"","''":""}
        rem_octave = re.compile("(%s)" % "|".join(map(re.escape, replace.keys())))
        chordL = [rem_octave.sub(lambda mo: replace[mo.group()], x) for x in chordL]
    try:
        pL = [NOTES.index(x) for x in chordL]
    except:
        pL = list(range(len(chordL)))
    return np.argsort(pL)
```

### Embedding and Vectorization

We use a language-like representation to divide the dataset into bars. We then create a 100-token vocabulary size, with notes having fewer attributes than chords.

```python
n = ['do','dod','re','mib','mi','fa','fad','sol','lab','la','sib','si']
c = {"M":[0,4,7],"m":[0,3,7],"sus":[0,5,7],"dim":[0,3,6],"m7":[0,3,7,9]}
```

### Chord Deduplication and Scale Mapping

We deduplicate chords to reduce the number of unique chords. We also map chords to scales for better understanding:

```python
def iterate_chords():
    l = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
    n = ['do','dod','re','mib','mi','fa','fad','sol','lab','la','sib','si']
    n2 = n + n + n
    c = {"M":[0,4,7],"m":[0,3,7],"sus":[0,5,7],"dim":[0,4,6],"m7":[0,3,7,9]}
    m = list(c.keys())
    s = {}
    for i, l1 in enumerate(l):
        for m1 in m:
            k = l1 + m1
            l2 = l.index(l1)
            c1 = "-".join([n2[x + l2] for x in c[m1]])
            s[k] = c1
	return s, s1

chords, chords_scale = iterate_chords()
```

## Model

The model is designed to generate sequences based on the learned patterns from the dataset.

### Results

After training the model for 100 epochs and a few minutes of time, the loss is 0.1 and accuracy is 0.95.

## Generating Music

We use Markov chains to generate series of chords based on authors' preferences:

![markov_bach](../../f/f_gen/markov_bach.png "Markov Bach")

### Example Chord Sequence

Here's an example sequence of chords starting with `G`/`E:m`:

```
['la-re-fad', 'la-do-mi', 'la-do-fad', 'la-do-mi', 'sol-si-re', 'la-re-fad', 'sol-do-mi', 'sol-do-mi', 'la-re-fad',...]
```

### Initial Generation Results

The first generation results are overfitted:

```
<<mi1 si sol>>  -> sol16 mi16 si16 do16 mi16 re16 do16 si16 do16 si16 la16 sol8 mi8 la16 
<<fad1 la re>>  -> sol16 mi16 si16 do16 mi16 re16 do16 si16 do16 si16 la16 sol8 mi8 la16 
<<re1 si sol>>  -> sol16 mi16 si16 do16 mi16 re16 do16 si16 do16 si16 la16 sol8 mi8 la16 
```

### Model Refinement

We refine the model by reducing its parameters and using a minimal set:

```python
       ,"vocab_size":100,"sequence_length":20,"batch_size":64
       ,"embed_dim":6,"latent_dim":6,"num_heads":8
```

### Improved Generated Music

The refined model produces more interesting music:

![generated_music](../../f/f_gen/mus_generated.png "generated music")

### Example MIDI File

Here is an example MIDI file with some interesting ideas but sometimes falling in loops and missing the key:

<midi-player src="../../f/f_gen/gen1.midi" sound-font></midi-player>

## License

[CC by-sa-nc](https://creativecommons.org/licenses/by-nc-sa/4.0/)

# nodejs

 Link: [nodejs]("../a/nodejs.html")

### Overview of Node.js Applications in Directory

This document outlines several applications developed using Node.js, along with details on each application's functionality and technical implementation.

#### 1. **Geocode**
- **Description**: An app for anonymizing addresses by parsing them line by line using a geocoding service.
- **Features**:
  - Takes a list of addresses.
  - Parses addresses and applies anonymization, such as removing digits from coordinates or using geohashes.
- **Implementation**:
  - Uses asynchronous JavaScript with Promises to handle sequential operations on address parsing and geocoding.

#### 2. **Text Corrector**
- **Description**: An automated tool to assist writing sales emails by suggesting corrections based on user input.
- **Features**:
  - A text editor where users can draft an email in different sections (subject, greeting, presentation, etc.).
  - Continuously evaluates changes and applies suggestions from a language model.
  - Provides options for editing prompts and sending requests to the language model.
- **Implementation**:
  - Built with Node.js using Express and EJS.
  - Main functions are implemented in JavaScript on both the frontend and backend.

#### Deployment Instructions
- **Environment Setup**: Create an `.env` file and set the `OPENAI_KEY`.
- **Running Locally**: Use `npm install`, followed by `npm start` or navigate to the build directory with Docker, using `docker-compose up -d`.
- **Access**: The applications are accessible at `localhost:3000/correct`.

These applications showcase different aspects of Node.js development, including asynchronous programming, frontend-backend separation, and integration with external services like geocoding APIs and language models.

# lernia

 Link: [lernia]("../a/lernia.html")

**Lernia Library Description**

*Lernia* is a machine learning library designed for automated learning on geospatial and time series data. It provides various modules to handle data pre-processing, feature engineering, and model training.

### Modules Descriptions

#### Time Series Module
- **`series_load.py`:** Loads and preprocesses time series from web services.
- **`series_stat.py`:** Performs statistical properties analysis and filtering of time series.
- **`series_forecast.py`:** Implements forecast models such as ARIMA, Holt-Winters, and Bayesian methods.
- **`series_neural.py`:** Forecasting using neural networks.
- **`algo_holtwinters.py`:** Implementation of the Holt-Winters algorithm.

#### Computing Module
- **`calc_finiteDiff.py`:** Implements finite difference for solving differential equations.
- **`kernel_list.py`:** Contains a collection of kernels.

#### Geographical Module
- **`geo_enrich.py`:** Enriches location data with geographical information.
- **`geo_geohash.py`:** Computes geohashes for locations.
- **`geo_octree.py`:** Provides octree algebra based on coordinates.

#### Basics Module
- **`lib_graph.py`:** Styles for graphs.
- **`proc_lib.py`:** Utilties for Spark processing.
- **`proc_text.py`:** Text preprocessing and quantification.

#### Learning Module
- **`train_reshape.py`:** Tools to reshape data prior/post-training.
- **`train_shape.py`:** Reduces curves shapes into metrics suitable for training.
- **`train_feature.py`:** Utilites for feature statistics, elimination, and importance.
- **`train_interp.py`:** Interpolation techniques for smoothing data.
- **`train_score.py`:** Scoring utilities for performance.
- **`train_metric.py`:** Important metrics for scoring and performance.
- **`train_viz.py`:** Visualization tools for performances and data statistics.
- **`train_modelList.py`:** Collection of sklearn models for comparison.
- **`train_model.py`:** Iteration and tuning on sklearn models.
- **`train_keras.py`:** Parent class for training with Keras.
- **`train_deep.py`:** Deep learning models for regression and predictions.
- **`train_longShort.py`:** Long Short-Term Memory (LSTM) models for time series prediction.
- **`train_convNet.py`:** Convolutional Neural Networks for predicting small images.
- **`train_execute.py`:** Execution of learning libraries based on custom problems.

### Data Structure

Every time series is represented as a matrix, where each row corresponds to an hour in a day and each column represents the count at that hour.

### ShapeLib

**`shapeLib.py`:**
```python
redF = t_s.reduceFeature(X)
redF.interpMissing()
redF.fit(how="poly")
redF.smooth(width=3, steps=7)
dayN = redF.replaceOffChi(sact['id_clust'], threshold=0.03, dayL=sact['day'])
dayN[dayN['count']>30].to_csv(baseDir + "raw/tank/poi_anomaly_"+i+".csv", index=False)
XL[i] = redF.getMatrix()
```

#### Replace Missing
- Data is homogenized and missing values are replaced via interpolation.

#### Smoothing
- Polynomial interpolation and smoothing are applied to reduce time shifts in the data.

#### Chi-Square Distribution
- $\chi^2$ tests are performed on location-specific time series to identify volatile locations.
- Outliers are replaced with an average day for those locations.

#### Feature Importance
- Statistical properties are studied, and a ranking of features is derived based on importance for model performance.

### Regression

**Regression Models:**
- Various skew metrics (e.g., auto_decay, noise_decay) are used to train models that adjust counts.
- The ROC curves illustrate the performance of different regression models.

#### Scoring
- A scoring system using Pearson's r and ridge regression is implemented to evaluate model performances.
- The absolute difference score measures how well predicted values match reference data per location.

### Shape Clustering

**Shape Clustering:**
- Different patterns for user clustering are recognized through feature extraction and interpolation of time series.
- Characteristics like intercept, slope, convexity, and trend are calculated to cluster curves.

### Feature Selection
- A correlation matrix helps identify strongly correlated features.
- Five features with the highest variance are selected to increase training cases.

### Deep Learning Autoencoder

**Autoencoders:**
- Convolutional autoencoders are used to create encodings from sets of images, representing hourly counts per week.
- They help detect problematic locations and morph measured data into reference data.
- The model is trained with convolution layers, and the results show that **88% of locations** have poor prediction within 0.6 correlation.

### Results Generation
**Predictor and Regressor:**
- Activities are generated by applying both predictor and regressor models to time series data.
- Results are sorted based on a $\chi^2$ probability, discarding high `p_value` results.
- The detailed flowchart of the project using Node-RED is provided for reference.

### Flow Chart
![Flow Chart](../../f/f_mot/test_flow.png "Project Flow Chart")

**Structure:**
- The analysis is structured to deliver yearly delivery calculations based on various models and parameters.

# video presentation 1

 Link: [video presentation 1]("../a/video_presentation_1.html")

This document is a presentation about an electronic music video titled "Electro Jam with Aira P-6" from the show "Tornate per ultimi". The video features atmospheric electro jamming sessions that take place in different settings, including Austrian and Italian fronts. The video was captured using the Roland Aira P-6 as well as other equipment such as a Zoom G1 Four, Sony Alpha, Insta360 camera, Novation Circuit, and electronic violin. The performance includes vocals from Francesca Tidoni. The presentation provides details about the episode, timeline, moments, tags, keywords, meta-information, and footer for the video.

# music entropy

 Link: [music entropy]("../a/music_entropy.html")

### Entropy as Measure for Creativity

#### Metrics Calculation

- **Song Rhythm**: Represents the information content in the timing patterns of the notes.
- **Chromatic Information**: Refers to the distribution of pitches within a song.
- **Total Entropy**: Combines both rhythmic and chromatic information.

For each MIDI file, the histograms are created for:
- Each note duration
- Pitch

The distances between songs are calculated using the formula:
\[ d_{ij}^2 = (E_i^r - E_j^r)^2 + (E_i^c - E_j^c)^2 + (E_i^t - E_j^t)^2 \]

#### Graph Construction

Songs with a distance less than 0.5 are connected in a Neo4j graph.

### Data and Results

|Song |Rhythmic Entropy|Chromatic Entropy|Total Entropy|
|-    |-              |-             |-            |
|Flutto|2.024         |5.239          |6.56        |

#### Distance Between Songs

![distance songs](../../f/f_viudi/DistCanzoni.png)

#### Evolution of Entropy

![entropy evolution](../../f/f_viudi/EntropyEvolution.png)

### Analysis

- **Connections in the Graph**: The graph shows clear connections between Bach's Ciaccone, Lazy Bird of Coltrane, and Vitali Ciaccone.
- **Evolution Pattern**: The entropy generally decreases over time for many songs, indicating a stabilizing process.

The document highlights how the creation of music can be measured using entropy, showcasing that some pieces have more distinct characteristics in terms of rhythm, chromatics, or both.

# spark

 Link: [spark]("../a/spark.html")

### Overview

The document "spark.md" contains multiple Python scripts designed for various purposes related to data processing, machine learning, geospatial analysis, and image generation. Each script serves a specific function within the context of these applications.

#### Data Processing and Machine Learning Scripts

1. **proc_freq.py**: Processes GPS trajectory data to calculate unique users, total events, and average events per user for each day.
2. **train_linear.py**: Trains a linear regression model using the Cal_Housing dataset with Spark MLlib.
3. **etl_tankRef.py**: Reads and processes reference curve data from log files, generating daily and hourly reference values.

These scripts typically involve reading and processing large datasets, performing statistical calculations, and applying machine learning models to extract insights or predict outcomes based on the data.

#### Geospatial Analysis Scripts

1. **proc_cronon.py**: Processes trajectory data using Apache Spark.
2. **proc_traj.py**: Processes GPS trajectory data to compute motion vectors, velocity quivers, and clustering ratios for each segment of a trajectory file.
3. **test_etl_matrix.py**: Performs ETL operations on structured data using Apache Spark.

These scripts focus on geospatial analysis, including trajectory processing, spatial data manipulation, and visualization using geospatial libraries like GeoPandas and Shapely.

#### Image Generation Scripts

1. **gan_train_aws.py**: Trains various types of Generative Adversarial Networks (GANs) on AWS using Keras and TensorFlow.
2. **gan_train.py**: Another script for training GANs, possibly focusing on different domains or configurations.
3. **gan_deploy.py**: Deploys trained GAN models as endpoints on Amazon SageMaker.

These scripts involve complex machine learning tasks such as image generation, model training, and deployment in cloud environments like AWS.

#### Miscellaneous Scripts

1. **proc_demoData.py**: Processes data from a specified directory using Apache Spark.
2. **train_aws.py**: Another script for training GANs on AWS.
3. **etl_tank.py**: Contains functions for processing GPS trajectory data.

These scripts can be used for various purposes such as data processing, model training, and deployment, with each script addressing a specific aspect of these tasks.

### Summary

Each script in this document is designed to perform different functions related to data processing, machine learning, geospatial analysis, and image generation. These scripts are typically part of larger applications or workflows that require handling large datasets, applying complex algorithms, and integrating with cloud services like AWS for scalability and performance. The use of libraries such as Apache Spark, TensorFlow, Pandas, and GeoPandas ensures robustness and efficiency in processing the data.

### Python Script: PyKafka Integration

This Python script is designed to interact with Apache Kafka using PyKafka, a Python client for producing and consuming messages from Kafka topics. The main components and functions include:

1. **Importing Libraries**:
   - `from kafka import KafkaProducer` is used to create a producer instance for sending messages.
   - `from kafka.errors import KafkaError` is used for handling exceptions related to Kafka operations.

2. **Kafka Producer Configuration**:
   - The script sets up the producer by specifying the Kafka broker address (`brokers`) and any additional configurations like key serialization (`key_serializer`), value serialization (`value_serializer`), and batch size (`batch_size`).

3. **Producer Initialization**:
   - A `kafka_producer` is initialized with the configuration settings defined in step 2.
   - The producer can now be used to send messages to a Kafka topic.

4. **Sending Messages**:
   - The script includes a function named `send_message` that takes three parameters: the message content, the key for serialization (optional), and the topic name.
   - Inside the `send_message` function, the producer is used to send the message to the specified topic with optional key serialization.

5. **Error Handling**:
   - The script handles potential exceptions that might occur during message sending using a try-except block within the `send_message` function.
   - If an error occurs, it prints an error message and logs the exception details for debugging purposes.

6. **Example Usage**:
   - There is an example usage of the `send_message` function in the main part of the script to demonstrate sending a sample message to a Kafka topic named "test_topic".
   - The script also includes print statements to show the status of the message sending operation and the response from the producer.

7. **Cleanup**:
   - After sending messages, it is good practice to close the producer when done using `kafka_producer.close()`, but in this example, it is not explicitly shown as the script exits after completing the example usage.

Overall, this script provides a simple and effective way to integrate Kafka into Python applications for real-time data processing and message passing. The use of PyKafka simplifies the process by providing a high-level API for interacting with Kafka brokers.

# midi player

 Link: [midi player]("../a/midi_player.html")

**Title:** Motion

**Author:** Giovanni Marelli

**Date:** July 2, 2019

**License:** Creative Commons Non-Commercial Share Alike 3.0

**Language:** English (United States)

**Output Format:**
- Markdown document with strict syntax, backtick code blocks, autolinked bare URLs, and GitHub markdown features.

This summary provides key metadata about the `midi_player.md` document located in the specified directory.

# app

 Link: [app]("../a/app.html")

### Introduction to the Project Directory (`app.md`)

**Project Directory:** This document contains a comprehensive overview of various projects and applications developed by an organization, focusing on three main technologies: Java, Cordova, and Angular. Each section details specific projects completed within each technology domain.

### Java Projects

1. **Android Connect SQL - 2013**
   - Description: An Android application designed to interact with a SQL database.
   - Visual Representation: ![tanto_survey](../../f/f_dauvi/njombe.svg "tanto survey")
   - Features:
     - Populates the survey using a JSON template.
   
2. **TantoSurvey - 2013**
   - Description: An Android application to fill out a livelihood survey from a remote database.
   - Visual Representation: ![tanto_survey](../../f/f_dauvi/njombe.svg "tanto survey")
   - Features:
     - Populates the survey using a JSON template.

### Cordova Projects

1. **Canova and VeneziaÈUnica - 2014**
   - Description: Two applications developed using Cordova:
     - **Canova**: Logs the completion of cleaning servers per bus.
       - Features:
         * Loads workers' information
         * Logs which bus was cleaned at what time
         * Stores offline data during low connectivity
         * Syncs data with a server
         * Provides admin login and user management features
     - **Venezia è unica**: A mock-up application for purchasing coupons and transportation tickets.
       - Features:
         * Allows adding purchases to activate discounts.

2. **Gardalì - 2014**
   - Description: An IoT-based application that connects agricultural professionals with an IoT server.
     - Features:
       * Enables real-time monitoring of sensor data through a web portal.

### Angular Projects

- **Angular Examples:** This section provides details about applications built using Angular, though no specific projects are mentioned.

### Node.js Projects

1. **Geocode - 2020**
   - Description: An app to anonymize addresses by parsing and processing addresses with geocoding services.
     - Visual Representation: ![geocode](../../f/f_intertino/cover_geocode.png "geocode cover")
   - Technical Features:
     - Uses a chain of promises for address parsing.
     - Example code snippet demonstrating async function `parse_row`.

2. **Text Corrector - 2023**
   - Description: An automated assistant designed to help writing outreach sales emails using an AI language model.
     - Visual Representation: ![cover_corrector](../../f/f_intertino/cover_corrector.png "text corrector")
   - User Interface:
     - Composes email drafts in different sections like subject, greeting, value proposition, and signature.
     - Implements a criteria block for editing prompts and generates suggestions through the language model.

### Technical Implementation Details

- **Node.js Implementation:**
  - The app is built using Node.js with Express framework.
  - Main functions are implemented in JavaScript on the frontend.
  - Front-end and back-end separation is illustrated.
  - Detailed structure of API calls and data processing is shown.

### Deployment Instructions

- **Environment Setup:** Set up an `.env` file for environment variables such as OpenAI key.
- **Deployment Options:**
  - Run `npm install` followed by `npm start`.
  - Alternatively, use Docker with `cd build/ && docker-compose up -d`.

#### Access URLs:
- **Geocode Application:** [localhost:3000/geocode]
- **Text Corrector Application:** [localhost:3000/correct]

### Conclusion

This document serves as a comprehensive guide to various projects developed by the organization, highlighting their technologies and functionalities. It provides clear visuals and detailed descriptions for each project, making it easy for developers and stakeholders to understand and engage with the applications in question.

# personal profile

 Link: [personal profile]("../a/personal_profile.html")

This document provides a comprehensive overview of an individual's professional background, skills, and personal attributes:

### Professional Experience

- **Data Products & Infrastructure**: Hands-on experience in developing data products and infrastructure across technical, product, and commercial teams.
- **Data-Driven Decision-Making**: Built robust statistical analysis, predictive modeling, algorithm design, machine learning, and data/text mining skills.
- **Leadership of Complex Projects**: Successfully led complex technical projects in both B2B and B2C environments. Proficient in managing remote teams.

### Skills

- **Optimization Problems**: Specialized in optimization problems.
- **Productization of ML & Prototyping**: Expertise in productizing machine learning, creating prototype (PoC, MVP) solutions.
- **Tech Presales**: Strong tech presales skills.
- **Personas Segmentation & Multichannel Strategies**: Capable of persona segmentation and developing multichannel strategies to drive conversion uplift.
- **Coding Experience**: 15+ years of coding experience in data processing/viz, cloud/grid computing, web development, data platforms, ETL, and front/back end.

### Personal Attributes

- **Customer Understanding**: Developed a deep understanding of customer needs, which is crucial for building durable customer stakeholding.
- **Innovation Driven**: Keen on innovation, novel business models, and collaborative working environments.
- **Passionate Storytelling**: Passionate about storytelling and crafting compelling narratives.
- **International Languages Knowledge**: Good knowledge of international languages.
- **Long Coaching Experience**: Has a long history in coaching.

# spatial

 Link: [spatial]("../a/spatial.html")

### Spatial Analysis and Backup Material

#### Spatial Latency Analysis

1. **Data Collection**: We collected latency data based on vehicle positions using geohashes for coordinate pairs.
2. **Geographical Distribution**:
   - The average latency is calculated for each geohash, showing a pattern similar to modem upload and camera latency.
   - Incidents are clustered spatially where `camera_latency` exceeds 400 ms.
3. **Cell Handover Analysis**: 
   - Handovers are highly correlated but not directly linked with camera latency.

#### Backup Material

1. **Long Short-Term Memory (LSTM) Analysis**:
   - We trained a LSTM model using 16-fold cross-validation.
   - Randomly substituting features to assess the model's performance, indicating that synthetic random features significantly reduce the performance of models with important predictors.
2. **Dictionary Learning**:
   - Rolling windows are used to create time series clusters for clustering into an essential dictionary.
   - The dimensionality of the cluster is verified for orthogonality.

These analyses help in understanding spatial patterns and correlations related to latency, handover, and data analysis techniques.

# deployment

 Link: [deployment]("../a/deployment.html")

This document, titled "Deployment", provides an overview of experience with different CI/CD (Continuous Integration and Continuous Deployment) workflows. The main content includes:

1. **Introduction**: A brief introduction to the document.

2. **CI/CD Workflows**:
   - **GitLab**: Information on how to set up and use GitLab for continuous integration.
   - **Jenkins**: Details on configuring Jenkins for continuous deployment processes.

3. **Variables**:
   - Explanation of using variables in CI/CD pipelines, which allows for dynamic configuration without modifying the pipeline code directly.

This document is likely a guide or reference for setting up and managing CI/CD pipelines, particularly focusing on GitLab and Jenkins environments.

# sql

 Link: [sql]("../a/sql.html")

The document titled "SQL" discusses various aspects of SQL and its role in database management and system integration across multiple industries. It highlights the importance of database schema design, data integrity, performance optimization, backup strategies, and how these features are crucial for efficient data storage, decision-making support, and security.

The text then provides a detailed overview of four key components: Database Management, Web Development, Data Analytics, and Business Intelligence (BI). Each component is described in terms of its core functionalities, usage scenarios, and their respective importance in modern business operations. 

By focusing on these areas, the document emphasizes the comprehensive nature of SQL as it relates to data management and system integration. It highlights how each component works together to create a robust solution that spans from data collection to decision-making.

In summary, the document underscores the critical role of SQL in various aspects of database management and system integration across multiple industries.

# data platform

 Link: [data platform]("../a/data_platform.html")

### Data Platform Overview

The document outlines a comprehensive data platform setup that leverages Docker Swarm for scalability, microservices architecture, and secure access control. Here are the key features:

1. **Components**:
   - Docker images, middlewares, schedulers, jobs, and UIs.
   - Main components include Airflow for scheduling tasks, Metabase as a BI tool, Presto for querying data from Kafka, Nginx for webserver routing, and Kafka for messaging.

2. **Principles**:
   - Scalable architecture based on cloud and microservices.
   - Secure access by restricting jobs to granular or executive levels.
   - Compliance with anonymization and retention policies.
   - Innovative solutions evaluated against migration benefits.
   - Stable releases with comprehensive testing, monitoring, and alerting.
   - Safe data redundancy and version control.
   - Attractive tech stalks for attracting new talent.
   - Shared knowledge management in a document repository.
   - Agile project management focusing on goals, sprints, planning, and retrospectives.
   - Collaborative selection of admin tools.

3. **Structure**:
   - Core application is under the `sawmill` repository.
   - Docker images are built using scripts (`live_py/docker_build.sh`, `go_ingest/docker_build.sh`).
   - Environment variables are managed via `~/credenza/database.env` or secrets in GitLab.

4. **Security and Access**:
   - Secure infrastructure with different access levels for various services.
   - Infrastructure design to balance performance and operativity without sacrificing security.

5. **Project Management**:
   - Continuous integration (CI) using GitLab’s built-in tools.
   - Support and roadmap including tasks such as building the cluster, setting up a central database, platform integration, replacing routines, refining requirements, and API building.

6. **Contributing and Acknowledgment**:
   - Collaboration encouraged through pull requests.
   - Project license is CC-BY-NC-SA 4.0.

This document provides a detailed roadmap for setting up and managing a scalable data platform that adheres to modern best practices in security, scalability, and collaboration.

# tech

 Link: [tech]("../a/tech.html")

This document provides a comprehensive overview of the technical projects and activities related to motion and data analytics. The main sections cover:

### Data Analytics

1. **R Scripts**: Contains various R scripts used for data visualization, model building, reports, and predictive analytics from 2014 to 2016.

2. **Audience Overlap Analysis**: Demonstrates radar plots that illustrate differences between audiences using [audOverlap.gif](../../f/f_intertino/audOverlap.gif).

### Bots

- **Crowler Projects**:
  - Downloads popularity lines from Google Maps (2017, 2018).
  - Uses a headless crawler for temperature, Grafana, and various API services (2018).
  - Implements a geocoding function with double nested promises (2020).

### Data Bases

- **Database Interfaces**: Provides interfaces to access databases (2020).

### Native Applications

1. **Qt**: Information about Qt applications is not specified.

2. **Simulations**: No details are provided regarding simulations projects.

### Embedded Systems

1. **Arduino Projects**:
   - Mechanical Synth (2015)
   - Pitch Follower (2016)
   - Midi Joystick (2017)
   - Processing + Kinect (2017)
   - Voice Paint (2017)
   - Raspberry Pi OpenFrameworks Optical Keyboard (2017)

### Backend Development

- **Node.js**: Projects related to Node.js are located in the `nodejs` directory.

### Frontend Applications

1. **Cordova Apps**:
   - No specific details provided for Cordova applications.

2. **React Apps**:
   - A barcode scanning app using React + Metro (2020).

3. **Angular Apps**:
   - An Angular application for barcode scanning and Ionic (2020).

### Summary

The document outlines a range of technical projects across various domains, including data analytics, bots, databases, embedded systems, backend development, and frontend applications. The use of Node.js, R scripts, and React/Angular frameworks is prominent in the documentation.

# traffic motorway

 Link: [traffic motorway]("../a/traffic_motorway.html")

The document titled "traffic on motorways" describes a study aimed at analyzing and predicting traffic patterns on German motorway networks using machine learning techniques. The key points of the study are summarized below:

1. **Data Collection**: 
   - Counts of vehicles crossing motorway sections are provided by BaSt (Bundesamt für Straßenbau und Verkehr).
   - OpenStreetMap nodes representing intersections and roads are identified for each counting location.

2. **Time Series Representation**:
   - Hourly vehicle counts are converted into a 7x24 image representation, where each pixel represents the number of vehicles passing through a node at a specific time.
   - Backfolding is introduced to handle boundary conditions in the image representation.

3. **Model Definition and Training**:
   - A simple and complex convolutional neural network (CNN) architectures are defined for the autoencoder.
   - The model is trained using BaSt count data, and its performance is evaluated over multiple epochs.

4. **Results and Analysis**:
   - The model successfully reconstructs traffic patterns from backfolded time series images.
   - Performance metrics such as correlation and relative error are used to compare different models and identify the best performing solution.
   - Dictionary learning techniques are applied to find the minimal set of average time series for describing locations, leading to better generalization.

5. **Tuning and Interpolation**:
   - The model is fine-tuned to avoid local minima and improve convergence.
   - Upscaling or downscaling of images affects the performance of the model, with downsampling often resulting in overfitting.

6. **Traffic Node Selection**:
   - Efficient methods are used to identify appropriate via nodes on motorway roads by considering orientation, chirality, and street class importance.
   - The algorithm ensures that via nodes do not incorrectly count traffic from ramps at junctions.

7. **External Data Integration**:
   - The model is tested for its ability to integrate external data (e.g., from OpenStreetMap tiles) into the prediction process.
   - There are limited improvements in performance due to overfitting of the flat autoencoder when applied to external data.

8. **Encoder Implementation**:
   - An encoder network is introduced to help adjust levels and effects like Friday traffic, enhancing overall model performance.

In summary, the study demonstrates the effectiveness of using CNNs for traffic prediction on motorways and provides insights into how different modeling approaches can improve performance and accuracy in real-world applications.

# logs proc

 Link: [logs proc]("../a/logs_proc.html")

This document outlines various Python scripts designed for different purposes related to data processing, machine learning, geospatial analysis, and image generation. Each script serves a specific function within the context of various applications.

#### Data Processing and Machine Learning Scripts

1. **proc_freq.py**: Processes GPS trajectory data to calculate unique users, total events, and average events per user for each day.
2. **train_linear.py**: Trains a linear regression model using the Cal_Housing dataset with Spark MLlib.
3. **etl_tankRef.py**: Reads and processes reference curve data from log files, generating daily and hourly reference values.

#### Geospatial Analysis Scripts

1. **proc_cronon.py**: Processes trajectory data using Apache Spark.
2. **proc_traj.py**: Processes GPS trajectory data to compute motion vectors, velocity quivers, and clustering ratios for each segment of a trajectory file.
3. **test_etl_matrix.py**: Performs ETL operations on structured data using Apache Spark.

#### Image Generation Scripts

1. **gan_train_aws.py**: Trains various types of Generative Adversarial Networks (GANs) on AWS using Keras and TensorFlow.
2. **gan_train.py**: Another script for training GANs, possibly focusing on different domains or configurations.
3. **gan_deploy.py**: Deploys trained GAN models as endpoints on Amazon SageMaker.

#### Miscellaneous Scripts

1. **proc_demoData.py**: Processes data from a specified directory using Apache Spark.
2. **train_aws.py**: Another script for training GANs on AWS.
3. **etl_tank.py**: Contains functions for processing GPS trajectory data.

Each script addresses specific tasks related to the document's objectives, which include data processing, machine learning model training, geospatial analysis, and image generation. The scripts are designed to work together within larger applications or workflows that require handling large datasets and integrating with cloud services like AWS for scalability and performance.

### Summary

The scripts in this document collectively provide a comprehensive toolkit for data processing, machine learning, geospatial analysis, and image generation. Each script is tailored to perform distinct operations and can be integrated into various workflows to achieve specific goals related to data science and analytics.

# machine learning

 Link: [machine learning]("../a/machine_learning.html")

The provided document titled "Machine learning models and practices" from directory contains a summary of various machine learning concepts, including:

1. **Supervised vs Unsupervised Learning**: 
   - Supervised learning involves labeled data where the model learns to predict outcomes based on inputs.
   - Unsupervised learning works with unlabeled data to find patterns or group similar data points.

2. **Gradient Boosting**:
   - Gradient boosting focuses on building a sequence of simpler models that each improves upon the last by minimizing the loss function.
   - It uses ensemble methods such as bagging and boosting, where each model tries to correct the errors of the previous model in the sequence.

3. **XGBoost**:
   - XGBoost is an optimized gradient boosting library designed for speed and performance, capable of handling a variety of machine learning problems.

4. **Hyperparameter Tuning**:
   - Hyperparameters are crucial for optimizing the performance of models. They can be tuned to find the best configuration.
   - Techniques like grid search, random search, and Bayesian optimization are used to explore different combinations of hyperparameters efficiently.

5. **Transformer Attention Projection**:
   - This concept is not fully described in the provided text; it likely refers to a specialized technique or mathematical operation related to neural networks.

6. **Random Forest Depth**:
   - The depth of a decision tree in a random forest model affects its complexity and ability to capture complex patterns in data.

7. **L1/L2 Regularization**:
   - These are regularization techniques used to prevent overfitting by adding penalties to the loss function.
   - L1 regularization adds absolute values of coefficients, while L2 regularization adds squares of the magnitudes of coefficients.

8. **Boosting**:
   - Boosting is a family of algorithms that combine multiple weak learners to form a strong learner. Common boosting algorithms include gradient boosting and AdaBoost.

# triangulation

 Link: [triangulation]("../a/triangulation.html")

This document describes an approach for estimating activity centers, spatial coverage, and stability in wireless network data using triangulation techniques. The key steps include:

1. **Cell Coverage Estimation**: Determine the most precise cells in a given area using Best Server Estimation (BSE) centroids.
2. **Triangulation of Activity Centers**: Sum up events into polygonal activities based on these BSE centroids, then refine their positions to account for spatial stability and noise.
3. **Geohash Binning**: Anonymize data by encoding coordinates into geohashes to protect individual counts while maintaining precision.
4. **Space Deformation**: Introduce a curvature factor to the space model, affecting activity center positions based on cell centroids.
5. **Network Integration**: Incorporate street network information to simulate real-world movement patterns and adjust activity positions accordingly.

The document provides a detailed explanation of each step, including mathematical formulations and implementation details.

# node

 Link: [node]("../a/node.html")

# Node.js Portfolio Summary

This document outlines the work done using Node.js. The portfolio focuses on:

1. **Automation**: Includes tasks such as crawlers, Selenium automation, and automated testing.
2. **Backend Development**: Focuses on interfaces with databases.

## License

The content is licensed under a Creative Commons Attribution-NonCommercial-Share Alike 4.0 International (CC BY-NC-SA 4.0) license.

# spatial data

 Link: [spatial data]("../a/spatial_data.html")

The document "spatial_data.md" discusses various attributes associated with spatial data, including:

1. Labelling: This refers to identifying objects or locations within a spatial dataset.
2. Routes: It relates to the paths and connections between different points or areas.
3. Terrain: This deals with the physical features of an area, such as mountains, valleys, and hills.
4. Supply lines: It is about the routes or systems used for transporting goods from one location to another.

Overall, the document emphasizes that spatial data encompasses a wide range of attributes related to geographical features and their relationships within a space.

# mallink engine

 Link: [mallink engine]("../a/mallink_engine.html")

The mallink_engine.md document discusses the optimization of a system for delivering scooters among drivers. The main tasks include:

1. Routing efficiency: Calculating the most optimal route connecting all spots a van could see.
2. Spot prioritization: Predicting layers where revenue is most likely to be high, considering factors like potential revenue and costs.
3. Energy calculation: Considering single paths and interactions between them to optimize energy usage.
4. Class structure: Displaying interdependencies and solving the problem by toggling spot activation and applying the Metropolis algorithm.

To improve acceptance rates of moves, Markov Chains are introduced:

1. Calculating a dense Markov chain (first power) and increasing the power until a sparse Markov chain is obtained.
2. Using a cumulative probability to simplify the iteration process as iterations proceed.

The document also explores different types of moves like single task move, extrude, phantom, canonical, and gran canonical simulations to improve convergence and run time efficiency.

Overall, the goal is to find an efficient distribution task among drivers that minimizes costs while maximizing revenue.

# agent naming

 Link: [agent naming]("../a/agent_naming.html")

This project aims to create a reinforcement learning model that can identify and name objects in environments similar to Atari games. The team compared their approach with a previous implementation of Deep Q-Network (DQN) for playing Breakout, focusing on differences such as using velocity and collision data instead of stacked images, increasing batch size, and implementing a feedback loop between actions and the model's output.

### Key Points:

1. **Agent Objective**: The agent learns to interact with the environment by making decisions that maximize rewards, such as crushing bricks in Breakout.

2. **Model Architecture**:
   - **Input Data**: Uses velocity, frame difference (collision), and batch of 64 consecutive states.
   - **Output Actions**: Determines actions like moving a paddle or changing its position.
   - **Attention Mechanism**: Monitors which parts of the environment are most important for learning by focusing attention on specific areas.

3. **Visualization**:
   - **Scores**: Tracks training loss and reward.
   - **Inputs**: Shows average states and velocity changes.
   - **Actions**: Visualizes distribution of actions over time.
   - **Attention Map**: Highlights which parts of the environment the model is paying attention to at each step.

4. **Learning Challenges**:
   - **Causality in Breakout**: The team identified a clear correlation between scores, hits (brick destruction), ball bounces, and paddle control, but found less direct causality from actions like hitting bricks.
   - **Attention Evolution**: Over time, the model's focus shifts from digits to bottom elements, indicating it starts learning to avoid losing life.

5. **Future Work**:
   - Introducing additional scores as output that depend on specific actions and studying the activation for those actions.
   - Expanding the model's capabilities to handle different types of games with varying challenges.

### Implementation Details:

- The team used a genetic selection algorithm to evolve their DQN, considering fitness in each iteration.
- They ensured that the model's outputs were designed based on measurable interactions with the environment, categorizing them into classes like myself, tools, walls, info, and dangers.

This project provides insights into how reinforcement learning models can be tailored for specific environments and challenges, especially those involving causal reasoning.

# filatto infra

 Link: [filatto infra]("../a/filatto_infra.html")

**Summary**

### Title:
Filatto

### Author and Date:
Giovanni Marelli | 2019-11-18

### License:
Creative Commons Non-Commercial Share Alike 3.0

### Language:
en-US

### Output Format:
Markdown (Strict, Backtick Code Blocks, Autolink Bare URLs, Markdown GitHub)

---

# Delivery SaaS

Filatto is a SaaS designed for micro-mobility-based delivery that integrates different components to manage supply, collect workforce status, and provide ordering and tracking features.

**Principles:**
- Cloud based
- Full-API
- Modular
- Open source

**Key Components:**
1. **Supply Management**: Manage, organize, and display supply.
2. **Workforce Status**: Collect and organize the status of the delivery workforce.
3. **Ordering**: Provide consumers with the option to order.
4. **Acceptance & Payment**: Accept orders and process payments.
5. **Delivery Tracking**: Track the status of deliveries.

# Infra

## ERP
The suggested ERP is [Odoo](https://www.odoo.com/). Key reasons include:
- Cloud based
- On-prem/SaaS
- Open source, highly configurable
- Large marketplace with many apps
- Website/e-commerce builder
- Full-API

![Odoo Apps](../../f/f_ops/odoo.png)

## Middleware
The middleware is the core component of the project and handles requests between:
1. Consumer app
2. Provider app
3. Delivery app
4. ERP

![Filatto Infra](../../f/f_ops/filatto_infra.svg)

## Data Storage
Data storage uses various types of databases to store and query data:
- Demand and supply stored in a relational DB.
- Maps and areas as geo shapes in MongoDB.
- Customer preferences represented as graphs.

![Filatto Infra](../../f/f_ops/filatto_db.svg)

## Optimization
An additional service will optimize delivery availability, operating areas, and routing times. This is referred to in the infra section.

## Apps
The consumer app is designed using the [Intertino](https://github.com/sabeiro/intertino/angular/qr_ang) project:
- Front-end development with Node.js (React/Angular)
- Testing with Ionic
- Compilation with Ionic

### Users of the App:
1. Suppliers
2. Delivers
3. Consumers

## Partnerships
| Company | Infrastructure |
| --- | --- |
| Takelocal | ?? |

| Company | Infrastructure |
| --- | --- |
| ?? | ?? |

## Addressable Market
- Restaurants-clients: Food delivery
- Shops-clients: Grocery delivery
- C2C: Parcel delivery

## ERP Settings
ERP settings include:
1. Defining shifts for relative restaurants, operating areas, and operating time shifts.
2. Booking rider's shifts from the ERP.
3. Fleet management to route requests on other fleets if riders are booked.
4. Three categories of rider payments (freelance, monthly salary, weekly salary).
5. Riders' availability calendar, booking system, performance reporting, bonus/malus reporting.
6. Payment system: e-invoice, direct debit.

---

### References:
- [Infra](antani_infra.html)

# antani infra

 Link: [antani infra]("../a/antani_infra.html")

### Summary of antani_infra.md

This document outlines the infrastructure setup for Antani, an agent/network intelligence system. It covers deployment, server specifications, client-side frontend, and server-side backend implementations.

1. **Deployment**
   - The engine is deployed using a hypervisor and containers.
   - Services are linked to check routing and services.
   - Example commands for setting up the environment include:
     ```bash
     sudo yum -y install httpd php libapache2-mod-wsgi python-dev
     ...
     sudo systemctl restart httpd.service
     ...
     docker run -it --link redis1:redis --name $imgName -p $PORT:$PORT -v $(pwd):/$APP_DIR $imgName bash
     ...
     curl $SERVER/antani
     ```

2. **Server Specifications**
   - The base URL for the service is `http://$SERVER/antani`.
   - Endpoint details include:
     * `/`: Checks server status.
     * `/conf`: Changes configuration.
     * `/longtask`: Starts long process.
     * `/status`: Gets current process/worker status.
     * `/solve`: Starts worker and returns a job ID (Routific format).
     * `/jobs`: Returns job status/solution (Routific format).
     * `/publish`: Publishes solution after manual inspection.
     * `/simplify`: Simplifies the route.
     * `/process`: Serial routine start.
     * `/solution`: Returns published solution.

3. **Frontend**
   - A frontend is available at [dauvi.org/antani_viz/].
   - JavaScript code for interacting with the server includes:
     ```javascript
     $.ajax({
         type: "POST",
         url: url,
         data: JSON.stringify(data),
         contentType:"application/json",
         success: function(json) {
             console.log(json);
             if(Object.keys(geom).length !== 0){
                 sol = json;
                 geom = formatData(sol);
                 spotL = geom.spotL;
                 pathL = geom.pathL;
                 refreshLayer(spotL);
             }
         },
         error: function(xhr, status, error) {console.log(status + '; ' + error);}
     });
     ```

4. **Backend**
   - A Flask app is created to handle requests and responses.
   - Routes include:
     * `/simplify`: Simplifies the route based on a JSON input.
     * `/solution`: Returns the simplified solution as JSON.

5. **Asynchronous Processing**
   - Celery is used for asynchronous tasks.
   - Example of creating a Lambda function and connecting it to an API Gateway.

6. **Data Structure**
   - A data structure is proposed for seamless communication between OptEn, backend, and frontend.

7. **AWS/Productization**
   - The solution is stored in an S3 bucket using JSON serialization methods.
   - Lambda functions are used to handle API requests.
   - Chalice is introduced as a tool for managing AWS resources and deployments.

Overall, the document provides a comprehensive guide on deploying and managing the Antani system, including backend infrastructure, frontend development, and asynchronous processing with AWS services.

# audio mixer

 Link: [audio mixer]("../a/audio_mixer.html")

The document titled "Motion" has the following details:

Title: Motion
Author: Giovanni Marelli
Date: 2019-07-02
Rights: Creative Commons Non-Commercial Share Alike 3.0
Language: en-US

Output configuration:
Type: Markdown Document (markdown_strict + backtick_code_blocks + autolink_bare_uris + markdown_github)

# causality

 Link: [causality]("../a/causality.html")

The document discusses the concept of causality and statistical techniques to infer it. Key points include:

1. **No Statistical Technique Can Test Causation**: Directly inferring causality from data is not possible without a controlled experiment. Correlation does not imply causation.

2. **Experimental Design**: For causal inference, one needs to control for all other variables and ensure the manipulation of only one variable (the independent variable) affects the dependent variable.

3. **Observational Data**: If only observational data are available, correlation can be suggestive but not conclusive. Hypotheses must be made and tested, even if the lack of a correlation does not disprove causation.

4. **Statistical Techniques**:
   - **Granger Causality**: A statistical technique to test whether one time series is a good predictor of another. It is less reliable than controlled experiments.
   - **Instrumental Variables (IV)**: Useful in econometrics when there are endogeneity issues and direct causal relationships cannot be established through experimental methods.

5. **Longitudinal Studies**: These can introduce confounding variables, making causal inference challenging even with experiments.

6. **Statistical Testing**:
   - **Hypothesis Tests**: Necessary to verify models and make inferences. They should be used with caution as they often rely on assumptions.
   - **Reliability Analysis**: Important for validating models to ensure reproducibility.

7. **Decision-Making in Research**: The reliability of findings should be assessed, particularly in high-stakes areas like drug development, where accurate inference is crucial.

8. **Practical Applications**:
   - Deep learning techniques are increasingly being used in fields like computer vision and natural language processing.
   - Bayesian methods offer new approaches to probabilistic reasoning and can be applied to various statistical problems.

Overall, the document emphasizes the importance of experimental design and robust statistical methods for inferring causality from data.

# cplusplus

 Link: [cplusplus]("../a/cplusplus.html")

The document outlines several areas of research in C++ programming with various libraries and applications:

1. **Math Libraries**: This section covers mathematical operations including matrix filtering, algebraic functions, numerical integration/derivation, approximated basic functions (Gamma, Bessel, Neumann), spectral analysis, correlation, normalization, statistical properties, interpolation, regression, filtering, Bezier curves, and splines.

2. **Sputtering Simulations**: This application uses Monte Carlo simulations to study the behavior of ions on a silicon lattice, calculating impurity diffusion. The process is visualized using a 3D model.

3. **Monte Carlo Simulations for Lipid Chains**: These simulations simulate the grand canonical equilibrium of lipid chains around a nanoparticle. The results are displayed graphically with features like log, points, lines, spectrum, autocorrelation, and running average.

4. **Molecular Dynamics Simulations**: This application visualizes the dynamics of molecules and surfaces using OpenGL for 3D rendering. It can display chains, molecules, surfaces, and navigate through them.

5. **Visualization Tools with Qt**: The software Avvis is described as a C++/Qt application that has been developed over six years. It supports various features such as displaying signals, plotting ranges, computing spectrum, autocorrelation, and more. A screenshot of the program's interface is included.

6. **Visualization Tools with OpenGL**: ElPly is a 3D visualization software that can display simulation results of lipid chains, surfaces, molecules, and navigate through them using OpenGL for 3D rendering. It supports features like displaying chains, marching cubes, navigating menus, and reading configuration files.

7. **Gtk Libraries**: This section describes a Python 2 code called caciotta leaks, which creates an interface between the ERP database and the user. The code is illustrated with a screenshot of the interface.

8. **Finite Differences Code**: This C++ code computes finite differences up to 4th order for continuum mechanics simulations using marching cubes.

9. **Bot Review of Source Code**: This section provides a bot review focusing on multiple files working together to support scientific programming and calculus, emphasizing various functionalities like mathematical libraries, calculus solvers, data sources integration, optimized code, visualization tools, parallel computing support, machine learning integration, user interface, documentation and examples, and community support.

# no key board

 Link: [no key board]("../a/no_key_board.html")

The document titled "Motion" is authored by Giovanni Marelli and was last updated on July 2, 2019. It's licensed under the Creative Commons Non-Commercial Share Alike 3.0 license. The language used in this document is English (en-US). The output format specified for generating markdown content is defined as `md_document` with the variant set to `markdown_strict+backtick_code_blocks+autolink_bare_uris+markdown_github`.

# location

 Link: [location]("../a/location.html")

The document titled "location" provides an overview of various features and analyses related to urban planning and geospatial data processing. The key points covered include:

1. **City Features Analysis**: 
   - A series of Overpass Turbo queries are used to identify the most important features for each city.
   - These features are analyzed using buffers and layer dissolving techniques to visualize them on maps.

2. **Population Density Calculation**:
   - Official statistical data such as population density, gender asymmetry, foreigner percentage, flat density, land use, and age asymmetry is enriched with POI information.
   - Population density is calculated using a stiff multiquadratic interpolation function based on neighboring official census data tiles.

3. **Degeneracy Measurement**:
   - Degeneracy is defined as the recurrency of POIs in a spatial region. It is measured by calculating the distribution of other POIs at a certain distance and fitting a parabola to determine the degeneracy as the intercept of this curve.

4. **Isochrone Calculation**:
   - Each location's local network data is downloaded, and isochrones are calculated for various times (e.g., 15 minutes).

5. **Spatial Forecast Prediction**:
   - There are examples of spatial forecast prediction in the literature, such as predicting property values using machine learning techniques.

The document aims to provide a comprehensive analysis of urban features and their relationships with spatial data and statistical models.

# ml eng

 Link: [ml eng]("../a/ml_eng.html")

ML engineering involves developing and managing systems that enable machine learning models to be developed, trained, deployed, monitored, and maintained efficiently. The provided document lists three key technologies related to ML engineering:

1. Protobuf: A language-neutral data interchange format used for serializing structured data in a way that is efficient and easy to parse. It is commonly used in ML applications to serialize large datasets or protocol messages.

2. GraphQL: An API query language and server-side runtime that provides an interface to a web service's data. GraphQL allows clients to request only the data they need, making it more efficient than RESTful APIs for complex queries involving multiple resources.

3. (Missing item): The document does not provide information about the third technology listed.

Overall, ML engineering involves using these technologies to design and implement systems that support machine learning workflows, from model training and deployment to performance monitoring and maintenance.

# synth

 Link: [synth]("../a/synth.html")

The document named synth.md contains a title, author, date, copyright information, language setting, and output options. The title is "Motion", the author is Giovanni Marelli, it was published on July 2nd, 2019, and is licensed under Creative Commons Non-Commercial Share Alike 3.0. The language used in the document is English (United States). The output options are for creating a markdown file with specific variant settings for backtick code blocks, autolink bare URIs, and Markdown GitHub formatting.

# websites

 Link: [websites]("../a/websites.html")

The document titled "websites.md" in the directory contains a comprehensive summary of various websites that the author has worked on, along with their brief descriptions and screenshots. The sites covered include:

1. **Mr Relais (1999)**: A high school project website to sell electronics schemas and general knowledge.
2. **Kotoba (2006-2011)**: An online learning platform about university studies, written in PHP with features like simulation code, log-in functionality, language lessons, physics compendium, pictures, and music.
3. **Tanto (2013)**: A website for data collection and repository during an internship period in Tanzania, showcasing reports and work done during this time.
4. **Dauvi (2013-2017)**: The first server hosting Odoo ERP and publishing the first apps written in Cordova.
5. **Website Requests (2013)**: A collection of websites from the consultancy period, showcasing different types of businesses and services.
6. **Intertino (2016)**: A website promoting web digital and analytical tools.
7. **Anticolo (2016-2021)**: A data room for sharing KPIs with management, featuring features such as time series reports, aggregations, KPI monitoring, and renders JSON.

Each site includes a logo and brief descriptions of its main features or functions. The screenshots provided in the document are crucial for understanding the visual aspects of each website.

# security

 Link: [security]("../a/security.html")

### Security Overview

The document discusses the importance of designing secure infrastructure without compromising performance or operativity. It provides a comprehensive overview of different types of data breaches, including those related to:

1. **Personally Identifiable Information (PII):** Data that can be linked to an individual, such as personal details and financial information.
2. **Financial Information:** Especially vulnerable due to its connection to PII, it can lead to fraud and identity theft.
3. **Health Information:** Sensitive due to its value in healthcare transactions and the potential for misuse by bad actors.
4. **Intellectual Property (IP):** Valuable trade secrets and confidential information that could be sold or disclosed.
5. **Competitive Intelligence:** Relevant data about competitors' strategies, which can provide an advantage.
6. **Legal Information:** Data contained in legal documents, such as agreements and contracts, which might have sensitive content.
7. **IT Security Information:** Important for accessing systems, including passwords and other credentials.

### Secure Practices

The document outlines several secure practices to protect various aspects of infrastructure:

- **Password Management:** Utilizing strong, unique passwords and implementing secure authentication mechanisms (e.g., bcrypt).
- **Environment Variables and Docker Configuration:** Keeping sensitive data out of code repositories and securing configurations.
- **Web Server Security:** Implementing authentication mechanisms like Basic Auth or API tokens for web services.
- **Middleware Security:** Protecting middleware components with access controls to prevent unauthorized access.
- **API Token Management:** Using secure methods to manage API tokens, such as JWT (JSON Web Tokens) and OAuth.
- **Web Server Authentication:** Utilizing HTTP headers for authentication to enhance security.

The document provides examples of how different technologies can be secured in practice, including Nginx with Basic Auth for authentication, Flask and Go gorilla/mux for securing APIs, and Apache2 for web server authentication using `.htpasswd`.

# spiega business

 Link: [spiega business]("../a/spiega_business.html")

This document is an overview of the author's professional experience, which spans over 17 years in various data-driven business roles across different industries. The key points include:

1. **Technical Expertise**: Hands-on experience in a wide range of technologies including AI, ML, and data science.
2. **Leadership Skills**: Successfully managed complex technical projects in both B2B and B2C environments.
3. **Cross-Functional Collaboration**: Strong collaboration across technical, product, and commercial teams.
4. **Project Management**: Proven ability to lead multi-disciplinary projects spanning automotive, energy, pharma, FSI, manufacturing, research, advertising, publishing, mobility, telecom, retail, and airline sectors.
5. **Specialized Knowledge**: Expertise in optimization problems, data science for productization, prototyping, tech presales, personas segmentation, multichannel strategies, conversion uplift, and AI development.
6. **Client-Specific Projects**: Successful execution of various client projects, including energy management, IoT predictive maintenance, blockchain in pharma, insurance assistant bot, mortgage installment collection uplift, sales automation tools, mobile network analytics software, data monetization for targeted audiences, inventory forecasting, and customer feedback analysis on e-commerce.
7. **Technical Roles**: Covered a diverse range of technical roles such as Tech Consultant, Data Science, Tech Consultant/Technical Lead, AI Lead, Project Manager/SME/Lead, Data Architect/Data Engineer, Sales/Marketing/Consultant, Technical Consultant/Collaborator, Data Analyst/Data Engineer/Consultant, and Customer Support Specialist/Agent.
8. **Customer Contact Points**: Experience in call centers, e-commerce, email, advertising, with a focus on improving customer retention, upsell, seller performances, in-site performances, and metrics like open rate and whitelisting.

The document serves as an extensive professional profile highlighting the author's deep expertise and successful track record across various data-driven business use cases.

# data compliance

 Link: [data compliance]("../a/data_compliance.html")

This document outlines the principles and design considerations for building an infrastructure that ensures data compliance across various requirements, including security, access control, data protection, anonymization, data retention, and purpose.

### Data Compliance

Designing a secure infrastructure involves fulfilling several general and specific requirements, which include:

1. **Security**: Ensuring robust security measures are in place to protect against unauthorized access.
2. **Access Control**: Granting appropriate levels of access to data while adhering to privacy laws.
3. **Data Protection Law**: Complying with relevant data protection regulations such as GDPR.

### Data Access

The infrastructure should:

1. **Distinguish Between User and Job Access**:
   - **User Access**: Allows individuals to view, query, or export data, subject to restrictions on personal-sensitive data.
   - **Job Access**: Processes the data and aggregates results, without access to sensitive information unless necessary.

2. **Sensitive Data Categories**:
   - **Public Data**: Available on the internet or licensed by the source.
   - **Personal Data**: Information about individuals with varying levels of sensitivity.
   - **Synthetic Data**: Artificially generated data for development purposes.
   - **Sensitive Data**: Defined as personal information covered under GDPR, including name, address, date of birth, etc.
   - **Anonymized Data**: Data where sensitive fields are hashed, masked, or deleted.

### Anonymization

To handle sensitive data effectively:

- **Hashing**: Converts data into a cryptographically secure format to protect privacy.
- **Masking**: Substitutes sensitive fields with dummy values that cannot be linked back to the original data.
- **Deletion**: Removes sensitive information from datasets entirely.
- **Homomorphic Encryption**: Encrypts data so that operations on encrypted data result in an encrypted answer, which can be useful for certain types of analyses.
- **Aggregation**: Groups similar personal information into ranges (e.g., age groups).
- **Zero Knowledge Proof**: Provides specific access to data without revealing the exact value.

### Retention and Purpose

Data storage should consider:

1. **Retention Time Frame**: Aligns with legal requirements, such as those for audits or financial purposes.
2. **Purpose of Storage**: The infrastructure should be designed with clear objectives in mind regarding how and why data is stored.

For different stakeholders—data producers and consumers—the approach to access control and retention differs:

- **Data Producer**: Obliged to retain certain data sources according to legal requirements (e.g., audit logs or financial records).
- **Data Consumer**: May require clear documentation of data usage purposes and a specific retention policy before granting access.

### Processing Windows and Historical Trends

In operational scenarios, consider the following approaches:

- **Processing Window**: Allows for processing of granular data within specified time limits, with a buffer period to reprocess in case of failures.
- **Historical Trends**: Retains aggregated reports for comparison over time.
- **Financial Data**: Ensures that billing and cost-related data are retained appropriately.

### Conclusion

This document provides a comprehensive guide on designing an infrastructure that ensures data compliance across various aspects, including security, access control, data protection, anonymization, retention policies, and operational considerations. It outlines the importance of distinguishing between user and job access, categorizing sensitive data, implementing effective anonymization techniques, and considering retention and purpose in data management practices.

# creative coding

 Link: [creative coding]("../a/creative_coding.html")

This document, creative_coding.md, appears to be a guide on creating animations using WebGL and shader programming. The author mentions that they have tried to develop an application for this purpose, but the crashes make it difficult to maintain the code base effectively.

The text describes three different creative coding techniques:

1. Slit scan effect: This technique involves cutting through layers of image data and rearranging them to create a new visual effect.
2. Puzzle effect: This involves dividing an image into smaller pieces that can be moved around to form a new picture.
3. Video manipulation: The author describes how they are experimenting with manipulating video footage using WebGL.

The document also mentions that the tool is useful for writing animations but has resulted in significant crashes that have made it challenging to save past code. It ends with a license notice stating that the content is licensed under CC by-sa-nc (Creative Commons Attribution-NonCommercial-ShareAlike).

# geo

 Link: [geo]("../a/geo.html")

This Markdown file titled "geo transformation and queries for GIS" contains a detailed description of various geometric transformations and queries used in geographic information systems (GIS). The document is organized into sections focusing on:

1. **Geo Operations**: Contains code snippets and explanations for different spatial operations such as identifying points within polygons, clustering coordinates, calculating angles, tangent points, containing features, polygon to edges conversion, spectral clustering, intersecting lines/areas, resampling data, querying with MongoDB near sphere distance, filtering by lists, bounding box queries, etc.

2. **MongoDB Queries**: Provides examples of using MongoDB for querying and finding nearby points within a specified distance or locating records that intersect specific areas or polygons.

3. **Neo4j Queries**: Demonstrates basic operations using Neo4j, including creating nodes, relationships, executing queries, and visualizing graphs.

4. **Network Operations**: Shows how to create, manipulate, and visualize networks using the OSMnx library for street network data in Germany and the NetworkX library for general graph manipulation tasks.

5. **License Information**: Includes a Creative Commons Attribution-NonCommercial-ShareAlike 3.0 license statement at the end of the document.

The content is rich with Python code snippets that can be used for implementing these operations in GIS projects.

# admin tool

 Link: [admin tool]("../a/admin_tool.html")

The "admin_tool.md" document in the specified directory outlines a collection of powerful administration tools designed for easy deployment. The main sections include:

1. **docker**: Information about Docker, which is likely a containerization platform used to manage and run applications within isolated environments.

2. **kafka**: Details on Kafka, which is described as "a distributed event streaming platform that can be used for high-throughput messaging."

These sections provide introductory information about each tool, suitable for users interested in deploying and managing them effectively.

# ml basics

 Link: [ml basics]("../a/ml_basics.html")

### Introduction to AI

The document begins by providing a brief introduction to artificial intelligence (AI), its concepts, and terminology. It highlights that AI requires an instance to run and must have connections for input and output. The text explains how AI learns from historical data and works with probability, identifying high-frequency occurrences as accurate predictors.

### Evolution of AI Cycle

The evolution of the AI cycle is discussed, emphasizing the importance of a data-driven approach and the need for an ML pipeline in successful projects. The text mentions that rule-based systems are more suitable for low-reoccurrence tasks compared to big data applications.

### Importance of Data and ML Pipeline

The document stresses the crucial role of high-quality data in AI projects and highlights the importance of a well-defined ML pipeline. It also notes that AI is beneficial for simplifying complex stratified rules, such as pricing.

### Ethical Considerations

The ethical considerations of AI are briefly mentioned, discussing concerns about bias, privacy, and potential misuse of AI systems.

### GenAI (Generalized AI) and its Types

The document introduces genAI, describing it as a branch of AI where models generate content instead of numerical values or items from lists. It discusses the different types of genAI media: text, images, sound, video, with specific decomposition techniques for each media type.

### ML Types

Different types of machine learning are introduced, including prediction, forecasting, pattern recognition, anomaly detection, compression, and classification.

### From Need to Production

The journey from idea to production in AI projects is outlined. The text emphasizes the importance of management, foundation, PoC (Proof of Concept), planning, production, and post-sales phases, with a focus on delivering high-quality outputs and effective monitoring and reporting.

### Project Types

The document lists various AI project types, including manufacturing, logistics, media, banking, finance, insurance, energy, IT, e-commerce, advertising, healthcare, retail, and telco. It also mentions cross-industry use cases like product suggestion, contact points, customer care, audience targeting, sale assistant, and knowledge sharing.

### What is ML Made of?

The basics of machine learning are presented, focusing on the distinction between frequentist and probabilistic approaches. The document discusses training, model types (regressors, classifiers), neural networks, attention mechanisms in transformers, prediction vs forecasts, reinforcement learning, and computer vision and natural language tasks.

### Evaluation

Evaluation of genAI systems is discussed, emphasizing the need for advanced metrics like consistency, toxicity, hallucinations, correctness, and accuracy. The text highlights that AI models require a ground truth from domain experts to evaluate their performance effectively.

### GenAI Overview

GenAI is introduced as a branch of AI focused on generating content rather than making numerical predictions or providing items from lists. The text covers the different types of genAI media and mentions the evolution of transformers in data science since 2018. It also notes that transformer architecture has limitations without built-in intelligence, emphasizing the importance of training effort and high-quality input data.

This summary provides a comprehensive overview of AI concepts, including its history, types, ethical considerations, and advanced evaluation metrics used in genAI projects.

# middleware

 Link: [middleware]("../a/middleware.html")

The document named `middleware.md` is about middleware in a cluster environment. It includes the following sections:

- **Authentication**: The document provides examples of authentication methods implemented in Go and Python code snippets.
- **Database Interface**: A simple Go function for querying data from a database is described, which fetches entries based on specified criteria.
- **Messaging Interface**: An example of a middleware using Flask/FastAPI to produce and consume messages through Kafka, demonstrating how to set up and interact with Kafka in this context.

# train mapping

 Link: [train mapping]("../a/train_mapping.html")

### Train Mapping

We create a mapping based on reference data for a small geographic area that cannot be resolved with our data. The goal is to establish the contribution of each cell to measuring visitors.

#### Consistency in Reference Data

The reference data has internal consistency varying from location to location. We control this consistency by adding noise and checking its stability at different levels (daily, hourly). We also observe that noise at the hourly level does not change correlation as fast as for daily values, leading to differences even when 15% noise is introduced.

#### Forecastability

We quantify the forecastability of customer time series using a long short term memory model on reference data. Some reference data are easy forcastable by the model, while others are not understood.

#### Data Preparation

We use filters on activities and calculate daily values on a CILAC basis. The tarball is processed with an ETL script that unpacks the tar and processes the output using Spark.

#### Mapping Weights

We filter cells based on their proximity to the POI and find the best linear weights for each cell contributing to measure activities at the location using least squares optimization. This helps in achieving a better match between the activities and reference data.

#### Effect of Filtering

Filtering slightly improves input data, but after weighting it is irrelevant. Among different filters, version 11.6.1 with 40 km previous distance and chirality shows the best results.

#### Effect of Mapping

We monitor the correlation improvement at each step of the process and find that the version 11.6.1 with 40 km previous distance and chirality achieves the highest correlation with reference values.

#### Capture Rate

The stability of the capture rate over time is checked, and the min-max interval is within acceptable limits without problematic outliers.

#### Software Overview

Different models are tested for their best performances and stability. The suite includes APIs, spatial grid operations, visualization tools, training methods using Keras, regressor tests on learn/play sets, bot selenium for location enrichment, signal processing libraries, dataset utilities, model collection, execution routines, geographical enrichment, convolution kernels, text parsing utilities, curve summarization, long short term memory algorithm, and learning/play testing.

#### Learn Play

Learn-play is used to run regressors on time series data. Depending on the temporal resolution, different datasets are prepared for training using [train_execute](/geomadi/blob/master/geomadi/train_execute.py).

#### Long Short Term Memory (LSTM)

A dataset is prepared that includes reference data, time, activities, footfall, isocalendar, historical data, mean temperature, cloud cover, and humidity. The LSTM algorithm is then run over 30 days to predict future activity levels.

#### First Location Set

We prepare data for a set of locations with high daily visits, low chi-square, skewness, variance on reference, high correlation blind test, low variance in long short term memory, and large cell coverage.

#### Production

Cooperation with Insight is required for backup, validity proof, optimization of methods, productization, harmonization of the xy source, impact of new infrastructure on activities and footfall, improvement of spatial resolution for activities, and improvement of activity filters.

#### Competitors

A prediction model is needed to derive motorway guest counts for competitor locations. This model will consider telco data, cilac labelling, geographical data (population density, land use), and weather data.

### ToDo Items

- Insert Google popularity lines
- Feature importance for every location
- Evaluate the model on February 2019
- Retrain on new reference data and include footfall

# video production

 Link: [video production]("../a/video_production.html")

The document "video_production.md" is a content strategy for a music channel named Viudì, which shares ideas and projects related to musical instruments, soundtracks, electronic music gear, DIY projects, and other audio-related topics.

### Key Points:

1. **Channel Focus**:
   - The channel primarily focuses on creating original electronic jam videos with unique soundtracks.
   - Videos have different topics, including DIY projects, nature-based exploration, and technology-based connections between instruments, effects, and loudspeakers.

2. **Content Structure**:
   - Each video is a "dawlessjam" (meaning no DAW or editing software) where all edits are done during the video editing process.
   - Videos often include sound loops from different types of instruments and have specific keywords to categorize them.

3. **Audience**:
   - The channel aims to motivate musicians to add devices and sounds into their music, as well as producers to leave their audio workstation and play more music.

4. **Upcoming Content**:
   - Two new video concepts are planned to maintain continuity in the electro-journalism workflow:
     1. "Winter Acoustics" – an electro ambient jam focused on winter landscapes using natural echo locations.
     2. "Technical Tutorial (Gear Focus)" – a tutorial focusing on adjusting granular settings for different environments using the Aira P-6.

5. **Tech Used**:
   - The channel uses various electronic music instruments such as Roland Aira, Korg Volca, and Zoom SampleTrak/Zoom G1.
   - Cameras include Sony Alpha, Insta360, and Rode AI Mic.
   - Locations covered include Italy, Alps, Kyoto, Berlin, and other countries.

6. **Keyword Organization**:
   - The document provides a template for organizing keywords and creating a spreadsheet or Notion page to archive this content.
   - It also suggests generating HTML structures for a portfolio of these jams.

7. **Documentation Structure**:
   - The document includes sections on what the channel is about, audience targeting, upcoming content ideas, technical specifications, and metadata cleaning.
   - A table of contents provides an overview of the key points discussed in the document.

8. **License Information**:
   - The content is licensed under a Creative Commons Non-Commercial Share-Alike 3.0 license.

Overall, this document outlines a comprehensive strategy for maintaining a consistent and engaging music video series focused on electronic jamming and creative audio production techniques.

# coiler

 Link: [coiler]("../a/coiler.html")

The document titled "Motion" by Giovanni Marelli discusses the creation of a coil, which is used to wind a thin copper wire around magnets. This creates pickups for various applications.

# emacs

 Link: [emacs]("../a/emacs.html")

This document provides a comprehensive overview of the Emacs configuration file, detailing various features that enhance productivity, code management, collaboration, and AI integration within the software lifecycle. The setup includes customization and personalization options such as themes and font settings, extensive package management using MELPA for managing development packages, enhanced coding mode with support for multiple languages and interactive code execution, development tools like version control integration and shell interactions, project management features like Projectile and keybindings for common tasks, AI-driven assistance through tools like Ellama and Minuet, and custom functions and commands tailored to specific workflows. The document also includes a summary of the usage and importance of this configuration and provides the license information under CC by-sa-nc.

# flute

 Link: [flute]("../a/flute.html")

This document provides a detailed guide on how to calculate the placement of toneholes on a flute. It explains several variables that are important in determining the correct length and size of the holes for each note on the flute, including:

1. Effective tube length (L_eff): The theoretical length of the flute without end corrections or toneholes.
2. Speed of sound (v_sound): A crucial variable used to calculate the wavelength of a given note.
3. Actual tube length (A): The actual length of the flute that produces the correct note.
4. Tonehole correction factor (C): Determines how much each tonehole must be displaced from L_eff to produce the desired note.

The document also includes equations for calculating C and L_h, as well as instructions on how to determine the initial length of the flute (L_eff) for a specific lowest note based on its frequency and the speed of sound in the air. It provides a tool to update the chart for different temperature and humidity settings to accurately calculate L_eff.

The guide also includes a Tonehole Location Calculator that allows users to input their own specifications about their flute, such as actual length and diameter, to determine the correct placement of each tonehole for each note on the flute. The document concludes by emphasizing the importance of starting with small holes and gradually increasing them to achieve the desired pitch.

# lernia feature

 Link: [lernia feature]("../a/lernia_feature.html")

This document outlines several features of a library called "Lernia", which appears to be used for building models related to weather data. Here are the key points:

### Data Sources
- The library collects weather data from Dark Sky API.
- It also retrieves census data from Eurostat.

### Statistical Properties
- The document discusses analyzing statistical properties such as distribution, periodicity, autocorrelation, noise type, and decomposition of time series.

### Normalization
- Data is normalized to handle different scales and to improve model convergence. This includes min-max scaling and removing outliers.
- Correlation analysis is performed to remove derivable features.

### Feature Reduction
- Principal Component Analysis (PCA) is used to reduce the dimensionality of the data by identifying relevant sub-components.
- The 2D cross-correlation helps understand interactions between features, which can then lead to feature selection.

### Missing Values Handling
- NaN values are replaced using interpolation or dropping lines in Python, with special handling at boundaries.

### Data Cubes
- If multiple time series are available per location, the Chi-square distribution is used to identify outlier sequence windows and replace them.

### Feature Importance
- The document discusses different methods for calculating feature importance, including normalization and regularisation.
- Iterative model training helps in identifying important features by removing one feature at a time.

### Predictability
- The impact of feature cleaning on model predictions is analyzed using different models to ensure consistency.
- For spatial data, model performance improves after feature cleaning.

### Data Transformation
- Various techniques are discussed for transforming and compressing time series data:
  - Line fitting to simplify complexity
  - Dimensionality reduction with pictures
  - Interpolation for precise information
  - Distribution transformation for density estimation

### Boosting
- The distribution of residuals is analyzed after applying boosting, which allows training another model on the residuals.

### Categorical Variables
- Encoding options include One-Hot Encoding, Nominal Groups, Clustering, Hashing, Binary Encoding, Ordinal Encoding, Interval Encodings, and Contrast Encoder.
- Time-related categories like weekdays are grouped and stretched for better modeling.

Overall, Lernia focuses on data analysis and model building with a strong emphasis on normalization, feature reduction, and predictive performance optimization.

# mc amp

 Link: [mc amp]("../a/mc_amp.html")

The document "Motion" is titled "Motion" and was created by Giovanni Marelli on July 2, 2019. It is licensed under the Creative Commons Non-Commercial Share Alike 3.0 license in English (United States). The output format for the document is a Markdown file with strict formatting rules, backtick code blocks, automatic linking of bare URLs, and GitHub style syntax highlighting.

# R

 Link: [R]("../a/R.html")

The document titled "R" outlines my use of the R programming language in corporate roles from 2014 to 2017. The primary focus was on ETL (Extract, Transform, Load), data analysis, and data visualization, with a notable interest in creating visually appealing results.

### Key Points:

- **Language Used**: R was the main language used for data analytics and visualization.
- **Visual Outputs**: I produced several visualizations, including demographic, time series, geographic, affinity, and customer feedback plots. These images are available on GitHub.
- **Research and Projects**:
  - Worked on a comprehensive analysis using R for statistics and multivariate analysis.
  - Focused on forecasting and signal theory, integrating data from various industries.
- **Multivariate Analysis**: Techniques like PCA, factor analysis, and canonical correlation analysis were used to understand relationships among variables and reduce dimensionality.
- **Forecasting Methods**: ARIMA, exponential smoothing, and machine learning algorithms (like neural networks) were employed for time series forecasting.
- **Signal Theory**: Applications included stock market trends, noise reduction in audio/video files, and pattern recognition in medical images.

### Technical Details:

- **R Packages and Libraries**: Utilized a wide range of R packages and libraries tailored to statistical computing and data visualization.
- **Data Integration**: Integrated data from structured databases (SQL), unstructured data (text/images), and time series data for a holistic view of industry dynamics.
- **Industry-Specific Insights**: Provided actionable insights across various industries, including finance, healthcare, telecommunications, and supply chain management.

### Impact:

- **Actionable Insights**: Enabled businesses to make informed decisions by understanding complex datasets.
- **Risk Management**: Improved risk management through forecasting techniques in industries like finance and insurance.
- **Operational Efficiency**: Enhanced operational efficiency through signal theory applications in telecommunications.
- **Decision Support Systems**: Developed decision support systems that used historical data for predicting outcomes and recommending actions.

### Conclusion:

The document concludes by highlighting the multidisciplinary approach of using R to analyze and visualize data across multiple industries. This work demonstrated how R can provide comprehensive insights, drive innovation, and optimize operations in various sectors.

# data sets

 Link: [data sets]("../a/data_sets.html")

### Summary of `data_sets.md`

This document provides an overview of data sets used in various analyses. The main points include:

1. **Deci Second Data Analysis**:
   - Source: `etl_telemetry_deci.py`
   - Query: `network_log.sql`
   - Features to consider: `computing` and `vehicle_ping`.
   - Excluded features: `rtp`, `modem`, `ttl`, `interval_duration`, and `packets`.
   - Data is collected by subsetting `network_log` table, pivoted by modem name, and analyzed in time series plots.
   - Insights include correlation between modems' data, cellular 3 being the most stable operator, and different behaviors among vehicles.

2. **Dataset Preparation**:
   - Two datasets prepared: `latency_set` (August-September data) and `spike_set`.
   - Latency set has fewer spike events compared to the spike set.
   - Features included in each dataset are location, networking, vehicle dynamics, and computing.

3. **Spike Preprocessing**:
   - Query: `resample_1sec.sql`
   - Code: `etl_spikes.py`
   - Spike data resampled at 1-second intervals, with some missing values (~1%).
   - Peak identification and splitting of time series.
   - Artificial exaggeration of the peak to help model understanding.

4. **Spike Inspection**:
   - Analysis of spike events showing concurrent spikes on different cars.
   - Visualizing the relationship between `room_cpu` and spikes, indicating a clear variation prior to spikes.
   - Identified three pairs of cars with similar behavior before spikes.

5. **Feature Selection**:
   - Poor features identified based on low variance, frequency, and noise level.
   - Rich features like `rtp_lost`, `rtp_late` used as discriminators for latency analysis.
   - Feature correlation and interdependency analyses for better understanding.

6. **Feature Statistics**:
   - Visualization of time series for various features, including computing, networking, vehicle dynamics, and deci seconds.
   - Subsetting data prior to spikes and calculating log transformations to gain meaningful insights.
   - Analysis of variance to understand causal dependencies and regimes.

7. **Latency Statistical Properties**:
   - Periodicity and auto-correlation analysis of `camera_latency`.
   - Power spectrum analysis in normal and spike regimes.
   - Autocorrelation properties during spikes, indicating stability compared to normal behavior.

8. **Feature Normalization and Denoising**:
   - Importance of good normalization for model performances.
   - Flattening of outliers to ensure consistent normalization across predictions.
   - Denoising by averaging multiple time series where the spike happens at 0 second, providing a statistical understanding of the process.

This comprehensive overview outlines the data analysis processes and findings for various aspects of vehicle telemetry and network data.

# resume

 Link: [resume]("../a/resume.html")

The resume.yml file contains a summary of the following skills and experiences:

1. AI/generative solutions for cloud and on-prem:
   - Tech presales and service professional
   - Consults, teaches, and realizes ML/AI projects using modern solutions (cloud/on-prem)

2. Strategic data consultant/LLM:
   - Architects and delivers data infrastructure: storage, interfaces, middlewares, scheduler, messaging, security, redundancy, analytics, BI
   - Trains and implements language models with focus on email outreach

3. Director client data services/telco:
   - Leads technical implementation of afinti AI solutions for big European clients (telco, banking, media)
   - Manages remote teams assigned to customer projects in DE, DA, DS, AI, DB admin
   - Responsible in customer projects: pre-sales, feasibility study, metric design, data reliability, data analytics, performance monitoring, billing, financial reports

4. AI lead/mobility:
   - Developed a full stack (micro service based) solution for fleet dispatch
   - Defines most profitable task assignments for capable agents on the field
   - Demand forecast and customer patterns forecasting on telemetry data

5. Sr DS/mobility:
   - Interprets mobile data of 30M users and their mean of transportation
   - Product owner for product development of origin-destination matrices
   - Responsible for customer deliveries (mobility, advertising, real estate, commuter patterns)
   - Machine learning, insight highlights, and data monetization

6. Sr DS/advertising:
   - Data-driven advertising via audience segmentation on a large cross-device media network
   - Responsible for target quality and performance, inventory forecast, modeling, data visualization, and business intelligence
   - Tech consultant for user profiling built from web logs, CRM data, second-party enrichment, semantic engines, and SEO keywording
   - Represents my company for the big data project of the corporation

7. Data scientist/e-commerce:
   - Data-driven segmentation of price and ancillary teasers on lufthansa.com
   - Campaign design, tracking, revenue calculation, reporting, and tool concept development
   - Owner of 30+ A/B tests with 3M certified revenue uplift

8. Data consultant/ERP & BI:
   - Advising SMEs to organize and collect data in their companies, installing cloud-based ERP/CRM systems
   - Setting up a geo-based rural portal to connect professionals

9. Research assistant/biophysics:
   - Developed a parallel high-performance c++ suite for Monte Carlo and Molecular Dynamics simulations
   - OpenGL 3D visualization, ETL, data visualization, and reporting for biological-oriented questions
   - Publications: Influenza Fusion, String Method, Pore Formation

10. Education:
    - PhD in biophysics from UniGö
    - Master's degree in Nanoparticle stability in lipid membranes from UniPd
    - Bachelor's degree in Monte Carlo simulations of ion-defects' diffusion from UniPd

11. Training:
    - Tuning of parallel programs (Q3/12)
    - Management consulting & project management (Q3/13)
    - ERP setting up and programming (Q1/14)
    - Entrepreneurship: market, strategy, business plan (Q2/14)
    - HackItaly: 48h app dev (Q1/17)
    - Aws training courses (Q2/20)
    - Entrepreneurship program: blockchain in pharma (Q2/20)

12. Awards:
    - Fund for supporting cultural and creative ideas (Q3/13)
    - Ideas' competition Valsabbia e Garda (Q1/13)
    - Maker of merit (Maker faire Rome) (Q3/15)

# contact channel

 Link: [contact channel]("../a/contact_channel.html")

This document outlines various contact channels and their corresponding key metrics, uplift chances, and tracking mechanisms. It categorizes them based on the type of interaction:

1. **Offline Advertisement**: 
   - Usually difficult to reconcile until a purchase occurs.
   - Metrics: QR codes or dedicated landing pages.

2. **Online Advertisement**:
   - Most used metrics:
     * Click rate
     * Landing page
     * Purchase

3. **E-commerce**:
   - Most used metrics:
     * Banner click
     * Booking funnel
     * Purchase

4. **Chat**: 
   - Metrics not specified.

5. **Email**:
   - Domain warming is a process to send emails to recipients who perform positive operations (inbox placement, reply...).
   - Most used metrics:
     * Inbox placement
     * Bounce rate
     * Open rate
     * Reply rate
       * Positive reply rate

6. **Call Center**:
   - Most used metrics:
     * Number of calls
     * Purchase
     * Downgrade
     * Cancel

This document provides a comprehensive overview of different contact channels and their respective performance metrics, aiding in decision-making for improving customer engagement strategies.

# blindtest

 Link: [blindtest]("../a/blindtest.html")

This document is a technical report about the evaluation of a prediction model, primarily using customer data and activity counts. The main points are as follows:

1. **Model Representation**: The prediction model is represented by the equation \( x_{act}(t) m_{share}(t_d) = y_{ref}(t) + y_{out}(t) \), where:
   - \(x_{act}\) is the number of activities,
   - \(m_{share}\) is the market share,
   - \(y_{ref}\) are reference data (cachier receipts),
   - \(../../f/f_people\) is people per receipt,
   - \(y_{out}\) are people outside the shop,
   - \(t\) and \(t_d\) represent time and day respectively.

2. **Reference vs Reference**: To assess the model's capability, the report compares the model's output to a reference dataset generated by multiplying customer data with random noise. The plots show that when Gaussian noise is added, individual locations may have low correlation but the overall sum neutralizes it. Scores are calculated for different levels of Gaussian noise (50%, 90%), and final scores are shown on 30 days.

3. **Day Correlation Mapping**: 
   - Activities are calculated daily by considering a 20km previous distance filter.
   - The correlation between activities and reference data is evaluated using 6% of cilacs (close to a poi) with a correlation over 0.6.
   - A sum of activities over all countries is plotted, showing no day filtering initially but after filtering out bad days, weekdays are corrected, and a 2D correlation is performed between cilac patterns.

4. **Etl Process**: The ETL (Extract-Transform-Load) process includes low count filtering, weekday correction, filtering, and regression adjustments with the following steps: 00, 04, 22, 30, 41.

5. **Blind Test on Real Data**:
   - A performance comparison is shown between learning and play activities performed on the same days.
   - The smoothing process correlates neighboring events, improving the score in June.
   - The curve of improvement over time (June) is plotted.
   - Detailed scoring charts are provided for different learning steps and blind test scenarios.
   - Correlation maps over locations are also included.

Overall, the report details various aspects of the model's evaluation, from its theoretical representation to practical implementation and performance testing on real data.

# dsp

 Link: [dsp]("../a/dsp.html")

The summary of the document dsp.md is:

- Title: "Motion"
- Author: Giovanni Marelli
- Date: 2019-07-02
- License: Creative Commons Non-Commercial Share Alike 3.0
- Language: en-US
- Output format: markdown_strict+backtick_code_blocks+autolink_bare_uris+markdown_github

# index

 Link: [index]("../a/index.html")

The provided document appears to be a directory listing for a web-based documentation site. It contains various sections detailing projects and topics related to data science, engineering, modeling, and theory. The content is organized into several categories including:

1. **blog_main**: A section about the main blog or homepage.
2. **geomadi**: Geospatial analysis, focusing on graph creation, location intelligence, motorway stoppers, routing comparisons, and triangulation of sensor data.
3. **mallink**: Microservice-based optimization engine, covering antani concept overview, infrastructure design, microservice integration, KPI comparison, overview page, mallink optimization engine, and comparison with Routific.
4. **albio**: Machine learning for signals, with content on lernia feature selection, library overview, forecast with exogenous variables, time series forecast in production, and blind test on series forecast.
5. **ndoe**: Motion patterns, focusing on equations of motion, ride behavior, mobility concepts, capture rate for restaurants, activation potential, spatial utilities, quality on telemetry, data types for telemetry, feature relevance, forecast anomalies, prediction on telemetry, and spatial analysis.
6. **lernia**: Features and training, detailing the use of neural networks, machine learning models, and AI in industry for 2025 update.
7. **sawmill**: Data archiving and operations, covering data platform basics, data storage applications, data compliance, data modeling, security practices, webserver and networking, messaging system, middleware, cloud providers, CI/CD praxis, testing types, scheduling jobs, log processing, UI/data visualization for business.
8. **dev**: Development front-end/back-end (native), providing common programming practices, simulations, native visual applications, openGL, Python data exploration, ETL, R data exploration, visualization, and middleware to interact with relational databases.
9. **gen**: Generative AI projects, including painting with ML, text generation, music composition, agent naming environment, redundancy in natural images, and AI in industry updates for 2019 and 2023.
10. **intertino**: Marketing/sales/retention strategies, covering offer segmentation, agent compensation, lagged metrics, customer lifetime value, contact channels, and marketing applications.
11. **assesment**: Assessments and applications, including scooter movement, auto sensors, shared bike usage, UFO sightings, and weather prediction.

Each category contains several project descriptions with brief summaries of their objectives, key features, and the years they were developed (e.g., 2015-2023). The content is presented in a structured format using HTML and CSS for layout.

# cloud provider

 Link: [cloud provider]("../a/cloud_provider.html")

This document provides an overview of cloud providers and services used for different IT infrastructure tasks. Key points include:

1. **Cloud Providers**: The main players are AWS, GCP, Azure.
2. **On-Prem Deployment**: Involved manual setup and management.
3. **AWS Infrastructure Setup**:
   - VPC, Internet Gateway
   - Subnet with Public Routes
   - EC2 instance, Elastic IP
   - Security Groups (SSH, HTTP)
   - Additional steps like CloudFront for certificate activation and Load Balancing (ELB, Target Group, CloudFront Distribution)

4. **Filesystems**:
   - AWS S3, GCP Filestore, Azure Files, DigitalOcean Space

5. **Query Engine**: BigQuery from Google Cloud, Hive.

6. **Orchestration**:
   - Kubernetes, MicroK8s, OpenShift, Docker Swarm

7. **Spark Framework**:
   - EMR (AWS), Deltashare/AutoML (Azure), Databricks
   - MLflow, Kubeflow, Netflix Metaflow, Kedro, H2O AutoML

8. **Data Storage Solutions**:
   - RDS (Amazon), PostgreSQL (On-Prem)
   - MongoDB, DynamoDB (AWS)

9. **Instance Types**:
   - Elastic Map Reduce, EC2 Instances, Compute Engine (GCP)
   - Droplet (DigitalOcean)

10. **Machine Learning Operations**: SageMaker, MLflow, Kubeflow, Metaflow, Kedro, H2O AutoML

11. **Warehouse and Query Services**:
    - Athena, Redshift (AWS), BigQuery, Snowflake, Hadoop Hive

12. **Load Balancing Mechanisms**:
   - Celery, AWS Elastic Load Balancer, AWS API Gateway

13. **ETL/Batch Processing**:
    - Glue, Lambda, Apache Airflow, Pub/Sub (GCP)
    - YARN (Hadoop), Snowflake (Storage), DBT

14. **Logging and Tracking**:
    - Elasticsearch, Kibana/Grafana (On-Prem)
    - AWS CloudWatch, Prometheus

15. **Cloud Monitoring Tools**:
   - Datadog
   - Terraform for Infrastructure as Code

16. **Messaging Solutions**:
    - Apache Kafka, Redpanda, AWS Kinesis

17. **Business Intelligence Tools**:
    - Metabase, Superset (On-Prem), PowerBI/Tableau (Azure)

The document provides a detailed overview of how these cloud services can be utilized for various IT tasks, from application deployment to data management and analytics.

# video presentation

 Link: [video presentation]("../a/video_presentation.html")

The document, video_presentation.md, appears to be a comprehensive overview of a collection of audio and video recordings related to various creative projects and experiences. The main content is divided into several sections:

1. **Header Section**: The title "Dawless Jam Electro Archive - The Collection" at the top provides an overview of the archive's name and its purpose.

2. **Featured Video Section**: This section features a single video titled "Austrian Camp 'Tornate per Ultimi' & Aira P-6". It describes a musical improvisation session from an Austrian front camp, including timestamps for different scenes and the instruments used in the performance.

3. **Collection Archive Section**: This is a main part of the document where various audio and video recordings are listed across different locations and topics. Each entry includes:
   - **Location / Topic**: Where the recording took place or what the focus was.
   - **Description / Moments**: Descriptions of the content captured, often focusing on soundscapes, environments, or specific events.
   - **Equipment / Style**: Lists the equipment used in each session and the style of music or creative techniques employed.

4. **Technical Specs Section**: This section provides a summary of the standard setup used for most videos in the archive, including keyboards, sequencers/keys, VCA/Processors, cinematics, cameras, effects, sampling devices, and mixing tools.

5. **Footer Section**: The footer credits the document's creation based on metadata provided and notes that all equipment was used for live improvisation and workshop settings.

Overall, this document serves as a directory of creative work and experiences in electronic music, video production, and sound recording techniques across various locations and contexts.

# tech stack

 Link: [tech stack]("../a/tech_stack.html")

The tech stack listed in `tech_stack.md` from the directory includes:

1. **Data Integration**: Airbyte (https://lnkd.in/ex_NT8p8)
2. **Pipeline/Workflow**: Prefect (https://lnkd.in/e9BH4kTx)
3. **Data Transformation**: dbt (https://lnkd.in/ejfCg3UX)
4. **Dashboard**: Lightdash (https://lnkd.in/dbBWnGZj)
5. **Quality Assurance**: Great Expectations (https://lnkd.in/e-49gzUx)

# agent compensation

 Link: [agent compensation]("../a/agent_compensation.html")

This document provides an overview of agent compensation in a company setting, focusing on how it motivates agents and leads to better outcomes for both the company and individual agents.

The main points are:

1. **Save Rate**: The primary target is the save rate (the percentage of calls resulting in successful retention).

2. **ETL Process**: Data is extracted using SQL queries and converted into a continuous format. Categorical features are also converted to numerical values for better model performance.

3. **Data Quality**: The dataset includes missing and outlier values, which were addressed by typecasting the data types and not applying transformations.

4. **Feature Engineering**: Customer dimensions such as last bill amount, pre-call tenure, package hierarchy, and product category are analyzed to identify their impact on save rate.

5. **Sampling Shuffling**: The document discusses a test to ensure there is no bias in how calls are distributed among agents (e.g., homemovers vs. no transfer calls). 

6. **Modeling**: Various machine learning models were tested for predicting save rate, but the results showed subpar performance.

7. **Latent Variables**: Agent skill is treated as a latent variable and modeled using a hierarchical Bayesian approach. Agents are simulated in a tournament setting to assess their ability.

8. **Game Theory**: The document uses game theory to understand how different compensation schemes can influence agent behavior and company outcomes.

9. **Compensation Model**: The model assigns a reward based on the user's value, risk of call failure, or success probability. It aims to incentivize agents to focus on high-value customers and difficult calls.

10. **Simulation**: A simulation is conducted using different compensation models to evaluate their impact on company revenue, agent compensation, and customer retention.

11. **Tuning**: The document discusses tuning parameters like agent commission and engine influence to increase motivation and effectiveness.

Overall, the document provides a comprehensive analysis of agent compensation strategies and their effects on business outcomes, highlighting areas for improvement and suggesting new models that can lead to better results.

# train reference

 Link: [train reference]("../a/train_reference.html")

The document describes a process for correcting data from sales receipts into daily and weekly visit counts at gas stations. The corrections include handling missing values, smoothing hourly variations, controlling volatility, using deep learning to detect non-predictable locations, adjusting for holidays, accounting for missing source information, considering extrapolation factors for motorway drivers, analyzing market share on the motorway, controlling weather effects, distinguishing commuter vs touristic traffic patterns, adjusting for population density, dealing with direction distinction uncertainty, filtering trip distances, addressing low counts, identifying device type, and considering the number of people per car vs receipt. The process uses statistical properties and models to predict and adjust the data to better align it with reference visit counts.

# monte carlo

 Link: [monte carlo]("../a/monte_carlo.html")

The provided text is a markdown file titled "monte_carlo.md" located in a directory. The content seems to be incomplete, as it lacks actual text or information about the Monte Carlo method and its configurations. Without more details or context, I cannot provide a comprehensive summary or summary of what might be contained in this document.

# skills

 Link: [skills]("../a/skills.html")

The document `skills.yml` from the directory contains a structured list of skills categorized under different topics. Here is a summary of the skills:

### Languages
- Native: Italian
- Fluent: English, German, Spanish (Intermediate)
- Intermediate: French, Portuguese

### Programming
- Python
- JavaScript
- C++
- C
- R
- Spark
- Go (Viz) OpenGL
- Qt
- GTK+

### Machine Learning
- TensorFlow
- Keras
- scikit-learn
- scipy
- caret
- PyTorch

### AI
- Generative Adversarial Networks (GANs)
- Reinforcement Learning
- Forecasting and Predictions
- Classification

### Web Development
- HTML5, CSS3
- JavaScript (D3.js, React, Angular)

### Server Management
- FastAPI, Celery, Redis, Nginx, Traefik, Node.js, PHP

### Databases
- SQL
- PostgreSQL
- Cassandra
- MongoDB
- Neo4j
- Elasticsearch (FS) HDFS S3

### Development Tools and Methods
- Git, GitLab, SVN
- CI/CD
- pytest
- Docker

### Production Infrastructure
- Docker Swarm, Kubernetes
- Airflow, Kafka, Presto, Terraform

### Visualization Tools
- Kibana, Grafana, Metabase, Power BI, Tableau

### IoT
- MQTT, Mosquitto, Arduino, ESP32, Teensy, Seeed, Raspberry Pi, Jetson

### Numerical Computing
- NumPy, GSL
- CGAL
- MATLAB, Octave, Maple, ROOT (Grid) MPI, OpenMP

### Software Development Tools
- QGIS (Visualization), Mayavi, POV-Ray (CAD/3D), Rhino, Blender, CURA (Slicer)

### Large Language Models (LLMs)
- RAG, GraphRAG, LaunchChain, LangSmith, LlamaIndex

### Cloud Services
- AWS: S3, IAM, EC2, SageMaker, Bedrock, ECS, CloudFront, Lambda, Athena
- GCP: BigQuery, Kubernetes, Pub/Sub, Gemini
- Azure: Factory, Kusto, ML Studio, Synapse, Databricks, Cosmos
- NVIDIA: CUDA, Ominverse, Morpheus, Nemo, Nim, TensorRT, Triton
- Cisco: UCS, Meraki, Splunk

This comprehensive list provides a detailed overview of the skills and tools possessed by an individual or team, covering various domains from language fluency to cutting-edge AI technologies and cloud infrastructure management.

# generative

 Link: [generative]("../a/generative.html")

This document describes the development and testing of a generative neural network model, specifically focusing on image processing techniques such as face detection, filtering, and transformation. The key points include:

1. **GAN Architecture**: A Generative Adversarial Network (GAN) is used to transform images into desired outputs. This involves an encoder and decoder, where the encoder reduces the image's dimensions while preserving its essential features, and the decoder reconstructs the original or transformed image.

2. **Face Detection and Rescaling**: The document mentions using Haar cascades for face detection and rescaling pictures to a consistent size of 360x480 pixels, addressing issues with erroneous face detections.

3. **Image Filtering**: Various filters are applied to each image, including color binary thresholds, contours, Canny edge detection, and grayscale conversion, which collectively enhance the image quality.

4. **Training Procedures**: Different types of training sequences are conducted:
   - **Autoencoder**: To check if the generator is capable of describing the final result.
   - **Gray to Color Transformation**: A model learns to convert grayscale images into color images through multiple epochs.
   - **Color Filters**: Layers with different binary thresholds are used to train the encoder toward the original picture.
   - **Contours and Canny Edge Detection**: These techniques improve image details and edge detection, but they require significant epochs for convergence.

5. **Average Face/Expression Morphing**: An average morphing technique is applied to multiple images within a subset to produce an overall averaged face or expression.

6. **Noise Input Testing**: Random noise input testing shows the model's ability to generate pure generator outputs without any predefined patterns.

7. **Further Trials and Results**: The document highlights notable outcomes from AI-generated faces, showcasing various artistic transformations.

8. **Super Resolution**: While not detailed here, it mentions using super-resolution techniques with a GAN architecture.

9. **Model Architecture**: Describes the architecture of both the generator and discriminator in detail, including convolutional layers, pooling, batch normalization, and dropout to prevent overfitting.

The overall goal is to develop a robust generative model capable of transforming images into various styles or expressions based on the input filters and training procedures described.

# queries

 Link: [queries]("../a/queries.html")

This document provides a comprehensive guide on SQL queries, covering various operations such as selecting data, filtering and subsetting, ordering and grouping results, unique values, functions, views creation and modification, table deletion, column type selection, data swapping, wildcard use, variable usage, date range filtering, joins, unions, comments, database and table creation, and modifications.

# forecast

 Link: [forecast]("../a/forecast.html")

The document `forecast.md` from directory `/src/forecast_spike.py` describes a spike forecasting model based on camera latency data. Here is a summary of the key points:

### Model Overview

1. **Prediction and Forecast**: The model starts by making a good prediction for the next spike in the camera latency data.

2. **Training Process**:
   - All peaks are flattened at 300ms.
   - Features are normalized between -1 and 1, excluding the 5th and 95th percentile with outliers interpolated.
   - The model is trained over various epochs on different subsets of the data:
     - Full dataset
     - Denoised series using rolling windows
     - Single series using rolling windows
     - Cross-validating single series
     - Denoised series using rolling windows

3. **Forecasting Techniques**:
   - **Denoised Series**: The model trains to forecast spike advance times until the correct prediction is achieved.
   - **Single Series**: Iterates over every single series and forecasts from each `from_peak` value, considering maximum latency.

4. **Feature Analysis**:
   - Feature importance analysis using knock-out techniques.
   - Model validation using a pre-trained model on calendar week 39 with rolling windows of 6 seconds.

5. **Comparison with Alternatives**:
   - Naive forecasting models are compared to Facebook Prophet, MLP regressor, and ARIMA for peak prediction, showing poor performance due to the abrupt nature of spike arrivals.

### Key Visualizations

- Plots showing training history, forecast advance effectiveness, prior forecast, rolling forecasts, maximum forecast, latency maximum forecasts, and confusion matrices.

This document outlines a comprehensive approach to forecasting camera latency spikes using machine learning techniques, highlighting the importance of feature normalization and model validation.

# midi hub

 Link: [midi hub]("../a/midi_hub.html")

Sure, here is a summary of the document `midi_hub.md` from directory:

The document titled "Motion" is authored by Giovanni Marelli and was last updated on July 2, 2019. The content of this document is licensed under the Creative Commons Non-Commercial Share Alike 3.0 license. The language used in the document is English (en-US). The output format for the document is specified as an Markdown file with specific variants: `markdown_strict+backtick_code_blocks+autolink_bare_uris+markdown_github`.

# javascript

 Link: [javascript]("../a/javascript.html")

### Summary of JavaScript Projects

1. **React Native**: You have experience with asynchronous functions, Redux-Form for managing forms, performance optimization techniques such as memoization and lazy loading components, state management using Redux and Context API, and writing unit tests using Jest and React Testing Library. Your projects focus on handling user input, fetching data from APIs, maintaining application state, and ensuring app performance.

2. **Node.js**: You have worked with Express.js for creating RESTful APIs, integrated databases like MongoDB and MySQL, implemented error handling, asynchronous programming using promises and async/await, and security measures like authentication and data validation. Your projects include implementing user input forms, managing application state efficiently, and ensuring the security of your applications.

3. **React**: You have used Formik for form management, Redux and Context API for state management, written unit tests using Jest, ensured responsive design, deployed React applications to platforms like AWS or Vercel, and set up CI/CD pipelines. Your projects focus on handling forms, maintaining application state, ensuring the quality of components, and optimizing performance.

4. **Angular**: You have used Protractor for end-to-end testing, Jasmine and Karma for component testing, implemented security measures like authentication and input validation, optimized Angular applications for performance, and deployed Angular applications using tools like Angular CLI and CI/CD pipelines. Your projects focus on implementing user interface components, ensuring application security, maintaining application state efficiently, and optimizing performance.

### Overall Recommendations

- **Documentation Learning**: Always ensure to understand the official documentation of libraries and frameworks you use.
  
- **Code Reviews**: Regularly review your code with peers or mentors for best practices and improvements.
  
- **Continuous Learning**: Stay updated with new technologies and patterns in JavaScript development. Attend workshops, meetups, and online courses to keep up with the latest trends.

By following these recommendations, you can enhance your skills and create more robust applications across different platforms.

# lagged metrics

 Link: [lagged metrics]("../a/lagged_metrics.html")

This document describes a project that investigates the differences between on-call and lagged metrics. The main findings are:

1. Lagged metrics consider a time span of 25 days when customers could call again, resulting in a loss of around 10% customers.
2. Several different metrics are used to predict, including on-call and lagged metrics.
3. The features have been cleaned and normalized for distribution comparison.
4. Feature independence was checked using correlation plots, overlay distributions were compared with saved/lost customers, and joyplots showed the distribution of features.
5. Predictive models were built for both on-call and lagged metrics, with confusion matrices provided for evaluation.
6. Features were knocked-out to calculate their relative importance in comparison to the on-call model, and this was done again for the lagged model.
7. The relative difference between feature importance in the on-call and lagged metrics was calculated using a visualization that shows how it evolves week by week.
8. A lift analysis was conducted based on categorical metrics, showing how the relative importance of these metrics compares to non-categorical metrics.

Additionally, the document discusses cohort reshuffling, where the association of agents per area varies over time and shuffling among cohorts is demonstrated using a Sankey diagram.

# company tools

 Link: [company tools]("../a/company_tools.html")

The document "company_tools.md" from the directory contains a list of important productivity tools for a small company, including:

1. ERP and CRM systems like Odoo.
2. Static web pages and graphics for branding.
3. Backend data storage solutions like Airtable.
4. Shared folders using WebDAV, NAS, or NextCloud.
5. Customer feedback mechanisms.
6. Marketing design tools like Canva.
7. Automation workflows with Zapier.
8. Payment processing using Stripe.
9. Newsletter services like Substack.
10. Landing page creation platforms like Intercom.
11. Project management tools like Trello and Odoo.
12. Marketing channels like Product Hunt and Product Roadmap.
13. Knowledge base solutions like Notion.
14. Email marketing services like Mailchimp.

The document also mentions some open-source projects such as Great Expectations, Lightdash, dbt-core, PrefectHQ, and Airbyte. The licensing information for the content is CC by-sa-nc (Creative Commons Non-Commercial Share Alike 3.0).

# webserver

 Link: [webserver]("../a/webserver.html")

This document provides a detailed overview of web server configurations, experiences using various web servers, and setup for SSL certificates using Let's Encrypt. The main focus is on deploying Wikimania as an example.

**Apache**: A lightweight, fast, and reliable web server but more complex to configure and test. It is not discussed in detail due to its complexity.

**Nginx**: Similar to Apache but easier to configure and test. It provides a default website configuration and can be extended with additional configurations using the `conf.d` directory.

**Traefik**: A reverse proxy that offers web server capabilities. However, it is noted that it may not be completely reliable, especially regarding secure redirects. The document includes an example configuration file.

**Certificates**: Let's Encrypt certificates are used for securing web traffic. Certbot is used to obtain and renew these certificates. There's a sample command for running Certbot using Docker Compose.

**PHP**: A popular server-side scripting language integrated with web servers like Nginx or Apache. The document provides instructions on setting up a PHP environment within a Docker container, including extensions such as GD and PDO.

**Webserver Configuration**: The document explains how to route PHP requests to the appropriate web server (either Nginx or Apache) by using upstream configurations in Nginx.

**Load Balancing**: Although not directly discussed, the presence of Redis and Celery suggests that load balancing and distributed processing are important considerations for a production environment.

# data viz

 Link: [data viz]("../a/data_viz.html")

**data visualization**

Different data visualization tools and practices are discussed in the document. Some examples include:

1. Feature importance: ![feature importance](../portfol../../f/evaluate_data.png "feature importance")
2. Prediction results: ![prediction](../portfol../../f/learn_process.png "prediction results")
3. Socio-demographic characteristics: ![demographics](../portfol../../f/socio_demo.png "socio demo")

D3.js is mentioned, with several examples published on [anticolo's website]: 
- Overview: ![d3](../portfol../../f/d3viz.png "d3 overview")
- Network visualization: ![network](../../f/f_stage/viz_network.png "network")
- Heatmap visualization: ![heatmap](../../f/f_stage/viz_heatmap.png "heatmap")
- Sunburst visualization: ![sunburst](../../f/f_stage/viz_sunburst.png "sunburst")
- Circle pack visualization: ![circle pack](../../f/f_stage/viz_circlePack.png "circlePack") and ![circle pack](../portfol../../f/data_viz.png "circle pack")
- Treebox visualization: ![treebox](../../f/f_stage/viz_treebox.png "treebox")
- Taxonomy visualization: ![taxonomy](../portfol../../f/taxonomy.png "taxonomy")

The document also covers:
1. Maps (Python examples): ![movement](../portfol../../f/motion_pattern.png "motion patterns") and ![activation](../portfol../../f/activation_area.png "activation area")
2. Tools like Metabase (Docker) and Kibana are mentioned.

# restaurant

 Link: [restaurant]("../a/restaurant.html")

### Summary of Restaurant Guests Document

The document focuses on predicting restaurant guests from telco data. It outlines a methodology that involves several key steps and uses various metrics to understand the relationship between telco and reference data.

1. **Objective**: Predict restaurant guests using telco data.
2. **Model Representation**: The model is represented as \( g_{receipts}(t) = c_{rate}^a(t)a_{act}(t) + c_{rate}^f(t)a_{foot}(t) + b_{bias}(t) \), where activities and footfall are not independent.
3. **Data Enrichment**:
   - **Degeneracy**: Measures the recurrency of points in a spatial region.
   - **Population Density**: Incorporates official statistical data such as population density, men/women asymmetry, foreigner percentage, flat density, land use, and age asymmetry.
4. **Isochrone Calculation**: Calculates isochrones to determine travel times and distances.
5. **Footfall Estimation**: Estimates footfall on a regular grid using routing data.
6. **Other Metrics**: Includes street statistics like bast counts, bast weekend factor, etc.
7. **Time Series Preprocessing**: Substitutes anomalous points with averages.
8. **Sensor Mapping**:
   - Calculates sensor cross-correlation and selects consistent sensors.
   - Runs linear regression to estimate sensor activities versus visits.
9. **KPI Calculation**:
   - Computes correlation, relative difference, and relative error metrics.
10. **Regression Analysis**:
    - Performs country-wide and location-specific regressions on activity and footfall data.
    - Compares different models (country-wide, site-specific) for performance.
11. **Feature Selection**:
    - Selects features based on variance distribution to simplify the parameter space.
12. **Feature Knock-out Analysis**:
    - Analyzes feature importance by removing each one and measuring performance change.
13. **Daily Visits Prediction**:
    - Uses a regressor to predict daily visits from geographical data.
14. **Time Series Prediction**:
    - Utilizes long short-term memory (LSTM) with Keras for time series forecasting.

### Key Points
- The model is based on the interaction of activities and footfall, influenced by various location features.
- Data enrichment is crucial to capture the underlying relationship between telco data and reference data.
- Regression techniques are employed to estimate visitor counts from geographical data.
- Feature selection and knock-out analysis help identify important predictors for the model.
- LSTM models demonstrate good performance in forecasting time series data.

Overall, the document provides a comprehensive approach to predicting restaurant guests using telco data and leveraging various advanced statistical and machine learning methods.

# neural networks

 Link: [neural networks]("../a/neural_networks.html")

### Deep Learning Concepts

Neural networks consist of interconnected neurons that learn from data, transforming inputs into outputs through layers of activation functions. These networks include a forward pass for prediction and backward propagation to update weights based on errors.

#### Data Splitting

Training, validation, and testing sets are essential for model evaluation:
- **Train**: Used for training the network.
- **Validation**: Helps in tuning hyperparameters without overfitting.
- **Test**: Ensures final performance is unbiased.

#### Feedforward Network

A typical feedforward network follows this flow:
1. Input layer ($X$) with dimensions $nxm$ and a target variable $y$ of size $k$.
2. Weight vectors ($w_1$, $w_2$, $w_3$), biases ($b_1$, $b_2$, $b_3$), and activation function (e.g., ReLU).
3. Layers compute activations: 
   - $z_1 = g_1(w_1X + b_1)$
   - $z_2 = g_2(w_2 z_1 + b_2)$
   - $z_3 = g_3(w_3 z_2 + b_3)$
4. Predicted output: $\hat{y} = softmax(z_3)$

Parameters to set: ${w_1, w_2, w_3, b_1, b_2, b_3}$.

#### Layers and Functions

Network layers often include:
- **Input layer**: Formats data as tensors.
- **Normalization**: Scales inputs between 0 and 1 or -1 to 1.
- **Convolutional layers**: Apply filters on input neurons.
- **Pooling layers**: Reduce spatial dimensions for feature extraction.
- **Activation functions**: Sigmoid, TanH, ReLU, Leaky ReLU, Parametric ReLU, Softmax, Swish.
- **Dropout**: Randomly deactivates neurons to avoid overfitting.

#### Batch Processing

Each training iteration processes a batch of examples.

#### Activation Functions

Activation functions:
- Sigmoid (logistic): Smooth gradient and binary classification.
- TanH: Zero-centered output for better negative value handling.
- ReLU: Fast convergence, non-linear, vanishing gradient problem.
- Leaky ReLU: Prevents dying ReLU, consistent predictions for negative inputs.
- Parametric ReLU: Learns the negative slope for flexibility.
- Softmax: Multi-class classification probabilities.
- Swish: Improved performance over ReLU.

#### Cost Functions

Cost functions:
- Squared error: Regression loss function.
- Logistic function: Classification loss using sigmoid activation.
- Cross entropy loss: Loss for multi-class classification.
- Hinge loss: Support vector machine loss.

#### Scores and Metrics

Evaluation metrics include:
- Classification Accuracy
- Sensitivity, Specificity
- Precision, Recall
- F1 Score
- Logarithmic Loss
- Area Under Curve (AUC)
- Mean Absolute Error, Mean Squared Error
- Language models: Rouge score

#### Backpropagation

Backpropagation adjusts weights to minimize error:
- Minimizes cost function $f(x,y)$ using an optimizer.
- Optimizers like gradient descent and stochastic gradient descent are used.

#### Bias and Variance

Models can have overfitting (high variance) or underfitting (high bias):
- Regularisation techniques help balance model complexity.

#### Feature Regularization

Regularisations include:
- L1, L2, Elastic Net
- Pruning: Removing branches in decision trees

#### Dropout

Dropout randomly deactivates neurons to prevent overfitting:
- Binary classification results for dropout 30.
- Overfitting occurs with dropout 50.

#### Data Augmentation

Data augmentation increases dataset size:
- Examples are rotated, resized, or filtered to handle non-standard cases.

#### Batch Normalization

Batch normalization normalizes inputs during training:
- Prevents significant distortions in distribution of min/max values.

#### GANs

Generative Adversarial Networks (GANs) use an encode-decode architecture with attention layers and enhanced embeddings:
- Separated article on [GANs](generative.html).
- Keras implementations available at [keras-gan](https://github.com/eriklindernoren/Keras-GAN).

# series prod

 Link: [series prod]("../a/series_prod.html")

This document describes a forecast delivery pipeline for a project that uses pretrained models. It includes setup instructions for creating an ad hoc container, installing basic libraries, and preparing data for training and prediction. The pipeline involves checking data availability, submitting jobs to a cluster, processing data using Jupyter notebooks, applying mapping and regression scripts, calculating KPIs, organizing internal meetings, finalizing the delivery, and providing customer support.

# music evaluation

 Link: [music evaluation]("../a/music_evaluation.html")

The document "music_evaluation.md" discusses evaluating music bands and their songs in a contest. There are 600 bands, with each band having 3 songs to evaluate. The final 6 bands are accepted based on a score system. 

To ensure an accurate evaluation, criteria for sorting and comparing songs by genre are needed. A quantitative measure of quality is discussed, using a classical scoring system from 1 to 10 with 5 groups of judges evaluating 120 bands. Each band's total score is the mean score of their three songs.

The document provides an image of an app used for music evaluation and defines criteria for evaluating songs by melody, text, sound, master, singing, accompaniment, arrangement, rhythm, and bonus. The evaluation should be normalized by genres to ensure fair comparison between different genres. The document also discusses the limitations of a simple arithmetic sum score system and proposes using mean subtraction to improve the fairness of rankings.

# prediction

 Link: [prediction]("../a/prediction.html")

This document summarizes several data analysis and forecasting tasks for an internet-related project. It covers the following key points:

1. **Data Analysis of Historical Data**: The document discusses analyzing monthly, weekday, and week-and-festivity occurrences from historical time series data using box plots. This helps in understanding the distribution and variability in different time periods.

2. **Data Sources**: It outlines how to collect and organize source data, including an image of a histogram showing inventory history details and another for exposing data via API.

3. **Time Series Analysis Properties**: The document presents statistical properties such as autocorrelation and cross-correlation, along with the characteristic time scale. This analysis helps in understanding the patterns and dependencies within the time series data.

4. **Forecasting Techniques**: It describes using ARIMA (AutoRegressive Integrated Moving Average) for time series forecasting. There are animated GIFs illustrating how this model works, including autocorrelation simulation and periodic continuation of the time series.

5. **Monitoring**: The document mentions showing attributes per location and monitoring performances using animations like overlapped audiences and performance charts.

Overall, the document provides a comprehensive overview of data analysis, forecasting, and monitoring techniques used in an internet-related project.

# messaging

 Link: [messaging]("../a/messaging.html")

The document "Messaging" describes how messaging systems work, including producers and consumers, and their arrangement into topics. It also provides a link to a middleware in Python for publishing and consuming messages from a topic, with endpoints for producing, consuming, getting the latest messages, starting from a given time, showing the Kafka stream, deleting topics, listing topics, displaying swagger documentation, and providing an application user interface.

The document also explains how Kafka is deployed using a Docker Compose file. This includes Zookerper which stores topic contents in volumes, Kafka engine which requires careful definition of listeners, including internal and outside listeners with plaintext security protocol, and Kafka UI for monitoring the topics and brokers.

It further mentions Mosquitto, designed for IoT where many devices are sending information to a central server and user applications can consume topics and run analytics. Lastly, it briefly discusses Kinesis and pubsub systems.

# motorway

 Link: [motorway]("../a/motorway.html")

This document describes the motorway stoppers use case, which aims to identify isolated gas stations and distinguish drivers' directions on the motorway. The steps involved in the project are:

1. **Data Collection**: Collect data on customer activities (gas station visits) and vehicle movements.
2. **Data Cleaning**: Filter out non-motorway-related activities and activities outside the study period.
3. **Distance Filtering**: Apply filters based on trip duration, previous trip distance, and direction to select potential motorway stoppers.
4. **Direction Distinction**: Use chirality (orientation) to distinguish drivers' directions from different sides of the motorway.
5. **Shape Clustering**: Cluster locations based on their activity patterns.
6. **Scoring and Filtering**: Calculate scores for each location using correlation, regression, and difference metrics. Filter locations with high scores based on a threshold.
7. **Data Enrichment**: Add geographic information to enrich location data.
8. **Correction Factors**: Adjust results based on environmental variables such as population density and number of sources.
9. **Count Correction**: Use bagging regressors on decision trees to correct counts mismatch.
10. **Result Visualization**: Generate a correlation map, show results per location, and calculate capture rates.

The project involves several steps, including data preprocessing, filtering, clustering, scoring, enrichment, correction, visualization, and result generation. The final goal is to identify isolated gas stations and distinguish drivers' directions on the motorway based on customer data.

# routific

 Link: [routific]("../a/routific.html")

This document describes the use of Routific for distributing tasks to drivers. However, it highlights several limitations with Routific:

1. It does not improve on revenue.
2. It does not optimize on total drive time.
3. Changing task priorities affects routes but not graphs.

The author compares Routific's performance with an optimization engine that assigns tasks to a fleet. They created a setup of 600 spots, 6 task types, and 8 drivers.

The visual inspection shows that Routific routes often mix internal intersections and cross streets where there are fewer available parking spaces. It also has sequences that don't make sense and skips important priorities in the city center. Long deviations occur for driving on tunnels or when the scooter is on the ground.

Additionally, even with priority 1 over all tasks, Routific still returns routes that do not make sense. The document concludes that Routific can return more stops than the number of tasks and may cheat by returning a total drive time instead of actual driven distance.

# offer segmentation

 Link: [offer segmentation]("../a/offer_segmentation.html")

The document "offer_segmentation.md" discusses several aspects of customer profiling, pretargeting, touchpoint crossing, and revenue/bidding in online marketing. It provides a detailed methodology for analyzing user behavior, optimizing offers, and improving the effectiveness of marketing campaigns.

Here are some key points from the document:

1. **Customer Profiling:**
   - The document discusses how to identify customer segments using environmental parameters such as behaviour, item selection, time, source, location, session, class, travel/specific.
   - A learning process is proposed for correlating segment performance with specific variables using a Bayesian approach.

2. **Touchpoint Crossing:**
   - Offers are tracked across different touchpoints to understand customer decision-making throughout their journey.
   - Negative offer performances are also considered to gain insights into customer confidence in various scenarios.

3. **Pretargeting:**
   - The document introduces a parallel approach for computing user grouping in web marketing using masks that characterize user experiences, web sites, and campaigns.
   - Each mask is represented on a 2D plane with labels and points, and masks for web sites and campaigns are calculated by refining groups in asynchronous steps.

4. **Peripherical (Parallel) Approach:**
   - User experience masks are created by summing the relevance of ads and web pages.
   - The document describes how to perform convolution operations on these masks to find the best fitting opportunities for ads.
   - Each separated computing unit communicates user experience matrices and preferences to a central unit.

5. **Central (Parallel) Approach:**
   - The central unit computes user information by assigning vectors to each mask.
   - It performs cluster analysis, refine web and ad masks, and sends new values to external units in asynchronous time.

6. **Infrastructure and Scalability:**
   - The document outlines the architecture of the infrastructure with multiple computing units for parallel processing.
   - The system is designed to handle large volumes of users (50M), views (10G), URLs (1M), and pages (10k).
   - It mentions that calculations are performed on native machines via Python or C++ code, and cookies are analyzed after their last update.

7. **Revenue/Bidding:**
   - The document presents methods to calculate the cumulative probability of revenue based on click-through rates (CPO), cost-per-click (CPC), and cost-per-mille (CPM).
   - It discusses how to select offers using random numbers and a cumulative probability function related to distance from the center mask.

8. **Refinement:**
   - The document introduces refinement techniques, such as assigning distances of ad masks to cluster masks and selecting ads based on cumulative probabilities of these distances.
   - It also mentions interest filtering using user grouping to help users filter complex content in web sites.

9. **Customer Feedback Score:**
   - The document describes how feedbacks from customers are analyzed to extract sentiment and relevant words.
   - Sentiment recognition is used to understand customer feedback by identifying common words associated with different topics.

10. **Anonymous Offer Optimization:**
    - The document discusses session variables and the revenue function for ticket bookings, including ancillary sales and conversion steps.
    - It proposes methods for variant testing (split-page optimization) using t-tests and chi-square tests to determine winning variants.
    - It also presents metric noise propagation techniques to evaluate the reliability of booking frequencies.

In summary, the document provides a comprehensive framework for customer profiling, pretargeting, touchpoint crossing, revenue/bidding, and offer optimization in online marketing.

# mini hub

 Link: [mini hub]("../a/mini_hub.html")

### Mini Hub Project Overview

**Objective**: Assess the convenience and cost-effectiveness of mini hubs in last-mile deliveries compared to van2door delivery methods. If mini hubs are more convenient, they could offer a competitive price model.

**Scope**: The project focuses on determining the best spots for mini hubs, operational advantages, and comparing costs of different scenarios (van2door vs. van2hub + cart2door).

### Mini Hub Types

Mini hubs can be of three types:

1. **Rented Areas**: Cost: €3k/month / 2k packages
2. **Minimarkets**: Free capacity
3. **Lockers**: Variable cost, typically €0.5 per package with a max capacity of 30 packages

### Key Benefits of Mini Hubs

- Avoiding van delivery door-to-door traffic, parking issues, and bad timing.
- Matching the delivery time more accurately.
- Reiterating deliveries efficiently.
- Redistributing workforce to minimize vehicle expenses.

### Simulation Variables

For precise calculations:
- **Transportation Options**: Models transportation costs for vans and carts with different speeds and operation times.
- **Delivery Time**: Simulates delivery times within the day, focusing on early stages.
- **Cost Components**: Includes driver salary, vehicle cost (maintenance, renting), and fuel/electricity costs.

### Methodology

1. **Objective**: Compute and compare the costs of different operation schemes to find the most convenient location and size of mini hubs.
2. **Simulation Steps**:
   - Simulate orders across the city randomly.
   - Use routing graphs for vans and carts.
   - Calculate delivery times and distances.
3. **Steps**:
   - Generate orders.
   - Assign them to pickup stores.
   - Route pickups to mini hubs.
   - Route mini hubs to doors.

### Preparation

- Uses geomadi library to download and subset a graph for Berlin.
- Calculates geohashes with precision 8 and assigns unique nodes.
- Precomputes routed distances from geohash to geohash for vans and carts.

### Results

The simulation provides the following results:

| nr_hub | distance pickup/hub | distance hub/door | `p` from pickups | `p` from hub | time pickup/hub | time hub/door |
|--------|-------------------|-----------------|--------------|-------------|-----------------|---------------|
| 155     | 392                | 16             | 306          | 63            | 107              | 17              |
| 77      | 357                | 24             | 306          | 103           | 71               | 26              |

### Discussion

The results show that mini hubs offer a more efficient route compared to van2door delivery. The primary advantage is reducing the distance between pickup stores and mini hubs, minimizing travel time for both vans and carts. However, too many mini hubs can increase operational costs without significantly improving service times.

Overall, the project suggests mini hubs as a potential solution for last-mile deliveries but highlights the need to carefully select locations that optimize efficiency while keeping overall costs in check.

# data modeling

 Link: [data modeling]("../a/data_modeling.html")

**Title:** Data Modeling

**Author:** Giovanni Marelli  
**Date:** 2019-07-02  
**License:** CC by-sa-nc 4.0  
**Language:** en-US

## Introduction

In modern data platforms, a proper data model significantly influences the efficiency and cost of infrastructure setup. A well-designed data model ensures efficient data pipelines, fast batch processes, effective retention policies, swift insight creation, and cost reduction.

### Key Skills Required for Data Modeling

1. **Product Management:** Collecting and understanding business requirements.
2. **DevOps:** Understanding the technical stack and its components.
3. **Business Analysis:** Understanding the operations of various business units.
4. **Data Analytics:** Understanding data characteristics and transformation costs, as well as insights generated by data.
5. **Machine Learning:** Proposing suitable feature engineering and preprocessing techniques.
6. **Solution Architect:** Designing a correctly sized infrastructure.

**Use Case:** The FHIR (Fast Healthcare Interoperability Resources) standard is an example of a widely used protocol for sharing patient health information.

## Taxonomy

Taxonomy involves forming a data model by considering the company's structure, customer personas, audience segments, and product portfolio.

## Relational Data Models

Historically, relational databases have been predominant due to their relational nature, which facilitates easy integration between services.

## Nested Data Structures

Data models may include nested structures to represent complex relationships and hierarchies within data.

## Protocols and Standards

### FHIR (Fast Healthcare Interoperability Resources)

FHIR is a standard used for exchanging healthcare data, particularly patient information. It provides a structured format for sharing medical records and facilitating interoperability between different healthcare systems.

**License:** Creative Commons Attribution-ShareAlike 3.0 (CC by-sa-nc)

# text gen

 Link: [text gen]("../a/text_gen.html")

This document discusses various aspects of text generation and retrieval systems:

1. **Text Generation Models:**
   - The text generation process involves building a model that learns how to map input sequences to output sequences.
   - Common models include Long Short-Term Memory (LSTM) networks and Transformers, evolving from LSTM to Transformers for better flexibility.

2. **Text Preprocessing:**
   - Text is cleaned using techniques like lowercasing, stemming, removing punctuation, hyperlinks, and stopwords.
   - Lemmas are extracted and a vocabulary is created by selecting the most frequent words up to a maximum size.

3. **Splitter Techniques:**
   - Splitters are essential for creating Retrieval-Augmented Generation (RAG) systems, which need to process large documents into manageable chunks.
   - Key splitters include Markdown-based, Document Tree, and Sentence/Semantic Splitters. The best-performing splitter maintains document structure while keeping text chunk sizes similar.

4. **RAG Systems:**
   - RAG consists of two steps: collecting relevant context and generating a prompt to answer questions based on the context.
   - Challenges include creating a knowledge base, choosing an appropriate vector database, selecting retrieval metrics, designing efficient prompts, parsing outputs, and evaluating results.

5. **Tokenization/Embeddings:**
   - Tokens are created based on word frequency in training data, with an option to introduce semantic relationships using models like Word2Vec.
   - Tokens are reshaped for model input and saved as a consistent preprocessing function.

6. **Vector Stores:**
   - Various libraries like Chroma, FAISS, Pinecone, Elasticsearch, Qdrant, and Redis are used for vector storage, each with different retrieval metrics (e.g., cosine similarity).

7. **Chains and Templates:**
   - Chains and templates simplify building applications using Langchain and LlamaIndex, allowing for easy interaction with multiple LLM providers.

8. **Multimodal Handling:**
   - Some PDFs contain audio, video, and images, which need to be separated and processed by dedicated language models for retrieval.

9. **Evaluation Tools:**
   - MLflow is used for evaluating language models across various metrics like professionalism, relevancy, toxicity, faithfulness, answer correctness, context recall, precision, adherence, completeness, chunk attribution, accuracy/robustness (Bedrock), contradiction, and hallucination.

10. **Model Selection:**
    - Different models like LSTM, Transformers, BERT are compared, with LSTM yielding poor results and Transformers showing flexibility and grammar learning capabilities.
    - Word2Vec is used to reduce text dimensions through shallow neural networks, visualizing word embeddings in 2D and 3D.

11. **Performance Tuning:**
    - Techniques include hardware optimization (e.g., GPUs), batch processing, caching, prompting strategies, load balancing, tuning token traffic, simplifying chains, optimizing retrieval efficiency, profiling, monitoring, using C++, assessing storage bottlenecks, and evaluating resource use.

12. **PDF Processing:**
    - PDFs are complex, containing tables, images, and references.
    - Libraries like PyMuPDF, BeautifulSoup, unstructured, and camelot are used for various operations such as text extraction, table parsing, document structure creation, and graph generation.

13. **Other Tools:**
    - Additional tools like `pdfplumber` and `pdftabextract` offer different approaches to PDF processing, including OCR, rendering, clustering, and data extraction.

Overall, the document provides a comprehensive overview of text generation, RAG systems, model selection, preprocessing, and evaluation techniques in natural language processing.

# spiega

 Link: [spiega]("../a/spiega.html")

The document "spiega tech" is a collection of articles and projects from the author's career spanning over 17 years, with over 3,000 source code files and 2,000 images. The main areas covered include:

- Data science: machine learning in operations and business applications
- Optimization engine (reinforcement learning, simulations) 
- Simulation engine in Python
- C/C++ simulation code for biophysical membranes
- Generative ML (ML painting, text generation, music composition)
- Time series analysis
- Machine learning library used across multiple projects
- Equations of motion and ride behavior
- Big data processing and web services
- ERP tools and firm consultancy
- Scientific contributions (PhD defense/paper on membrane inclusion objects, master defense/thesis on nanoparticle stability)
- Music tech including theoretical discovery of composition, electronics
- IoT applications (coil for pickups/sustainers, synth collection, DSP effects, mechanical amplifier)
- Data management, governance, and security practices

The document includes links to various articles and projects within the "spiega" repository.

# antani concept

 Link: [antani concept]("../a/antani_concept.html")

This document discusses Antani, an innovative software solution designed to optimize logistics and operational efficiency in various industries. Key points include:

1. **Problem Definition**: The core problem addressed is identifying the most efficient path for tasks within a network while maximizing profitability, considering factors like revenue, cost, task time, and location.

2. **Previous Solutions**: The document compares existing solutions such as Delivery Based (Routific) and Google/Or-tools, highlighting issues with long deviations, skipped tasks, unclear priorities, lack of resuming, and inefficiencies in route optimization.

3. **In-House Solution**: A novel approach is proposed, which uses an ant-based algorithm to optimize routes. This involves simulating the behavior of ants moving from one task to another on a network, guided by energy functions that reflect profitability, location, cost, and time.

4. **Energy-Based Approach**: The document introduces an energy function for tasks in Antani, which measures the value of tasks, their separation, the area they cover, their operation time, and total distance traveled. This function is used to guide the ant's movement and optimize paths.

5. **Optimization Techniques**: Advanced optimization techniques such as Markov Chains and Monte Carlo simulations are employed to enhance the solution's performance. These methods help in finding near-optimal routes quickly and efficiently.

6. **Reinforcement Learning Integration**: The document also mentions integrating reinforcement learning to further improve the acceptance rate of solutions, making the process more dynamic and adaptive to changing conditions.

7. **Posterior Probability Improvements**: By incorporating real-time data, the solution is enhanced with posterior probabilities that update as new information becomes available, improving its accuracy over time.

8. **Microservice Design**: Antani's architecture is designed using a backbone of microservices, enabling scalability and flexibility in deployment and maintenance.

9. **Integration and Documentation**: The document outlines how Antani integrates various components like OpenLayers for frontend visualization, D3.js for data manipulation, and Redis for caching, along with a comprehensive documentation system to facilitate easy use by users and developers.

10. **Future Outlook and Acknowledgements**: The authors provide an outlook on the future development of Antani, including plans to test it in real-world scenarios and compare its performance with other existing solutions like Routific. 

Overall, this document provides a detailed overview of the Antani system, its theoretical foundations, implementation details, and future directions.

# route

 Link: [route]("../a/route.html")

This document discusses a project to analyze motorway traffic using various methods. The main goal is to understand where cars enter and exit specific junctions on a motorway in Germany. Here are the key points:

1. **Data Collection**: The focus is on 12 junctions on an isolated motorway (A4) crossing Germany.

2. **Preprocessing**:
   - Chains from tripEx are filtered using a pre-validation script.
   - Tile counts are obtained for each junction to count incoming and outgoing fluxes.

3. **Postprocessing Routing**:
   - The routing graph is built by keeping only junctions different from street classes.
   - We work on weighting the edges to improve routing quality, especially between highway classes like motorway, primary, secondary, and tertiary.
   - Distances are precomputed for zip codes using a shortest path algorithm.
   - An ODM (Optimal Demand Matching) is run for 9 days to count trips through motorway junctions.
   - The enter-to-exit relationship matrix is created by grouping via nodes together.

4. **Troubleshooting**:
   - After multiple iterations, the routing of people leaving the motorway became inconsistent.
   - We manually added via points on motorway links and associated them with locations to group entrances and exits together.
   - Further analysis revealed that some junctions were asymmetric and led to detours.

5. **Suggestions for Improvement**:
   - The project suggests updating the graph with additional attributes like routed distance, chirality, and gyration radius to improve routing accuracy.
   - It also recommends ensuring that trips do not start on motorways, direction changes are restricted, and paths are included between start and end points.

6. **Automated Labelling**:
   - Two functions (`enrichNissan` and `junctionNodes`) were written to automatically label junction nodes based on their proximity to the motorway and perpendicular distances.
   - These labels were used to create an infrastructure for further analysis.

7. **Analysis of Thuringia Data**:
   - The project also ran an ODM (Any Via) for 1M3 chains dataset in Thüringen, resulting in count matrices between entry and exit junctions.
   - Despite limited data, the results showed some asymmetry but no clear picture about the result performances.

Overall, the project aims to improve traffic analysis on motorways by addressing issues with routing, starting-ending points, and detours.

# python

 Link: [python]("../a/python.html")

### Summary of python.md Document

This document discusses the author's experience with Python programming, particularly focusing on the use cases and libraries they frequently employ in their projects. The content is organized into sections:

1. **Introduction**: The author describes how they initially discovered and began using Python, emphasizing its benefits over compiled languages for data analysis and testing.

2. **Development Areas**:
   - **ERP (Enterprise Resource Planning)**: Describes applications that use GTK interfaces and database connections.
   - **Geographical Tools**: Provides an overview of various Python-based projects across different domains including data processing, machine learning, web development, automation, and more.

3. **Detailed Analysis of Provided Code Files**:
   - **General Structure**: Highlights common elements such as the `__init__.py` file and scripts related to data processing.
   - **Specific Python Files**: Lists specific files for each area including those used in data consumption, web applications, database operations, machine learning, utilities, and tools.
   - **Python Libraries Used**: Describes commonly used libraries like pandas, NumPy, Matplotlib, TensorFlow/Keras, PyTorch, SQLAlchemy, psycopg2, boto3, Flask/FastAPI.
   - **Key Features and Requirements**: Specifies the knowledge required for specific tasks such as data manipulation, database interaction, web development, and machine learning.
   - **Code Examples**: Provides examples of how these libraries are used in practical code snippets.

4. **License Information**: Details the licensing terms under which the content is shared, specifically CC BY-sa-nc.

Overall, the document serves as a comprehensive guide for understanding and leveraging Python in various development tasks, providing both theoretical insights and practical examples to support effective project management and development workflows.

# piezo buffer

 Link: [piezo buffer]("../a/piezo_buffer.html")

The summary of the `piezo_buffer.md` document is as follows:

This file discusses using CircuitLab for creating a piezo buffer. It provides an overview of how to use CircuitLab for designing and simulating circuits, including information on circuit components, simulation settings, and code generation options.

# go

 Link: [go]("../a/go.html")

### Summary of the Document

The document "go.md" from the directory describes several Go projects and their primary features:

1. **`htpasswd.go`**:
   - Manages HTTP Basic Authentication in Nginx.
   - Uses MD5 hashing for passwords, with a format starting with `$apr1$`.

2. **`modules.go` in `logspout` Directory**:
   - Provides configuration and installation of components for Logstash support using Logspout.
   - Components include:
     - Healthcheck package to monitor Logspout status.
     - TCP and UDP transport packages for sending logs.
     - Logstash adapter for routing logs to Logstash instances.

3. **Web Server Configuration**:
   - Handles API endpoints using Gorilla Mux.
   - Supports HTTP methods such as POST, GET, PUT, and DELETE.
   - Provides static content serving from `/apidocs/` and `/static/`.
   - Error handling through response functions (`respondWithError` and `respondWithJSON`).
   - Defines routes for functionalities like index pages, page retrieval, authentication, CRUD operations, and Swagger documentation access.

4. **API Management**:
   - The `go_ingest` package initializes a database connection using environment variables.
   - Ensures the `products` table exists in the database.
   - Deletes all entries from the `products` table before running tests and reinitializes the sequence for new IDs.
   - Provides helper functions (`ensureTableExists`, `clearTable`) to manage table creation and data cleaning.
   - Uses Gorilla Mux for routing with test functions that cover scenarios like empty tables, non-existent products, product creation, retrieval, updating, and deletion.

5. **Authentication**:
   - Functions include `userpassword` for mapping usernames to hashed passwords, `generateJWT` for JWT generation, `authenticateRequest` for validating user credentials based on Base64-encoded headers, and `authenticateJWT` for validating JWT tokens.

6. **Swagger Documentation**:
   - The `docs` package uses Swag to generate a Swagger documentation template for the API.
   - Registers Swagger information with Swag's registration system, which generates actual Swagger documentation when the application starts.
   - Provides embedded files (`embed` package) to access static files without manual loading from the filesystem.

7. **Database Operations**:
   - The `main` package initializes an App struct using environment variables for database connection parameters.
   - Runs on port 5006 and handles operations like querying, updating, deleting, and creating entries in a database using the SQL package.

Each project showcases different aspects of Go programming, including authentication, web server configuration, API management, and document generation. The document provides clear structures for handling specific functionalities within larger application environments.

# feature relevance

 Link: [feature relevance]("../a/feature_relevance.html")

### Feature Temporal Ordering

**Inter-Feature Persistence Analysis:**
1. **Rolling Correlation Window (16 seconds):** We calculate the correlation of each feature with every other over a 16-second rolling window.
2. **Most Correlated Features:** While some features exhibit weak or no correlations, others show higher temporal correlation, particularly `vehicle_ping`, which is evident from violin plots.
3. **Cross-Correlation Analysis:** The cross-correlation between `vehicle_ping` and latency reveals that the former correlates strongly with latency at various time delays.

**Decay Time Calculation:**
1. **Exponential Regression on Decays:** For each feature, we perform an exponential regression to determine its decay time.
2. **Persistance Calculation:** Persistance is calculated as the sum of the decay curve over a specified interval (e.g., 30 seconds).
3. **Matrix of Persistance:** We then compute the matrix of persistance among all features to identify correlations.

**Persistent Features:**
1. **Cross and Auto-Persistance:** Large values in the persistence matrix indicate poor sampling or artificial similarity.
2. **Example Matrix:** A detailed matrix showing the persistance between various features is provided.

**Data for Other Applications:**
1. **Modem Persistance Data:** The same analysis is applied to modem-related features, indicating different phases and relationships.

### Phasing Analysis

**Delay Calculation using Cross-Correlation:**
1. **Example Delay Diagrams:**
   - **RTP vs Camera Latency:** Shows a clear delay.
   - **Joystick vs Camera Jitter:** Also shows a significant delay.
   - **Modem vs Camera Rtt:** Similar to RTP.

**Cross-Correlation Phase Difference Calculation:**
1. **Fourier Cross-Correlation Method:** This method provides a phase difference between features, helping in understanding the timing order.
2. **Example Fourier Diagrams:**
   - **Denoised Data:** Shows clearer phase differences.
   - **Deci Second Scale:** Modem data is more prominent before latency.

**Phase Lag Calculation for Each Series:**
1. **Dot Plot of Each Series:** Represents individual time series with slight variations in data points.
2. **Phasing Violin Plots:** These plots show the difference in phase lag between various features and camera latency.

### Final Phase Determination

1. **Average Delay Calculation:** The average delay is calculated using cross-correlation, revealing that different methods can give varying results for certain series (e.g., `bytes-Cellular 3`).
2. **Modem Features:** Modem features are consistently preceeding the latency.
3. **Denoised vs Summed Data Analysis:** The phase difference calculation is more robust with denoised data compared to summed data.

In summary, the analysis identifies that certain features (e.g., `vehicle_ping`, `modem_rtt`) preceed the camera latency spike, while others follow it or are less correlated. The methods used for phasing and delay determination provide varying results but can generally determine the temporal order of events with a high degree of confidence.

# documentation

 Link: [documentation]("../a/documentation.html")

**Summary of the Document:**

The provided document titled "Middleware" is a comprehensive guide on various aspects of project documentation and code, focusing on several key areas:

1. **Naming Convention**: The document introduces guidelines for naming conventions, though no specific details are provided.

2. **Inline Documentation**: It discusses the importance of inline comments in code to enhance readability and maintainability.

3. **Swagger Documentation**: The text emphasizes using Swagger as a tool to document APIs. It provides an example from a Python project where Swagger reads function definitions and generates a webpage with detailed information about endpoints, including curl requests for testing.

4. **Notion Overview**: Notion is highlighted as a user-friendly platform for documentation, planning, kanban, and team/project management. The document notes its increasing feature set and success over established tools like Atlassian and Jira due to improved usability.

5. **Alternative Platforms**:
   - AppFlowy
   - Focalboard
   - BookStack
   - Anytype

These alternative platforms are compared to Notion, emphasizing their features and ease of use in various contexts.

The document concludes with a summary of the advantages of using Notion for project management and documentation, highlighting its expanding capabilities beyond just documentation.

# scheduler

 Link: [scheduler]("../a/scheduler.html")

This document provides an overview of the scheduling system in Sawmill, focusing on Airflow as the primary scheduler. It details the usage of Airflow and a specific deployment configuration using Docker Compose. The document also explains how to schedule DAGs using cron syntax and provides Python examples for creating scheduled tasks within DAGs.

# motion

 Link: [motion]("../a/motion.html")

This document is titled "Motion" and was authored by Giovanni Marelli on July 2, 2019. It provides a detailed analysis of motion data collected from GPS devices across Germany. The content is structured into several sections:

1. **Introduction**: 
   - Overview of the dataset containing GPS coordinates, device type, accuracy, and time zone for each user.
   - Description of how octree indices are created for these coordinates based on accuracy.

2. **Data Type**:
   - **Positions**: Includes timestamps, unique IDs, device types, accuracy, and timezone for each GPS event.
   - **Densities**: Calculates density values by grouping positions into octrees, removing those with low event counts, and then averaging positions and times for these boxes.

3. **Trajectories**:
   - Pivoting user data to create a dataframe of trajectory points, including user ID, time-space matrix, number of trajectory points, bounding box (in octrees), and time interval.
   - Visualizations showing the density of trajectories across the city.

4. **Frequencies**:
   - Creating a dataframe to track daily user appearances in Germany.
   - Visualization of user frequency trends and distribution of events per user.

5. **Speed Profile**:
   - Calculating point-to-point space-time differences to derive speed, angle, and chirality for each trajectory segment.
   - Visualizations demonstrating how different smoothing methods affect the calculation of speed density.
   - Clustering trajectories into dwellings and movements based on a defined threshold.
   - Displaying dwelling and movement patterns across the city.

6. **Retail**:
   - Comparing GPS signal density with mobile antenna connections to identify retail areas.
   - Visualization of retail density maps and ranking changes compared to mobile data.

Overall, this document aims to provide insights into user motion patterns, trajectory behavior, speed characteristics, and their relationship to retail areas using geographic data analysis techniques.

# prediction telemetry

 Link: [prediction telemetry]("../a/prediction_telemetry.html")

This document outlines several types of prediction models and their performance in different scenarios, primarily focusing on camera latency and spike detection. The key points are as follows:

1. **Latency Prediction**:
   - **Objective**: Distinguish camera latency into different danger classes.
   - **Results**:
     - **Two Class**: Predictions decrease with more classes.
     - **Five Classes**: Significant performance drop.
     - **Incident Set**: Training is harder when focusing on incident data.
     - **Confusion Matrix**: Most confusion occurs within the diagonal, indicating high precision and recall for correctly classified latency classes.

2. **Feature Importance**:
   - **Results**: Different models have varying feature importances, with "modem issues" consistently top among relevant features.

3. **Spike Prediction**:
   - **Model**: Simple Sequential model is used as a baseline.
   - **Performance**: Baseline model performs well on average but only predicts peaks.
   - **Improved Models**: Three-layer networks perform better on incident data, detecting more peaks.

4. **Risk Prediction**:
   - **Objective**: Predict `time_to_spike` and calculate spike risk using Cox-Breslow survival estimator.
   - **Results**:
     - **Deviation**: Spike detection accuracy decreases with higher deviation threshold.
     - **AUC**: Cow Breslow AUC provides a good baseline for prediction.
     - **Cross Validation**: Model's performance converges towards the average.

5. **Spike Forecasting**:
   - **Learning Process**: Learning is irregular, with epochs showing inconsistent improvements.
   - **Confusion Matrix**: Confusion matrix shows high accuracy in forecasting spikes but also highlights low recall on unobserved data.
   - **Network-Focused Forecast**: When focusing only on networking features, the confusion matrix improves.

Overall, the document highlights the complexity of prediction models in different scenarios and emphasizes the importance of feature selection and model architecture for improving performance.

# testing

 Link: [testing]("../a/testing.html")

### Summary of the Testing and Checks Documentation in Directory `testing.md`

#### Overview
The document outlines various testing and check procedures for different services, which are essential to ensure the reliability and stability of software development. Here's a summary:

1. **Unit Tests and REST Requests**:
   - Each service has a `testing` folder containing tests that can be integrated into CI/CD pipelines.
   - Ideally, deployment should fail if any test fails to pass.
   - Tests can include unit tests for single functions or REST requests to the service.

2. **Testing in Actions**:
   - Placeholder section for testing actions.

3. **Database Connection Testing**:
   - Example Python script using psycopg2 and SQLAlchemy to connect to a PostgreSQL database and list databases, tables, and schemas.
   ```python
   db = create_engine('postgresql://{}:{}@{}:{}/{}'.format(db_user, db_pass, db_host, db_port, db_name))
   res = db.execute("SELECT datname FROM pg_database;")
   for r in res: print(r)
   ```

4. **Endpoint Testing**:
   - Example Python script that tests various endpoints of a service using `requests` library.
   ```python
   import os, sys, json, datetime, requests

   url = "http://0.0.0.0:5005"
   headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
   inMex = {
     "id": 1,
     "action": "(name, price) values ('test_product',11.25)",
     "table": "products",
     "filter": ""
   }
   resq = requests.post(url+"/create", json=inMex, headers=headers)
   print(resq.json())
   ```

5. **Backend Testing**:
   - Example Python script that tests backend functionalities such as authentication, book entries, and SQL ingestion.
   ```python
   import os, sys, json, datetime, requests

   url = "http://0.0.0.0:5006"
   headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
   payload = {
     "id": 1,
     "action": "(name, price) values ('test_product',%f)" % random.uniform(1,30),
     "table": "products",
     "filter": ""
   }
   resq = requests.post(url+"/create", json=payload, headers=headers)
   print(resq.json())
   ```

6. **Kafka Testing**:
   - Example Python script that tests Kafka for producing and consuming messages.
   ```python
   import json, base64

   inMex = {
     "content": "base64-encoded message raw content (unparsed)",
     "sender": "sender@example.com",
     "recipients": ["recipient1@gmail.com", "recipient2@yahoo.com"]
   }
   producer = KafkaProducer(bootstrap_servers=["kafka:9093"])
   producer.send(topic, value=inMex)
   ```

7. **Docker Health Checks**:
   - Docker can perform health checks to ensure a service is active at regular intervals.
   ```yaml
   healthcheck:
     test: ["CMD", "pg_isready", "-U", "api_ingest"]
     interval: 5s
     retries: 5
   ```

These procedures help in maintaining the integrity and reliability of the services by ensuring they are tested thoroughly before deployment.
