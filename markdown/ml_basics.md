---
title: machine learning basics
author: Giovanni Marelli
date: 2019-09-12
rights:  Creative Commons Non-Commercial Share Alike 3.0
language: en-US
id: ml_basics
category: #tech
roam_refs: ml basics
roam_aliases: ["machine learning basics"]
output: 
	md_document:
		variant: markdown_strict+backtick_code_blocks+autolink_bare_uris+markdown_github
---


# basics

* introduction to AI, concepts and terminology
* Evolution of AI cycle
* importance of data and ML pipeline
* Ethical consideration

AI is a software that needs an instance to run and connections with input and output
AI learns from the past and works with probability
AI learns patterns and is accurate with high frequency occurences
AI suits with big data, low recurrences are more suited to rule based
AI is helpful to simplify complex stratified rules (like pricing)
AI is data driven, successful projects should be adequately measured

## stand 2025

GenAI is conquering the professional market.
Large language models are now more accurate, consistent and able to handle sensitive data.
Protect from AI is getting essential.
AI spreading in security, networking and ticketing.
ML is needed in predictions, forecasts, anomaly detection, pattern recognition.

### AI types

* Generative models: translation, text, video, photo
* Agents: fulfill specific tasks (reading database, computing, search information, summarize)
* Assistant: customer questions, customer calls, browsing knowledge base
* Monitoring: scanning the system and trigger notification

### ML types

* Prediction
* Forecast
* Parttern recognition
* Anomaly detection
* Compression
* Classification

## from need to production

The AI journey starts from the wish to implement a new technology or a new way to solve an existing problem.
AI requires a certain data and infrastructure maturity to kick off a project and it's essential to dedicate some project resources with experts to check project prerequisites.

A typical journey is like:

* management:
  * presales and scoping
  * scope, objectives and success criteria
  * timeline and expenses
* delivery:
  * feasibility assessment
  * proof of concept
* planning:
  * PoC review and take aways
  * implementation plan
* production:
  * plan and coordinates experts, provide software/hardware
  * execute according to interdependencies
  * update the client regularly on deliverables, unexpected situations, mitigations
* post sales:
  * monitor appliances, data quality and model performances
  * consider eventual improvements and extra maintenances
  * check ROI

### management

Management is a crucial phase for project success
The **requester** should provide:

* clear use case description
* proposed strategy and description of attempts in that direction
* budget indication
* most relevant KPIs
* minimal data/tool access for the external
* explanation on the internal knowledge relevant for the project (data catalogue, ingestion processes, ETL)

The **provider** should then propose:

* the strategy to the goal
* costs and timeline
* risks and alternatives
* expectation management on data drive projects
* explain the state of the art in that field

The management phase should finish with an agreement on:

* deliverables and timeline
* staff and tools required
* planned interactions between the parts
* optimization metric and success criterium
* delivery format and final knowledge exchange


### foundation

A short **foundation** phase is essential to prove that:

* The infrastructure is suited for the specific task
* GDPR compliance
* The data governance allow externals to access (at least the portion of data for the PoC)
* Data has the correct density (in data points) and quality (consistency and regularity)

The foundation phase is essential to spot at an early stage issues which:

* might pop out later on and waste a huge investment
* spot serious inconsitencies and require to investigate the data collection
* signal issues with the data processing and point out relevant improvements
* often feature engineering is not meant for AI projects, relevant information is averaged out

During fonudation investigation a report is generated with all the findings marked as warnings or critical. A mitigation strategy is suggested as well.
Pursuing the issues uncovered during investigation leads to long terms benefits solidifying the processes and the readiness for future innovation.

### PoC

A successful PoC needs a clear agreement on:

* scope and objectives
* quantitative results (success metric)
* timeline and costs
* delivery format

When the system is compliant, active work can be done on data. Usual activities are like:

* data exploration: anomalies and consistency of features, statistical properties
* feature engineering: review or addend some ingestion processes
* preprocessing: reshape input, format types
* evaluation framework: how to evaluate and compare runs
* prepare dataset: what is going to be used for train and what for test
* model selection: which model leads to best results, what is convenient to put in production
* further tuning: performance boost in uplift or efficiency
* retrieval: connect the model with data sources, enhance model comprehension with metadata

### planning

After a successful PoC the client should review the results and decide whether or not to continue with an AI project depending on the success of the phase and the projected costs. During planning the parties discuss the option to extend the scope of the PoC or put in production what was tested.
The discussion for production should consider the set-up and live costs of the solution and whether the existing infrastructure can host the solution or additional hardware/software should be purchased.
The planning phase should provide a detailed list of activities and timeline for the roll-out of the solution.
The planning phase should consider all the actors consuming the solution and the form they want to interact with the system or with its analytcs (API, BI...)

