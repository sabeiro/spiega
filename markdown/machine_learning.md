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

# Machine learning models and practices

Overview on some of the commonly used machine learning models and their use cases.

# un/supervised learning

* supervised learning: an explicit output variable (y) to predict for classification and regression
* unsupervised learning: no output variable given, for clustering

# gradient boosting

Gradient boosting prefers many shallow models than a single deep model where each model tries to predict the error of the previous chained model.

* ensemble learning: by combining different models the learning is more flexible and less data sensitive 
  * bagging: training different models in parallel sampling from a subset of data (random forest)
  * boosting: training different models sequentially

* adaboost: uses decisions trees in one single split



# xgboost

The extreme gradient boosting 


# hyperparameter tuning

Hyperparameters depend on the specific model although different models share similar components (gradient, loss function, regularization...).

The tuning happens deciding which hyperparameters in which range and steps are going to be otpimized. For each set of hyperparameters the score is calculated using cross validation. The most time consuming way is to calculate the score for each set on a grid. Finer techniques can extrapolate scores without computing every single grid point.

# transformer attention projection

# random forest depth

# L1/l2 regularization

# boosting

