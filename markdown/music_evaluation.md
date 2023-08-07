# evaluation in music

During a music contest we had to evaluate around 600 bands, 3 songs per band. In the final 6 bands are accepted.
There are 5 groups of 10 jurys, each group evaluate 120 bands, 360 songs in total.
To provide an accurate evaluation of those bands we need to find good criteria to sort and compare songs genre independently.

# quantitative measurement

Usually a quantitative measure of quality is tricky, especially if all features have the same weight, the resolution of the scores is not high enough and the final score is an arithmetic sum.

We take a classical score from 1 to 10. Ideally fractional but the difference between 7.1 and 7.2 are really hard to define so most of the scores will be at the end integers. For each band the total score is the mean score of the 3 songs. 
6 is sufficient, most of the score will be dense around 6-8, 9 is a great performance, 10 is exceptional. The limited resolution of the features will create a really flat evaluation making really difficult to rank the bands. 

The arithmetic sum creates distortions because a feature centered around an higher value should not contribute to an overall higher score. The difference in variace between features distorts the total evaluation making ranking ineffective. We therefore substract the feature value by the feature mean so flat features don't contribute to the final score.


## criteria 

Let's define some criteria

| non trivial| melody| text| sound| master| singing| accompany| arrangement| rhythm| bonus|

The evaluation should be normalized by genres, i.e. the rhythm of a rock song should be relative to rock considering that the maximum increamental variations should reach a maximum of 10.