## production

The production phase is more engineering driven where a project manager distributes the tasks across all the experts taking care of cross dependencies.
The production phase should consider as deliverables:

* monitoring system: logs and dashboards
* documentation: end user and tech user
* system interaction: API - BI
* service level: continuous or on demand
* analytics: on product usage and performances


# project types 2025

AI supports different types of projects 

* manifacturing: predictive maintenance, digital twins
* logistics: last mile, efficiency, dispatch
* media: content, distribution, profiling
* banking: fraud, reliability
* finance: forecasts, risks
* insurance: pricing, risks
* energy: forecast, efficiency
* IT: networking, cybersecurity
* e-commerce: conversion uplift
* advertising: audience, inventory
* healthcare: assistant, diagnostic
* retail: inventory optimization, product development
* telco: cell demand, motion patterns

Cross industry:

* product suggestion
* contact points
* customer care
* audience targeting
* sale assistant
* knowledge share

# what is ML made of?

Some basic concepts about machine learning.

A software takes inputs and returns some output performing a calculation.
Machine learning is a regression, takes an input and returns a probability.

### statistics

The realm of machine learning is statistics, it is crucial to understand few concepts:

**Frequentist**: you look at the past and build a segment like male/18-35/good salary. You look at the purchase history and come to those conclusions:

  * is 40% of your customer base
  * converted 0.02% in advertising

![frequentist approach](../../f/f_lernia/frequentist_approach.png "frequentist approach")
_frequentist approach_

The **probabilistic** approach considers the most relevant features and the unique combination of the different segments to return a likelihood of the most probable outcome

* probabilistic:
  * this target has 15% conversion uplift from average
  * the most relevant feature is client age

![probabilistic approach](../../f/f_lernia/probabilistic_approach.png "probabilistic approach")
_probabilistic approach_

Machine learning works with probability, the most probable outcome is not strictly the correct one, sometimes two results scores similarly but just one is taken.

### training

Machine learning works with historical data. You take past experiences and try to derive common patterns, sometimes even cause-effect relationships. 

In machine learning you take a **model** and a **score function**, **training** is when you run the solver to minimize the score function.

Optimization metric:

* revenue
* conversion uplift
* cost reduction
* time loss

Score function:

* error
* correlation
* mutual information

There are different kind of models (regressors):

* tree structure
* bagging/boosting ensemble (width vs breadth)
* regression: neural networks, polynomial, logistic (yes/no), lasso/ridge (many similar features)
* classification: classes

![bagging_boosting](../../f/f_lernia/bagging_boosting.png "bagging_boosting")
_bagging vs boosting ensambles_

### neural networks 

Neural networks are layers of interconnected neurons, the architecture describes the connection between the single neuros. Famous architectures are:

* encoder-decoder
* convNet
* long short term memory
* transformers

### attention to transformers

2017-2019 was a crucial moment for ML. Data scientists were struggling to explain what models were based on and were building a lot of attention maps into their network to understand what caused the model to decide. The models where then pivoted around attention (opposed to add attention later) and transformers were born.

Transformers are more flexible than model previously used but require more computational power which was progressively made available by new hardware in the 20s.

Transformers have an encoder-decoder architecture where the large and redundant input space is comprised into a much smaller vector space. The encoder projects the text into a low dimensionality space where similar meanings are close-by. The encoder is the comprehension part of the transformer while the decoder formulates the answer back in a natural language.

Transformers needs embeddings which are representation in vector space of the input. The input should be converted into arrays before being processed by the model. Arrays are handy to perform vector search and find similarities. Embeddings traditionally come from algorithms like word2vec and are responsible for good model performances. Embeddings and models are tightly coupled and concious choises should be done in decing a pair. Usually LLMs perform at best with own developed embeddings.

### prediction vs forecasts

A **prediction** is the result of the most probable outcome for a given state:

* risk for a particular investment
* churn probability for a given customer
* product success on a market

A **forecast** is the probability for an event in the future. Forecast is different from predictions because the dataset consists in ordered time series and the output variable can be used as input as well.
Examples of forecast methods are:

* ARIMA
* periodic decomposition
* long short term memory
* pattern recognition

For forecasts neural networks usually perform worse than other metods and are pretty heavy in production.
Examples of forecasts are:

* next month revenue
* next system failure
* inventory volumes in two weeks


### reinforcement learning

Reinforcement learning is used when we have an agent interacting with the environment. The agent is able to perform an action on the system and a score quantifies the benefit of that action.
Examples are:

