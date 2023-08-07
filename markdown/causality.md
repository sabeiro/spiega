[blog](https://www.researchgate.net/post/Any_recommended_techniques_for_testing_causal_relations)
##  Jochen Wilhelm

IMPORTANT: NO regression technique, NO statistical analysis at all can test a causal relationship. Causality is no property contained in the data. The ONLY way to adress causality is to perform a controlled experiment, where you know, a priory, that only the arbitrarily changed condition (and nothing else) can be responsible for a possible change in the response. If you have only observational data (what is often the case in econometrics), you can only speculate or hypothesize about causal relations. A correlation of the respective variables would then be "in accordance" with such a speculation, but it will never be a proof, not even a strong support. And the lack of a correlation would *not* indicate that there is no causal relation.

## Mohammad Tahir
Path coefficient analysis of the dependent and independent variables partitions the correlations into the so called direct and indirect effects. It enables us to argue about the causality of independent variables with reference to dependent variables. I would not specifically refer to the data in question. However, there should be some hypothesized relationship existing between the independent and dependent variables.
Other alternative is using the technique of Simultaneous Equation Modeling (SEM).
Hope it helps.

## Fabrice Clerot
1- complete agreement with Jochen above : causality is not the data unless such data come out of a controlled experiment !
2- now, if you want to go on with something which is somehow a "statistical proxy" for causality, you can try to go along with "Granger causality" (although the name itself seems to me misleading as it is indeed a sophisticated correlation analysis which tries to capture some properties commonly associated with causality) ... but beware of the many technicals traps !
see also the discussion below :
https://www.researchgate.net/post/Cause-effect_dilemma2

## Patrick S Malone
Malone Quantitative
I essentially agree with Jochen, but with some caveats. First, even an experiment requires certain assumptions to make a strong inference of causality, which can be especially challenging in a field and/or longitudinal study.
Second, there *are* techniques for plausible causal inference without those conditions, or in an observational study, but they require rather strict assumptions. In econometrics, the most common to my knowledge is an instrumental variable approach, which may get you started on finding didactic papers and chapters. Again, the assumptions required are fairly technical and not to be taken lightly, especially with observational data. Consulting with an expert on causal inference is a good idea.
I am going to respectfully disagree with Mohammad. In recent years, the traditional path modeling approach to partitioning direct and indirect effects has increasingly come under fire as a flawed method for inferring causality except in limited cases. Pearl, Imai, and Mackinnon, among others, have written extensively on this.

## Jochen Wilhelm
Justus-Liebig-Universität Gießen
Patrick, thank you for your additions.
You are right that longitudinal studies, even with experimental intervention, can be problematic to infere causal relationships. Here, to my (limited) knowledge, an appropriate control group is obligatory, since anything can change over time, and often some unconsidered variable changing over time is the common reason for the variables under investigation changing, what automatically results in an apparent (but spurious) correlation.
Am am not an expert in causal inference, but I suppose that the "rather strict [and] fairly technical [...] assumptions" eventually just assure that the data can be used as if it was from a well-controlled experiment. Under the bottom line, it seems to me again that data alone can be no means provide any hints for (or against) causality. Causality remains a concept outside of the data that has to be tackled with logical arguments (and design of experiments) rather than with data. This might possibly me a little too strong position, though, but that's so far my understanding.


## Paul Louangrath
There seems to be confusions about whether to use linear regression or not. The decision to use regression is not a matter of personal choice or preference. Whether regression is applicable depends on the nature of the data. A model by definition is a mathematical statement that could best describe the behavior of the data set, i.e. a model must be best fitted to the data distribution.
LINEARITY
Test whether the data is normally distributed. If so, then linear regression is applicable. If linear regression is used, test of significance may be applied by using:
(1) t(r) = r(sqrt. (n -2) / sqrt. (1 – r^2)
NON-LINEAR
If the data distribution is nonlinear, then nonlinear modeling is used. In so doing, one needs to visually inspect the scatter graph/plot of the data to see the pattern and then decide of what can be best fitted, i.e. parabolic, logistic, etc.
DISTRIBUTION TYPE VERIFICATION
The character of the data distribution may be verified through the Anderson-darling test. AD test allows the researcher to verify whether the data is normally distributed. Normal distribution is directly tied to linear regression. Generally, for a 0.95 confidence interval, the critical value for the AD test is 0.787. If the result A^2 (read A square) exceeds 0.787, then one can conclude---through methodological verification supported by empirical data not personal reference of whether one likes or dislike linear regression---that a non-linear model is necessary. The A^2 formula follows:
(2) A^2 = -n – S
… where n = sample size and S is given by:
(3) S = sum (2k – 1)/n [nl(F(Y)) + ln(l – F(Y*)]
The term F(Y) is given by:
(4) F(Y) = (X – mu)/sigma
… where X = individual observation, mu = mean, and sigma = standard deviation.
BOOTSTRAPPING ANDERSON-DARLING TEST
To guard against Type I error, one needs to run the Anderson-darling test in sequence. Each sequence may be comprised of n > 5 data points. If the result shows that at certain sequence A^2 = normal distribution and at subsequent point A^2 = nonnormal then it is clear that linear regression is not applicable. This decision NOT to use regression model is supported by empirical evidence, not personal preference or hunches.
STATISTIC TEST UNAVOIDABLE
A proposed model is a proposed hypothesis. Acceptable practice in basic research must demonstrate that the proposed model could be substantiated with a certain level of confidence, i.e. 0.95 in social science or as high as 0.9975 in some pharmaceutical research. Hypothesis test and confidence procedures are indispensable in model verification. This statistical tool serves three functions: (i) reliability assurance, (ii) scientific objectivity capable of independent reproducibility and (iii) guard against inferential errors, i.e. Type I and Type II error.
RELIABILITY TEST
To be acceptable, the model must be reliable. To be reliable, the model in the present study must be able to reproduce the same or similar result in subsequent study independent researchers. Reliability test is achieved through correlation analysis. Again this is statistical analysis. Followings are possible lists of various test for reliability (depending on the nature of the data and research question involved):
-Weilbull reliability
-Spearman-Brown prediction formula
-Test-retest
-Parallel forms
-Split half
-Cronbach’s alpha (internal consistency test)
-Cohen’s kappa
-Fleiss’ kappa
-Intraclass correlation
-Kuder-Richardson formula-20
Failing applicable reliability test, the proposed model is nothing more than an algebraic formula. It would lack scientific value.

## Jochen Wilhelm

Paul, I don't agree with several points you made. Either these points are wrong or I am missing a deeper understanding (and I am wrong):
Linearity of the relationship has nothing to do with a normal distribution of the data. Further, I suspect that trhere might be some confusion of "linear regression" and "linear models".
(1) Not the data needs to be normal distributed but the errors/residuals of the applied model. The model may well model some non-linear relationship between the response and the predictors.
(2) The statement that "Normal distribution is directly tied to linear regression" is wrong. It would be more correct the other way around, like "linear regression is directly tied to Normal distribution".
(3) Testing for normal distribution is not helpful. The H0 is wrong on a priory gounds. Therefore, doing a test to reject H0 is nonsense. But if this is ignored and the test is done anyway, there are more difficulties: When the test is underpowered, relevant deviations can be overlooked. When the test is overpowered, negligible deviations will become "significant". There is no statement about the size or character of a minimal relevant deviation (i.e. about the adequate power).
(4) "Hypothesis test and confidence procedures are indispensable in model verification." is also wrong. A Hypothesis test is a statement about the probability of the data *given* the hypothesis (and *given* the model). It is NOT a statement about the validity, reproducibility, reliability or what else of the hypothesis or of the model.
I'd say that such a proposed reliance on hypothesis tests "lack scientific value".
NB: a model is function of one or more predictors providing (by some criteria "optimal") estimates for the response. The functional form of the model is selected on logical grounds. The model contains parameters/coefficients which values are determined to achieve an "optimal" prediction for the given data. "Optimal" typically means that the observed response values would have the highest likelihood. The likelihood is obtained from our expectations about the residuals, and this is formulated in an adequate probability distribution. Which distribution this should be depends on known or assumed constraints and properties of the residuals. A linear model is a model where the parameters in the model are all untransformed (i.e. "linear"). Such functions can be written as a "weighted sum" of the predictors, with the parameters as the weight factors (interpretable as effect sizes). This has nothing to do with a linear relationship between the variables. Unless otherwise stated it is understood that the residuals are modelled using the normal distribution, often because then there is a technically simple least-squares solution to get the maximum likelihood. Therefor one can say that "linear models are tied to normal distribution". But other probability distributions can be used. The models are then denoted as generalized linear models. Although in principle not different from linear models, the algorithms to find the maximum likelihood are different because the "least-squares shortcut" does not work here anymore. Further, if the adequate function can not be written as a weightet sum, just the algorithms to find the maximum likelihood has to be changed. Such generalized non-linear models are in principle nothing different, too.
NB2: "linear regression" is a special case of a linear model, particularily the model Y(X) = b0 + b1*X + e where e~N(0,s²). b0 and b1 are the parameters (here interpretable as intercept and slope of a straight line). The values for b0 and b1 are estimated from the data of the predictor X (x1,x2...xn) and the response Y (y1,y2...yn) by maximizing the likelihhod of the errors e (e1,e2...en):
ei = yi-(b0+b1*xi)
Under independence, the likelihood is
Lik = P(e1) * P(e2) * ... * P(en)
Lik = P(y1-(b0+b1*x1)) * P(y1-(b0+b1*x2)) * ... * P(y1-(b0+b1*xn))
The probabilities are taken from the normal distribution. To detemine the maximum likelihood, some algebra shows that the variance is irrelevant. For confidence intervals, the likelihood over all parameters plus the variance estimate has to be considered and the profile likelihood can be taken to define the limits for a given level of confidence. The profile likelihood hat the functional form of a t-distribution. For convenience, Fisher (and/or Gossett) provided a standardized form of this distribution, so that proabilities could be derived for an easy-to-calculate pivot of the data. This pivot contains a normalization factor what is known as the standard error.

## Paul Louangrath

Jochen,
Thank you for putting some thoughts into the issue. Several points follow to your comments:
(1) DATA TEST
It is not suggested that the data "must be" normally distributed. However, the purpose of testing if the data is normally distributed is to confirm whether it is normally distributed or something else.
(2) LINEAR REGRESSION & NORMAL DISTRIBUTION
Our understanding is consistent on this point. My writing might have put in in reverse :).
(3) TEST FOR NORMAL DISTRIBUTION
This is related to No. (1) regarding "linear regression."
(4) HYPOTHESIS & CONFIDENCE INTERVAL
Noted that we have fundamental differences in view points on this issue. See (5).
(5) SCIENTIFIC VALUE OF HYPOTHESIS TEST & CONFIDENCE INTERVAL
In pharmaceutical testing, it is indispensable especially in testing new drugs. One of the reasons why it takes 10 to 15 years to get a new drug to the market is that it is necessary to test and retest by the original lab and independent labs. Drug efficacy and the rate of toxicity tests all employ hypothesis test and confidence interval procedures. In other fields, such as economics, where the term "scientific method" is also used, hypothesis test and confidence interval procedures may not always be employed because one deals with different types of data and assumptions. However, to say that hypothesis test and confidence procedures have no scientific value would be incorrect. As a general practice in biology, biochemistry, pharmacology and epidemiology or even in social science, such as marketing research, hypothesis test and confidence interval procedures are still employed as conventional tools.
(6) LINEAR REGRESSION & LINEAR MODEL
Here lies of disagreement. I was looking in the perspective of linear regression (i.e. biostatistics).
I appreciate and thank you for your additional points on NB1 and NB2.

## Jochen Wilhelm

Thank you for your feedback, Paul.
I find your point (5) interesting. You use pharmaceutical testing as an example here. To my understanding, clinical trials performed to approve drugs for the market is *not* science. These studies are neither planned nor conducte to *learn* something but rather and explicitly to provida an empirical basis for a decision (approve or not). This is an important and useful tool - don't get me wrong here! - but actually it not science. The testing procedure is required for a quality control on the level of the society, for the population of all drugs that are on the market.
But there is still another point: "that is necessary to test and retest by the original lab and independent labs.". No doubt that this is right, but: if the test is believed to keep the desired error-rates, why should a re-testing be necessary or even important?
And, finally, "As a general practice in biology, biochemistry, pharmacology and epidemiology or even in social science, such as marketing research, hypothesis test and confidence interval procedures are still employed as conventional tools." - I know well. But the mere frequency of useage is no indication of its meaningfulness. If you would remove all papers showing hypothesis tests where the authors are not able to explain correctly what the meaning of a p-value or a "significant" result is, there would'nt be many papers left.
PS: I think that hypothesis testing is an important tool to control error-rates in industrial or economic processes (like drug approvals), but I also find that the reduction on "significant effects" is highly adverse. The effect sizes are more important, and aditionally there are many more parameters to look at, especially regarding drugs, like side-effects, compliance, costs(!), ethical issues, and much more. All these points *should* be considered when approving a drug. Unfortunately, there is no simple and purely mathematical procedure to account for all this, and this is a red flag for many people/doctors/politicians/bosses who want to have a one-for-all numerical value, seemingly easy to interpret, and calculated in an "objective" way.

# deeplearning resources

https://csml.som.ohio-state.edu/Huron/Publications/orpen.similarity.text.html
https://www.shanelynn.ie/word-embeddings-in-python-with-spacy-and-gensim/
https://www.datacamp.com/community/tutorials/deep-learning-python
https://towardsdatascience.com/gan-by-example-using-keras-on-tensorflow-backend-1a6d515a60d0
http://adventuresinmachinelearning.com/keras-tutorial-cnn-11-lines/
https://machinelearningmastery.com/keras-functional-api-deep-learning/
https://www.pyimagesearch.com/2018/04/16/keras-and-convolutional-neural-networks-cnns/
https://github.com/memo/webcam-pix2pix-tensorflow
https://towardsdatascience.com/bayesian-linear-regression-in-python-using-machine-learning-to-predict-student-grades-part-2-b72059a8ac7e
https://medium.com/@williamkoehrsen

