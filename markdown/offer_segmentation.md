# Customer profiling

### Idea

Data structure for real time parallel customer profiliation.
Pretargeting, offer optimization, data structure, segmentation.

## Learning segment performancees

During a web session the parameters, $p_i$, which can be used for segmenting the audience are:
![ancillary](../f/f_intertino/AncillarySketch.png "ancillary sketch")
_Environement parameters and ancillary offers._

* **behaviour**: returning, history, speed
* **item**: which product from the list
* **time**: till usage, booking time frame (h/d/m/y)
* **source**: referrer, searched words, social
* **location**: nation, landscape, quarter, company, weather
* **session**: browser, view, device, provider
* **class**: quality class among similar products
* **travel/specific**: type of group traveling, origin and destination

A learning process can be done correlating the performance of each teaser with the presence of a certain variable, e.g. via a naïve Baysian approach:
$$
  P(t|p_1,p_2,p_3,\ldots) = \frac{P(t)P(p_1|t)P(p_2|t)P(p_3|t)\ldots}{P(p_1,p_2,p_3,\ldots)}
$$
Where $P(t|p_1,p_2,p_3,\ldots)$ is the a posteriori probability of a teaser performance for a given presence of the paramters $p_i$.

Since the number of parameters is around 1000/2000 this process is very inefficient and requires a large learning phase. Most of the environmental variables are correlated and should be hence clamped into macro environemental variables findinf the few functions that define an efficient session scoring.
A big correlation matrix between all parameters should create a comprehensive hit map to guide the simplification and dimensional reduction of the parameter space. 
Second, some parameters shold be more influent in changing the teaser response and a correspondent ``learning weight'' should be assigned to each parameter. 

# Touchpoint crossing

Offer performances should be tracked over different touchpoints to understand which options is the customer considering throughout his journey.
Negative offer performances are as well really important to gain information about the customer. 

![customer_journey](../f/f_intertino/CustomerJourney.png "")
_Customer journey, in red are listed offered product, in orange potential product, in black alternative decisions._


During a journey the customer has to take different decisions and decline an offer might be an important source of information about how he is confindent in the city he is visiting.
For many biforcation points of his route we can consider a payoff matrix like:
$$
  \begin{array}{c c c} & disturbing & non-disturbing\\
    available & a_{11}|b_{11} & a_{12}|b_{12}\\
    non-available & a_{21}|b_{21} & a_{22}|b_{22}\\
  \end{array}
$$
Generally $a_{11},a_{12},b_{12},b_{22}$ are negative. The determination of these parameters allow the estimation of a score about the customer/city link.


# Pretargeting

## Self-consistent mask filtered web marketing

The parallel approach for computing low latency user grouping in web marketing is based on masks that characterize user experiences, web sites and campains.
Each mask has a specific semantic meaning, represents the superposition of different labels on a 2d plane.
The initial calculation of web site and campain masks is supervised and consists in representing the semantic information extracted from web site analytics and marketer expected audience.
The following steps use a self-consistent approach to refine masks and groups in different asynchronous steps. 
The mask of the single user experience is calculated on a peripherical computing center that reads and interprets user actions (from cookies, tracking\ldots).
The masks concerning web sites and campains are calculated on a central computing center by user grouping.
All the masks, histograms and functions are normalized.
\section{Setting (supervised)}
A set of semantic labels or categories (around 20) $\{l_1,\ldots,l_{N_l}\}$ that represent a target audience.
Labels concern audience whishes/interests and product properties, categories might be: amusement, trend, luxus, tech, use \ldots
At the beginning each ad is tagged with a percentage of each label according to the opinion of the marketer. 
![prelude](../f/f_intertino/Prelude.png "")
_Up) representation of a label on the 2d plane. Down) collection of all labels for ads and web sites and interpolated figure._

$$
  a_1 = \{f_1l_1,\ldots,f_{N_l}l_{N_l}\} \qquad \sum_i^{N_l}f_i = 1
$$
The same is done for the web site according to the document analytic
$$
  w_1 = \{f_1l_1,\ldots,f_{N_l}l_{N_l}\} \qquad \sum_i^{N_l}f_i = 1