* a videogame player
* a dispatcher software
* a trading agent

Reinforcement learning works with the explore/exploit logic. The agent first picks a random action and the score gets updated. A machine learning model has as input the state of the system (a picture for videogames, the stock market for a trading agent) and actions as output (move/jump/shoot, sell/buy). The learning process with the random approach takes a long time for the initial phases.
After a long random phase the agents starts using the outcomes of the model under training (exploit phase).
Sometimes the agent struggles later on in the game when encountering a combination not seen before. Those obstacles are the hardest to overcome since sometimes the training is too stable for changing its memory.

### Computer vision

Computer vision is a branch of ML aiming at recongizing content from pictures.
Computer vision is an old branch of information technology and makes use of different algorithms:

* Haar cascade: creates a dictionary of geometrical shapes and relative order
* convolutional neural networks: for edge recognition and dimension reduction
* transformers: more flexible than convNet, heavier and more demanding for training and inference

There is a large choice of computer vision libraries depending on the device they run. The main goal is to detect directly from camera and perform edge computing. Models should run on a small device and the list of objects to recognize should be synced.

The main purpose for computer vision is:

* survaillance: unauthorized recognition
* inspection: product line failure
* safety: anomaly behaviour
* remote control: notify controllers


To train computer vision systems is important to generate synthetic data to help the model recognize similar images in different conditions (lighting, rotation, distortions...).


### Natural language 

Natural languages is the ability for a model to communicate in programming or human languages.
The models are created using selected dictionaries and eventually understand the grammar and the syntax of the language.

The natural languages tasks changed over time and became more extensive:

* sentiment analysis
* reputation
* summaries
* translations
* reasoning


The former methods required heavy pre-processing on text to extract the semantic meaning of the sentece. Nowadays transformers don't need much pre-processing (stemming, stopwords...) because they are mainly trained on a huge amount of data. Large language models still would profit from additional embeddigs (e.g. grammar) to be more efficient.
Recently models show decent accuracy for small devices while a discussion is running around whether the huge models are reaching an asymptote with the current architecture.

Large language models are made by a encoder-decoder architecture, the encoder performs text understanding while the decoder formulate the answer. 

A key factor for the quality of outputs for LLM is the input data. Over a decade a large effort was done to create data sets for training. The most important dataset types are:

* Knowledge: articles
* Ground truth on dialogs and context: the model receives blanks in conversations and needs to fill in missing part
* Labelling: humans annotated summaries, abstracts, translations
* RLHF (reinforcement learning with human in the loop): needs a human to evaluate the outcome and suggest the model to re-iterate the answer until the human provides a better score
* SWAG (situations with adversarial generations): "she opened the hood of the car," ... "then, she examined the engine"
* chain of thought fine tune: suggesting the model issues with reasoning
* ORCA: AI assistant

Thanks for the performances of LLMs on these datasets in 2025 much smaller models can be used with similar results thanks to:

* distillation: a large model as a teacher and a smaller as a student
* quantization: training needs high precision, inference doesn't. Weights are casted to smaller numbers (4bit, 8bit) to compute faster
* cpp: once a model performs it can be translated into a more efficient language
* agentic: a complex task is divided to smaller models dedicated to simple tasks, the ensamble is highly efficient

This means that companies with smaller resources can perform fine tuning again and work on custom, highly performant models.

## evaluation

Evaluation is a critical aspect of genAI, the model cannot be simply evaluated by a score function as per classical ML but another model should be able to provide some confidence on the response. The metrics like ROUGE and BLEU which computes the distance from the expected exact words are outdated and more advanced metrics are requested like:

* consistency
* toxicity
* hallucinations
* correctness
* accuracy

Those metrics keeps on changing and can be contraddicted by humans especially in highly technical domains. In the race of the most performing model metrics can be discordant and sometimes biased.
The preferred approach for technical domains is to evaluate referring to a ground truth from a domain expert.

# genAI

Generative AI is a branch of AI where the model output creates a content instead of returning a numerical value or an item from a list. The media used are: text, images, sound, video
Within each media there are different decomposition techniques:

* text: chat, context 
* images: element recongition, scene description
* speech: diarization, sound processing
* sound: tracks, items
* video: relevant frames

GenAI hype started around 2018 when data scientists were training and fine-tuning transformers like BERT, ROBERTA, GPT... after a couple of years of architecture design, fine tuning, embeddings...
Then around 2022 a big investment was done in training really big models and only few players could participate in the race of investing in new models. Transformer architecture is versatile but has no particular intelligence built in. The accuracy of models depends mainly on traning effort and quality of input.

