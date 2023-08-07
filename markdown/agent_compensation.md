---
theme: spiega_pres
_class: lead
paginate: true
backgroundColor: #fff
backgroundImage: url('https://marp.app/assets/hero-background.jpg')
size: 16:9
style: |
  section {
    background-color: #ccc;
  }
---

# **dynamic targets**

# dynamic target

Agents compensation is a crucial stimulus for improving individual and company objectives. 

![title_stage](../f/f_intertino/title_stage.svg)
_compensation models_

# save rate

code: [target_rateCard](src/target_rateCard.py)

The usual agent target is the save rate

![saveRate](../f/f_intertino/saveRate_overall.png)
_overall save rate_

We actually know that there are many factors influencing the save rate

![saveRate](../f/f_intertino/saveRate_tenure.png)
_save rate depending on customer tenure_

The problem can be extended to multidimension

![saveRate](../f/f_intertino/saveRate_3d.png)

_3d representation of the save rate_


## ETL

code: [target_etl](src/target_etl.py)
query: [sky](query/sky.sql)

We first extract the data running the query on the client machine and extract the saving rate and the agent/user data. 

### data type

We have few features describing the customer, the agent group and the call type. Most of the data are in buckets which we turn into continous variables

### categorical

We than convert categorical features into continous variables to improve the model performance.

* `last_bill_amount` is substitued by the upper bound
* `precall_tenure` is substituted by the interval mean
* `package` hierachical tree
* `category` one hot encoding

## data quality

code: [target_stat](src/target_stat.py)

We have few features to predict the success rate and we analyze the quality of the input data

### missing/outliers

We have **missing** values across all features, we need to do a typecast to allow python handling the different kind of data.

Data are narrow distributed and we don't replace/exclude **outliers** neither perform a transformation on data

# save rate predictors

We start investigating the customer dimensions

![saveRate](../f/f_intertino/saveRate_bill-tenure.png)
_save rate depending on last bill and tenure_

We see a dependence on call time but we consider it more as an effect than a cause of save rate

![saveRate](../f/f_intertino/saveRate_rev-time.png)
_save rate depending on call time and customer revenue_

We can narrow down on many different levels and we will always see a feature contribution

![saveRate](../f/f_intertino/saveRate_seg-cat.png)
_save rate depending on segments and product categories_

taking into account that low values will be discarded or clamped into larger buckets

![saveRate](../f/f_intertino/saveRate_seg-cat_vol.png)
_save rate depending on segments and product categories_

We finally propose the following save rate for the rate card because in connects with the revenue stream and the product development

![saveRate](../f/f_intertino/saveRate_final.png)
_save rate depending on customer value and product holding_

We see that other variables are implicitely modeled by the rate card

![latent](../f/f_intertino/latent_variable.png)
_variables implicitely defined by existing variables_



## sampling shuffling

Is there a bias in homemover and no transfer calls where a group of agents gets an un even distribution of user groups? We test it calculating the share of call groups for each agent for each week and calculate the ranking distribution

![shuffling_chi](../f/f_intertino/shuffling_ranking.png)
_ranking from week to week_

The ranking correlation drops after few weeks

![shuffling_autocorrelation](../f/f_intertino/shuffling_autocorrelation.png)
_decay of autocorrelation over weeks_

We test the chi square for the agent series compared with the average 

![shuffling_chi](../f/f_intertino/shuffling_chi.png)
_chi values for agent call distribution_

We see that the chi values are pretty small and the p-values really high

### distribution

We analyze the distribution of features (normalized) and compare the variances

![feat_boxplot](../f/f_intertino/feat_boxplot.png)
_boxplot of normalized features_

Most of the values are discretized

![feat_series](../f/f_intertino/feat_series.png)
_time series of features_

### obvious dependencies

We see that this feature set don't have any internal correlation

![feat_corr](../f/f_intertino/feat_corr.png)
_correlation of features_

We display a pairplot stressing the different distribution depending on the save rate. We see a clear difference in distribution across all features and especially different regression depending on `last_bill_amount` and `precall_tenure`

![feat_pair](../f/f_intertino/feat_pair.png)
_pairplot of features depending on success_