$$
Each label has a representation on a 2d plane, like arouse-valence plane (the 1d formulation is as well a good alternative). 
$$
  l_i = b_1\mathbf{v}_1 + b_2\mathbf{v}_2\qquad b_1,b_2 < 1
$$
The points might be alternatively regularly placed on a 2d grid.
For each ad and web page we create a mask fitting the points with a Gaussian function.

## Mask

The mask is the central concept of this method, it consists in 20-30 3d points $(x,y,z)$ that are interpolated via a 2d Gaussian. The mask might include in total 100$\times$100 points but the essential information is stored in few tens.
For each mask $i$ we integrate its orthogonal values 
$$
  v_x^i = \int x f(x,y)dxdy \qquad v_y^i = \int y f(x,y)dxdy
$$
We represent all the masks as points on a 2d plane and perform a Delauney triangulation (no need to calculate correlation matrices, highly parallel) to isolate clusters. 
Clusters can be detected via expectation-maximization algorithm.
![harmony](../f/f_intertino/HarmonyCluster.png "harmony cluster")
_Representation of a mask on a 2d plane and consequent clustering analysis on the data on the graph. Each cluster is separated by a hull and for each cluster the average mask is calculated._

For each cluster we calculate the average mask and a list of web pages or ads that belong to that cluster.

# Peripherical (parallel)

From each cookie we read the information about the web sites and the ads clicked and create a user experience mask obtained by the sum of all web and ad masks.
![melody](../f/f_intertino/MelodyUserExp.png "melody")
_Creation of the user experience mask as sum of ad and web relevance._

We perform a convolution with the cluster masks and select the best fitting opportunities.
The best fit might be taken as well as the energy of the system, i.e. the energy closer to the largest value ($L_x\times L_y$) is token.
We show an ad on the web page currently viewed by the user by taking an ad randomly from the set of ads that belong to that mask.
Each separated computing unit communicates the user experience matrix and the the user preferences to the central unit.
```
{"user":[
     "id" : 10245,
     "userexp":[],
     "webuse":[],
     "aduse":[]
]}
```

![melody](../f/f_intertino/MelodyConvolution.png "melody convolution")
_melody convolution_

The computer unit stores information about the user
```
{"user":[
    "id" : 10245,
    "webvisited": [],
    "advisted": [],
    "adseen":[],
    "update":,
    "norm_weight":456732456
]}
```
The ``normweight'', $n_w$, number is used for normalization: if the next mask has weight 1 the former mask is multiplied by $(n_w+1)/n_w$ while the adding mask by $1/n_w$.

## Central

The central unit computes all the user information assigning to each user experience matrix two vectors.
Once the points are updated on the graph performs a cluster analysis and refine the web and ad masks.
The new masks and ad lists are communicated to the external units after the calculation.
Under convergence of points into separated clusters we perform coarse-graining of the information and we define each cluster as a hull.
Each hull represents a different graph database to speed up the computation. 
```
{"cluster":[
    "id" : 102,
    "hull_border": [],
    "u_mask": [],
    "db_address":,
]}
```

Each cluster can be separately processed.

## Infrastructure

Each external unit process the information about a single user with no communication required among different units.
!["orchestra"](../f/f_intertino/Orchestra.png "orchestra")
_Structure of the different computing units and the period segmentation. In the graph are shown the information during the map and the reduce phase._

The central unit computes the masks and communicate the new values to each of the external unit in an asynchronous time.
The external units are completely autonomous and the calculation time of the new masks do not affect the response time of the system.
The masks can be time dependent and different sets of masks might be selected depending on the hour of the day or the day of the week.

## Scalability

