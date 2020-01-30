# traffic on motorways
## counting locations
Across germany there are thousands of counting locations on the main roads and the count of vehicle crossing the section of the street is (https://www.bast.de/BASt_2017/DE/Verkehrstechnik/Fachthemen/v2-verkehrszaehlung/Stundenwerte.html?nn=1817946")[public]



<p><img src="f_via/bast_germany.png" title="BaSt Germany" alt="bast_germany" /> <em>BaSt Germany</em></p>
<p>For each of those location we select a pair of openstreetmap nodes (arrows) for the same street class.</p>
<p><img src="f_via/via_tile_selection.png" title="via tile selection" alt="via_tile_selection" /> <em>For the same BaSt location the tile intersects more streets</em></p>
<p>To stabilize over year we build an isocalendar which represents each date as week number and weekday. We see that isocalendar is pretty much stable over the year with exception of easter time (which shifts a lot).</p>
<p><img src="f_via/isocal_deviation.png" title="isocalendar deviation" alt="isocal_deviation" /> <em>isocalendar deviation</em></p>
<h2 id="data-set-preparation">data set preparation</h2>
<p>We take hourly values of BaSt counts and we split in weeks. Every week is represented as an image of 7x24 pixels.</p>
<p><img src="f_via/timeSeries_img.png" title="time series" alt="time_series" /> <em>image representation of time series</em></p>
<p>The idea is to profit from the performances of convolutional neural networks to train an autoencoder and learn from the periodicity of each counting location.</p>
<p>Convolutional neural network usually work with larger image sizes and they suffer from boundary conditions that creates a lot of artifacts.</p>
<p>That's why we introduce backfold as the operation of adding a strip to the border from the opposite edge.</p>
<p><img src="f_via/backfold.png" title="backfolding" alt="backfold" /> <em>backfolding the image</em></p>
<p>In this way we obtain a new set of images (9x26 pixels)</p>
<p><img src="f_via/timeSeries_backfold.png" title="time series" alt="time_series" /> <em>image representation of time series with backfold</em></p>
<p>And produce a set of images for the autoencoder</p>
<p><img src="f_via/img_dataset.png" title="img dataset" alt="dataset" /> <em>image dataset</em></p>
<h2 id="model-definition">model definition</h2>
<p>We first define a short convolutional neural network</p>
<p><img src="f_via/shortConv_3d.png" title="short conv net" alt="3d" /> <em>short convNet in 3d</em></p>
<p>We than define a slightly more complex network</p>
<p><img src="f_via/convNet_3d.png" title="conv net" alt="3d" /> <em>definition of a conv net in 3d</em></p>
<p>In case of 7x24 pixel matrices we adjust the padding to achieve the same dimensions.</p>
<h2 id="training">training</h2>
<p>We fit the model and check the training history.</p>
<p><img src="f_via/history.png" title="training history" alt="history" /> <em>training history</em></p>
<p>Around 300 epochs the model is pretty stavle and we can see the morphing of the original pictures into the predicted</p>
<p><img src="f_via/morph_noBackfold.png" title="morph no backfold" alt="morphNo" /> <em>raw image morphed into decoded one, no backfold</em></p>
<p>If we introduce backfold we have a slightly more accurate predictions</p>
<p><img src="f_via/morph_shortConv.png" title="morph short convolution" alt="morph" /> <em>raw image morphed into decoded one, with backfold</em></p>
<p>The most complex solution comes with the deeper model</p>
<p><img src="f_via/morph_conv.png" title="morph conv" alt="morphConv" /> <em>morphing for convNet</em></p>
<h2 id="tuning">tuning</h2>
<p>We worked to tune the network to avoid the system to fall in a local minimum</p>
<p><img src="f_via/local_minimum.png" title="local minimum" alt="mimimum" /> <em>training is trapped in a local minimum</em></p>
<h2 id="results">results</h2>
<p>At first we look at the results of the non backfolded time series</p>
<p><img src="f_via/shortConv_noBackfold.png" title="short convolution" alt="shortConv" /> <em>results for the short convolution, no backfold</em></p>
<p>If we add backfold we improve correlation and relative error</p>
<p><img src="f_via/shortConv_week.png" title="short convolution" alt="shortConv" /> <em>results for the short convolution</em></p>
<p>The deepest network improves significantly the relative error but as a trade off loose in correlation</p>
<p><img src="f_via/convNet_backfold.png" title="convNet wbackfold" alt="convNet" /> <em>convNet results with backfold</em></p>
<h2 id="scores">scores</h2>
<p>The deepest network improves drastically the relative error sacrifying the correlation</p>
<p><img src="f_via/boxplot_corErr.png" title="boxplot" alt="boxplot_corErr" /> <em>boxplot correlation and error difference between models</em></p>
<p>Correlation not being in the loss function is really disperse while optimizing</p>
<p><img src="f_via/confInt_score.png" title="confidence interval scoring" alt="confInt" /> <em>confidence interval for correlation and relative error</em></p>
<p>Ranking is not stable among the different methods</p>
<p><img src="f_via/sankey_backfold.png" title="sankey diagram" alt="sankey" /> <em>Sankey diagram of correlation shift between different methods</em></p>
<p>Different methods behave differently wrt the particular location</p>
<p><img src="f_via/sankey_error.png" title="sankey diagram" alt="sankey" /> <em>sankey diagram of error reshuffling</em></p>
<p>The deepest network tend to amplify the bad performances in correlation</p>
<p><img src="f_via/parallel_correlation.png" title="parallel correlation" alt="parallel" /> <em>parallel diagram of correlation differences</em></p>
<p>The short backfolded model has the worse performances for locations that had the best performances in the non backfolded version</p>
<p><img src="f_via/parallel_error.png" title="parallel error" alt="parallel" /> <em>parallel diagram of relative error</em></p>
<h2 id="dictionary-learning">dictionary learning</h2>
<p>We perform a <em>dictionary learning</em> for knowing the minimal set average of time series to describe with good accuracy any location. For that we will use a KMeans</p>
<pre class="python3"><code>clusterer = KMeans(copy_x=True,init=&#39;k-means++&#39;,max_iter=600,n_clusters=4,n_init=10,n_jobs=1,precompute_distances=&#39;auto&#39;,random_state=None,tol=0.0001,verbose=2)
yL = np.reshape(YL,(len(YL),YL.shape[1]*YL.shape[2]))
mod = clusterer.fit(yL)
centroids = clusterer.cluster_centers_</code></pre>
<p>We start with the most common time series and we calulate the score of all locations on that cluster</p>
<p><img src="f_via/cluster_1.png" title="1 cluster" alt="cluster" /> <em>most frequent cluster</em></p>
<p>We realize the 90% of the locations and weeks have a correlation higher than 0.9</p>
<p><img src="f_via/cluster_kpiDis.png" title="cluster kpi distribution" alt="cluster_histogram" /> <em>kpi distribution for single cluster</em></p>
<p>A single cluster is already a good description for any other location but we want to gain more insight about the system. We than move the 2 clusters to classify the most important distintion between locations which we will call &quot;touristic&quot; and &quot;commuter&quot; street classes.</p>
<p><img src="f_via/cluster_2.png" title="2 cluster" alt="cluster" /> <em>most 2 frequent clusters, touristic and commuter</em></p>
<p>We can extend the number of cluster but we don't significantly improve performances</p>
<p><img src="f_via/cluster_24.png" title="24 cluster" alt="cluster" /> <em>most 24 frequent clusters</em></p>
<p>If we look at the KPIs distribution 4 clusters are the best trade-off between precision and computation</p>
<p><img src="f_via/cluster_cumulative.png" title="cluster cumulative" alt="cluster_histogram" /> <em>cumulative histogram for correlation and relative error</em></p>
<p><img src="f_via/cluster_histogram.png" title="cluster cumulative" alt="cluster_histogram" /> <em>histogram for correlation and relative error</em></p>
<p>If we look at the most 4 frequent clusters we see that they are split in 2 touristic and 2 commuters.</p>
<p><img src="f_via/cluster_4.png" title="4 cluster" alt="cluster" /> <em>most 4 frequent clusters</em></p>
<p>We want than to see how often a single location can swap between commuter and touristic and we see that locations are strongly polarized though all the year</p>
<p><img src="f_via/cluster_polarization.png" title="cluster polarization" alt="cluster_polarization" /> <em>cluster polarization</em></p>
<p>If we look at the weekly distribution we see that the commuting pattern ressamble our expectation</p>
<p><img src="f_via/commuting_pattern.png" title="commuting pattern" alt="commuting_pattern" /> <em>commuting pattern strength through all locations</em></p>
<p>To compute a common year we build an isocalendar which is the representation of a year into</p>
<h2 id="via-nodes">via nodes</h2>
<p>To select the appropriate via nodes we run a mongo query to download all the nodes close to reference point. We calulate the orientation and the chirality of the nodes and we sort the nodes by street class importance. For each reference point we associate two via nodes with opposite chirality.</p>
<p>We can see that the determination of the via nodes is much more precise that the tile selection.</p>
<p><img src="f_via/via_algo.png" title="identification of via nodes" alt="via_algo" /> <em>identification of via nodes, two opposite chiralities per reference point</em></p>
<p>The difference is particular relevant by junctions</p>
<p><img src="f_via/junction.png" title="via nodes on junction" alt="junction" /> <em>via nodes on junctions, via nodes do not count traffic from ramps</em></p>
<h2 id="morph-external-data">morph external data</h2>
<p>Once we have found the best performing model we can morph our input data into the reference data we need</p>
<p><img src="f_via/join_plot.png" title="distribution of via and tile counts" alt="join_plot" /> <em>distribution of via and tile counts compared to BaSt</em></p>
</body></html>
