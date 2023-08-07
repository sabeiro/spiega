# Entropy as measure for creativity

$$ E = -\sum_i p_i\log p_i $$

For each midi I consider the information contained in rhythm, chromatism and the total one.
I compute the histograms relative to each single note duration and picth, separately and jointly.


|Song|rhythmic|cromatic|total|
|-|-|-|-|
|Flutto|2.024|5.239|6.56|

I compute the relative distances between songs:


$$ d_{ij}^2 = (E_i^r-E_j^r)^2 +  (E_i^c-E_j^c)^2 +  (E_i^t-E_j^t)^2  $$

and build the graph in neo4j for those songs whose distance is inferior of 0.5.


```
CREATE (Entropy:Measure {label:'measure for creativity'})
CREATE (Aere:Song { id:'0', name:'Aere', entropy:'4.962'})
CREATE (AjdeJano) - [:DIST{d: 0.470}] -> (Prolecic),
```

![distance songs](../f/f_viudi/DistCanzoni.png "dist songs")
_distance between songs_

You can see a clear connection to the songs which is pretty much the one we expect.

The evolution of entropy depends on the author and stabilizes over time, in same cases it shrinks.

![entropy evolution](../f/f_viudi/EntropyEvolution.png "entropy evolution")
_evolution of entropy_

In the graph Bach's ciaccone, lazy bird of Coltrane and Vitali ciaccona where analyzed.