Given: 50M users, 10G views, 1M url, 10k pages
$r_{CPO}$ 10\euro{}/order $r_{CPC}$ 1\euro{}/click $r_{CPM}$ 1\euro{}/1000views 
calc time 20ms, 50k calc/s.
The calculations are meant to be performed on the native machine via python or c++ code. The cookies are text analysed after the last update, the masks relative to the visited web site or ad are added to the user experience mask.
During the update phase the new user's mask is mapped into the central unit and the new information are updated in the graph. 
![users](../f/f_intertino/MUsers.png "users")
_Typical graph database per 1M users (ref: [pet project](http://mypetprojects.blogspot.it/2012/06/social-network-analysis-with-neo4j.html)._

According to the performances of Neo4j there should be no large computing time required to precess 50M nodes but different levels of coarse-graining might be introduced in the graph to improve performances. 
That means that different databases might be used to compute different magnification of the graph.

## Revenue/bidding

We know the ad visibility, the page visited and the ad selection.
![revenue](../f/f_intertino/Revenue.png "revenue")
_revenue figures_

We construct the cumulative probability of the revenue summing up each single revenue
$$
  r_{tot} = \sum_i^3 f_ir_i \qquad i \in \{CPO,CPC,CPM\}
$$
Where $r_i$ is the revenue of the offer and $f_i$ its frequency.
We use a random number uniformly distributed, $u$, to select the offer
$$
  r_l = \frac{\sum_i^l f_ir_i}{r_{tot}} \qquad P(l|u) = P(u<r_{l-1} \& u\geq r_{l})
$$

## Refinement

To each ad, $i$, can be set a number that represents the distance of the ad mask to the average cluster mask, $d_c^i$. The ad, instead of being selected with a random probability, might be selected using the cumulative probability of the sum of the distance from the center.
$$
  d_c = \sum_i^{N_{ad}}d_c^{i} \qquad d_c^l =\frac{\sum_i^{l}d_c^{i}}{d_c} \qquad P(l|u) = P(u<d_c^{l-1} \& u\geq d_c^{l})
$$
Where $u$ is a random uniform number.
## Interest filtering

User grouping can be used to let new user filter information about complex content in a web site.
!["dash"](../f/f_intertino/Dash.png "dash")
_Filtering dash based on user grouping_

The dash represents the same categories calculated by user grouping and let the user filter the information by populating the dash.

## Customer feedback score

One of the scoring parameter for a customer is the analysis of the feedbacks he writes in different channels. 

Specific customer feeedbacks were used to train dictionaries for the association of some keywords to specific arguments of sentiments.

![cloud](../f/f_intertino/Cloud.png "cloud sentiment")
_Training of dictionary for topic and sentiment recognition._

The training of the dictionaries is really important for understanding the sentiment of the customer and extract the most relevant words. Those words can be connected to a particular sentiment.  
The customers were asked to choose a category and rate their satisfaction to each comment.
We had then the chance to create topic and sentiment specific dictionaries to be able to automatic guess by user input the most probable reason of his feedback.
We run an emotion recognition to understand which words are more common to different topics.

![comment](../f/f_intertino/Comment.png "cloud sentiment")
_Distribution of sentence length, statistical communality between months._

We have analyzed as well the clustering and the correlation between words to see whether it was necessary to clamp words together or to assign a cluster number to the words.
It is as well important to read general statistical properties of the comment to recognize whether they are formally similar.

![sentence](../f/f_intertino/Sentence.png "sentence")
_Distribution of sentence length, communality between months, distribution of sentence length, statistical communality between months._

In this case we can correlate time periods together to understand which topic are more interesting in particular time of the year.


# Appendix

## Information flux in online sale

Following the thermodynamic example the Gibbs free energy is:

$$  G = U + PV - S\Delta T $$

if we want to translate this concept in terms of business we can say that revenue is the sum of the {\bf service} sold, the {\bf work} done and the {\bf gain in information}.
Sale has a major role the revenue that comes from the first two parts but a proper sale strategy can increase a significant gain in information. In the following we propose a sale oriented strategy with large focus on customer information gain.

![fig](f/f_intertino/InfraSketch.png "fig")
_Sketch of the infrastructure and customer information flow._

Throughout this document we are going to analyze some branches of this sketch.

# Anonymous offer optimization

## Session variables

We consider a session as our variable $x$, for each session we can define a function $g(x)$ that defines
the **revenue in the session**.
$g(x)$ is defined as the sum of the acquired services, we define the ticket, $t$, as the main product and all other products, $\{a_1,a_2,a_3,a_4,\ldots\}$, are ``attached'' to the ticket.
$$
  g(x) = w_tf_t(x) + \sum_{i\in \{a\}}w_if_i(x)
$$
where $w$ is the margin for each sale and $f$ the frequency of sale per session. 
We assume that the probability, $p$, of an ancillary sale is always conditioned by the ticket sale.
$$
  p_a := p(a|t) = \frac{p(a)p(t|a)}{p(t)}=\frac{p(a)}{p(t)} \qquad p(t|a) = 1
$$
where $p$ is the probability correspondent to the frequency $f$.
The metric $m$ is the {\bf session metric} defined as the path to a {\bf conversion}.
The straightes metric for the booking is:
$$
  ProductList - ItemSelection - CustomerDetail - Payment
$$
The formulation of the ticket booking frequency $f_t$ is:
$$
  f_t = f_{list} \cdot f_{it} \cdot f_{cd} \cdot f_{book}
$$
where we call $f_{st}$ the frequency of a generic step conversion.
When the booking comes from an external campaign an additional frequency is added:
$$
  f_t = (1-bouncerate) \cdot f_{list} \cdot f_{it} \cdot f_{cd} \cdot f_{book}
$$
## Variant testing
If we split a page into different variants we influence the frequency of the conversion step:
$$
  f_{st} \to \left\{\begin{array}{c} f^a\\f^b\end{array}\right.
$$
We perform a time average of the two frequencies, $\mean{f^a}_t$, $\mean{f^b}_t$ and find the winning variant performing a t-test
$$
  t_{test} = \frac{\mean{f^a}_t - \mean{f^b}_t}{\sqrt{s_a/N_a + s_b/N_b}}
$$
Where $N_a$ and $N_b$ are the sample sizes and $s_a$ and $s_b$ are the standard deviation of the correspondent frequencies and follow a $\chi^2$ distribution. 
If the difference between state $a$ and state $b$ consists in more than a single change we should consider the influence of each of the $M$ element changes:
$$
  T^2 = \frac{N_aN_b}{N_a+N_b}(\bra{\bar a} - \bra{\bar b}) \mathrm{Cov}_{ab}^{-1}(\ket{\bar a} - \ket{\bar b})
$$
where $\mathrm{Cov}_{ab}$ is the sample covariance matrix
$$
  \mathrm{Cov}_{ab} := \frac{1}{N_a+N_b-2} \sum_{i=1}^{N_a} \Big((\ket{a}_i - \ket{\bar a})(\bra{a}_i - \bra{\bar a}) + (\ket{b}_i - \ket{\bar b})(\bra{b}_i - \bra{\bar b})\Big)
$$

## Probability distribution

The correspondent probability of a number of conversions, $n_c$, in a day $i$, for an action $x_a$, follows the Poisson distribution: ($\Gamma(k) = (k-1)!$)
$$
  p_{st}(n_c,t;\lambda) = \frac{(\lambda t)^{n_c}}{n_c!}e^{-(\lambda t)}
$$
which is comparable to a Gaussian distribution with $\sigma = \sqrt{\lambda t}$ for $\lambda t \geq 10$. 

The probability distribution of a data set $\{n_c\}$ is:
$$
  P_g(\{n_c\}) = \prod_{i=1}^N \frac1{\sqrt{2\pi n_i}}e^{-\frac{(n_i-\lambda_it_i)^2}{2n_c}}
$$
The fitting parameter, $\lambda_i t_i$, can be determined by minimizing the $\chi^2$.
$$
  \chi^2 = \sum_{i=1}^{N_d}\frac{(n_i-\lambda_i t_i)^2}{n_i}
$$
since for Poisson distributions $\sigma_i^2 = n_i$.
If we instead measure a continous quantity attached to the action (e.g. price, $x_p$) we can consider a Gaussian distribution
$$
  p_{st}(x_p) = \frac{1}{\sigma_p\sqrt{2\pi}} e^{-\frac{(x_p-\bar{x_p})}{2\sigma^2_p}}
$$

## Metric noise propagation

We have defined the frequency of bookings $f_t$ as the product of frequencies per conversion step. 
$$
  f_t =  f_{list} f_{it} f_{cd} f_{book} = f_1 f_2 f_3 f_4 \qquad f_t \simeq f^0_t + \sum_{i=1}^4 tial_i f_t \cdot \Delta f_i
$$
The error of the total conversion propagates as follow:
$$
  s_t^2 = \mean{f_t - \mean{f_t}}^2 = \sum_{i=1}^4 (tial_i f_t)^2 s_i^2 = f_t^2 \sum_{i=1}^4 (s_i^2/f_i^2)
$$
Where we have assumed that cross correlations $s_{12},s_{13},s_{14},\ldots$ are all zero because of statistical independence of the different pages since no test is extended on another page. 
That implies that the less noisy metrics are short and defined across simple pages (few biforcation).
The typical noise generated from a Poisson process is the shot noise, which is a white noise and it's power spectrum depends on the intensity of the signal. The signal to noise ratio of a shot noise is $\mu/\sigma=\sqrt{N}$.
To filter out the noise we have to study the autocorrelation function of the time series
$$
  corr_{f_t}(x) = \sum_{y=-\infty}^\infty f_t(y)f_t(y-x) \simeq f_0 e^{-cx} %\mathrm{or} f_0\left(1-\frac{x}{c}\right)
$$
Being a white noise we can clean the signal removing the null component of the Fourier transform:
$$
  f_{clean}(x) = \int \left( \hat f(k) - \frac1\pi\int_\pi^\pi f(x) dx\right) e^{-2\pi\imath xk}dk
$$
All the different variants of the tests (e.g. languages) should have a comparable power spectrum.

## Offer rotation

While the margin parameter $w$ is fixed we can influence $f$ for each product. We start from a former set of frequencies given by a fixed disposition of the offers and we want to abilitate rotation of offers to see how teaser performances change. We should then track the conversion frequency and elasticity dependent on position and area of the teaser.
We consider a row of offers whose probability depends on the ticket sale:
$$
  \ket{a}=\left(\begin{array}{c}p_1\\p_2\\p_3\\p_4\end{array}\right) f_t \qquad  \ket{w} = \left(\begin{array}{c}w_1\\w_2\\w_3\\w_4\end{array}\right)
$$
We want to describe the internal product as a bilinear application on the invariant basis:
$$
  \bra{w}\rho\ket{a} = \frac{\bra{w} H\ket{w}}{\braket ww}
$$
where $H$ projection of $\ket a$ on $\ket w$ and $\rho$ the rotation matrix, $det(\rho)=1$.
$$
H := \left(\begin{array}{c c c c}
  a_{11} & a_{12} & a_{13} & a_{14}\\
  a_{21} & a_{22} & a_{23} & a_{24}\\
  a_{31} & a_{32} & a_{33} & a_{34}\\
  a_{41} & a_{42} & a_{43} & a_{44}\\
\end{array}\right)
$$
Once the original matrix is computed we can apply a rotation $\rho$ a obtain new values for the matrix $H$ and find the combination
$$
max(\bra w H\ket w) 
$$
and calculate the most optimal configurations.
\section{Segmentation influence}
Segmentation should have a direct influence on the offer probability. In this case we are able to add the conversion frequency for each product:
$$
  \ket{a} \to \ket{a} + \ket {a_s}
$$
In this case the optimization quantity will change as follow:
$$
  \frac{\bra{w} H\ket{w}}{\braket ww} \to \frac{\bra{w} (H + H_s)\ket{w}}{\braket ww} =  \frac{\bra{w} H\ket w}{\braket ww} + \frac{\bra{w}  H_s\ket{w}}{\braket ww}
$$
The interest in separating the contribution of segmentation might be of particular interest in case personalization criteria have completely different results.
\section{Session quality measurment}
Another important parameter is the {\bf session quality} which can be defined as
$$
  q(x) := q(x|G_p,G_w,C_l,S_p)
$$
 Which is a function depending on the scores:
* $G_p$ Expenditure capability (maximum budget)
* $G_w$ Expenditure willingness (flexibility in acquiring services)
* $N_p$ Network potential (influence on other travelers)
* $C_l$ Customer loyability (persistance in booking)
* $S_p$ Information Gain
A possible definition of those quantities is:
$$
  G_p := max(g) \qquad G_w := \frac{|g_t - g_{tot}|}{g_{tot}} \qquad C_l := \frac{t_{x}}{\bar t}\frac{m_{x}}{\bar m} \qquad S_p := \sum_i p_i\log\frac1{p_i}
$$
Where $p_i$ is the ratio between teaser conversion and teaser generation.
Session quality is an important score for session 