A close up explains which features are important for the prediction

![feat_joyplot](../f/f_intertino/feat_joy.png)
_joyplot for the most relevant features_

We can say a slight difference in distribution in the different success subsets

![feat_saved](../f/f_intertino/feat_saved.png)
_feature on success_

We see that the afiniti engine is slightly increasing the call time

![feat_on](../f/f_intertino/feat_on.png)
_feature on afiniti on_

## prediction

We iterate over different models to calculate the prediction strength of this feature set. We see that performances are not high

![feat_pred](../f/f_intertino/feat_pred.png)
_prediction of save rate_

We see a larger number of false positive which tell us the difficulty to understand for a customer to cancel the contract

![feat_conf](../f/f_intertino/feat_conf.png)
_confusion matrix on save rate prediction_

### agent skills

We know that agent skill is a really important variable to model but we have few information on agent data to model such a variable and we hence treat it as a *latent variable*.

To assess the relative ability we imagine the agents being on a tournament, the customer is the referee and the game pitch is the area and the product. 

![agent_match](../f/f_intertino/agent_match.svg)
_agent ability simulating a match between agents_

Based on the historical series we run a stan simulation based on a prior ability where we compare the agent performances on the different game pitches

![prior_ability](../f/f_intertino/prior_ability.png)
_prior of the agent ability on area and product_

Once we get the prior distribution we run a simulation across all the agents over multiple games 

![posterior_ability](../f/f_intertino/posterior_param.png)
_posterior of the agent ability on area and product_

and we create a ranking

![posterior_ability](../f/f_intertino/posterior_rank.png)
_posterior of the agent ability on area and product_

We than simulate a series of matches and we finally calculate the posterior agent ability

![posterior_ability](../f/f_intertino/posterior_ability.png)
_posterior of the agent ability on area and product_

## agent compensation

Following *game theory* for a given set of **rules** the **compensation** implies a **strategy** and therefore the tuning of the compensation is crucial for performances.

![game_theory](../f/f_intertino/game_theory.svg)
_game theory sketch_

We need to balance between the individual and the company compensation:

* is an agent incentivized to risk his/her compensation with a difficult customer?
* does an agent has a real opportunity to change the success of a call?
* how can the company incentivize an agent to make the effort to save a customer

### saving rate compensation

We consider all users equal and the agent **compensation** is based on the **saving rate**. 
We consider a probability of saving rate of 73% +/- 22%:

* it is convenient for the agent to spend time trying to save the user?
  * would the agent complain for unbiased distribution of users (i.e. homemovers)?

### saving risk compensation

Each pair user/agent has a different success probability, what if the **compensation** would be based on the **success probability increase** 

* the agent will feel like an high stakes at poker
* the agent won't be penalized for his/her effort with a difficult case but incentivized to play

### customer value compensation

Users have a different value depending on their records, the value is weighted by the previous bill and the tenure:

* the agent is more motivated to spend more effort to save more valuable users
* the company retains important users

# compensation model

We have a list of **users**, each defined by the tenure, the bill amount, the product selection and the queue of the call

![user_list](../f/f_intertino/user_list.svg)
_definition of users based on tenure, bill value, product selection and queue_

We have a list of **agents** defined by the certifications, the tenure, the knowledge of the product and the queue they work in

![agent_list](../f/f_intertino/agent_list.svg)
_specification of agents_

We can estimate the **probability of success** of the call based on few information, we actually see that the retention of the customer is easier for high value customers

![call_probability](../f/f_intertino/call_probability.svg)
_the success of the call depends on few features_

Once a user calls the success probability depends on the type of agent joining the call

![user_agent](../f/f_intertino/user_agent.svg)
_user/agent success probability_

We predict the value of the customer in case of a successful call based on historical data

![call_success](../f/f_intertino/call_success.svg)
_estimated customer value after retention_


## objective

We propose parallel simulations where the agent is incentivised on different compensations which will imply different strategies and different achivements of company and personal goals

![agent_strategy](../f/f_intertino/agent_strategy.svg)
_agent strategey based on compensation_

## simulation 

code: [sim_compensation.py](src/sim_compensation.py)

We create a simulation where we:

* pick a random user (defined by similar attributes of the customer base)
* pick a random low number of available agents 
* simulate afiniti engine on or off
* pick a call success based on prior probability
* add a reward depending on the user value outlook

![simulation_detail](../f/f_intertino/simulation_detail.svg)
_simulation details_

The compensations are:

1. **save rate**, all users are equal
2. **risk rate**, effort on the most hard cases
3. **user value**, effort on the most valuable customer

Plus we simulate the effect of the afiniti engine on pairing users and agents:

* off: FIFO logic
* on: the most probable outcome interaction is chosen

### rules of the game

We suppose each agent has persuasive skills which can influence the outcome of the call. We give to the agent the same **persuasive strength** independent on the compensation but **proportional to the compensation**

![call_display](../f/f_intertino/call_display.svg)
_Display during the call with prediction box and compensation in case of success_

We create a set of users and agents following empirical distributions:

![bill_dis](../f/f_intertino/bill_dis.png)
_empirical and simulated distribution of last bill_

For last bill, tenure, and save rate

![bill_dis](../f/f_intertino/saveRate_dis.png)
_empirical and simulated distribution of save rate_


### simulation results

We see comparing to different strategies how the company revenue increases

![sim_revCmp](../f/f_intertino/sim_revCmp.png)
_revenue company in different scenarios_

We have a close up on the revenue uplift for the average across all simulations

![sim_liftCmp](../f/f_intertino/sim_liftCmp.png)
_uplift due to the different strategies_

We want to make sure that the agent compensation is fairly distributed across all agents, and we see a clear increase in agent compensation depending on the strategy

![sim_boxAgn](../f/f_intertino/sim_revAgn.png)
_compensation distribution across all agents_

We see that the company uplift is fairly distributed

![sim_joyAgn](../f/f_intertino/sim_joyAgn.png)
_distributions are not broader_

Finally we can show that the proposed compensation scheme still incentivize the individual ability

![sim_ability](../f/f_intertino/sim_ability.png)
_all the proposed methods increase the compensation together with the agent ability_

We show that the rank correlation on save rate is good across the different compensation, the pairing eingine is increasing the shuffling between agents. The compensation scheme increases shuffling between agents ranking

![sim_corr](../f/f_intertino/sim_corr.png)
_rank correlation across different compensation models_

# tuning

We have few parameters to tune:

* agent commission
* engine influence

What is a **boost** and how can we quantify the **influenceability** vs **motivation** of an agent?
We can set a benchmark with completely unmotivated agents and use it as a baseline for modelling the commission scheme.
We see that the agent compensation delta compared to save rate steadly increases 

![commission_uplift](../f/f_intertino/commission_uplift.png)
_uplift in commission compared from the current scheme_

## targets

Using different methods we can define the targets modifying the save rate by the weighted save rate and maintain a similar reward process

![sim_saveRate](../f/f_intertino/sim_saveRate.png)
_save rate across differente compensation schemes_

# summary

We can predict the **outcome of a call** with a certain accuracy and use our predictive capabilities to shape different simulations. 

The current compensation model is not motivating a win-win strategy for the company and the agent the current targets induce the agent to be as good as the others and don't consider the risk of loosing an high valuable customer

We have simulated different scenarios and fine tune a compensation model to increase the customer retention, the **company revenues** and the **agent personal reward**.

We have shown that compensating an agent proportionally to the risk of the call or the customer value increases both company and personal goals. 

We have shown as well that the increased revenue is **fairly distributed** and even less perfomant agent profit from a change in call distribution and strategy.



# reference


code    : [github]() 
project : [github]() 
article : [match](https://towardsdatascience.com/using-python-stan-to-pick-the-superbowl-winner-with-an-unrealistic-model-e68c84c3e95a)
article : [stan](https://www.mzes.uni-mannheim.de/socialsciencedatalab/article/applied-bayesian-statistics/#applied-bayesian-statistics-using-stan-and-r)
article : [stan](https://mc-stan.org/docs/2_21/reference-manual/hamiltonian-monte-carlo.html) 
