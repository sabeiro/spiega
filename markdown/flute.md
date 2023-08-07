# Flute calculator
[ref](https://kassaflutes.com/articles/flute-calculator)
## Variables
In order to properly calculate the placement of toneholes on a flute, several variables come into play. They are:
$$ \( L_{eff} \) $$
<td>The <strong>effective tube length</strong> associated with each desired note. This is the length the flute would be <em>theoretically</em> if it were “uncomplicated by end corrections, toneholes, and the like” (Hopkin, p.18). For flutes that are open at both ends (the blowhole constitutes an open end), this length is equal to the ½ the actual wavelength of the note itself.</td>
</tr><tr><td>\( v_{sound} \)</td>
<td>the <strong>speed of sound</strong> in air, which varies depending on the temperature and the humidity of the air. Since our variable \( L_{eff} \) above is equal to ½ the wavelength of a given note, we need \( v_{sound} \) to be able to calculate the wavelength of that note. (We’ll automatically calculate the speed of sound for our environment below.)</td>
</tr><tr><td>\( A \)</td>
<td>The <strong>actual tube length</strong> of the desired lowest note of the flute. We use the <em>effective</em> tube length \( L_{eff} \), above, to <em>estimate</em> the actual length — but we won’t know the <em>actual</em> length of the flute until we have reduced the flute’s length down until it produces the correct note. We need the actual length of <em>just the lowest note</em>, however, in order to accurately position the rest of our toneholes using the <em>tonehole correction factor</em>, that we will calculate below.</td>
</tr><tr><td>\( C \)</td>
<td>The <strong>tonehole correction factor</strong> — this is really the crux of the matter and what we are after; it is the amount the hole position must be displaced from the effective tube length (above), given the variables that follow:</td>
</tr><tr><td>\( d_t \)</td>
<td>the <strong>internal diameter</strong> of the tube</td>
</tr><tr><td>\( d_h \)</td>
<td>the <strong>diameter of the tonehole(s)</strong>
</td>
</tr><tr><td>\( t_e \)</td>
<td>the <strong><em>effective</em> thickness of the tonehole</strong> (this is the flute’s wall thickness <em>plus</em> some end corrections that depend on the diameter of the hole). \( t_e\ =\ t\ +\ .75d_h \)</td>
</tr><tr><td>\( s \)</td>
<td>the distance between \( L_{eff} \) for the hole in question and \( L_{eff} \) for the next hole below (or the entire tube in the case of the first open hole)</td>
</tr></tbody></table></div>
</div><div id="block-19" class="content-block   type-php-include  col-md-12 ">
<div class="block-inner "></div>
</div><div id="block-21" class="content-block   type-php-include  col-md-12 ">
<div class="block-inner "><div id="equations-block">
<h3>Equations</h3>
<p>We&rsquo;ll calculate these equations automatically with the tools below, but so we know what&rsquo;s being done, the equations are provided here.</p>
<p>Using the above variables, the equation used for calculating the amount of tonehole correction (\( C \)) and thus the placement of each tonehole is:</p>
<div class="well math">$$ C\ =\ s/2\ [\sqrt{1\ +\ 4(t_e\ /\ s)\ (d_t\ /\ d_h)^2}\ -\ 1] $$</div>
<p>Once we have determined the tonehole correction (\( C \)), the location of each individual tonehole (\( L_h \)) can then be calculated using:</p>
<div class="well math">$$ L_h\ =\ L_{eff}\ -\ C $$</div>
<h3>Tube Lengths</h3>
<p>To start building our flute, we need to know how long, initially, to make the tube that will become our flute — in other words, we need to know the <em>effective</em> tube length (\( L_{eff} \)) for our <em>lowest note</em> (the note that will play with all holes closed). To find that initial length, we need the frequency of the lowest note, and the speed of sound at the temperature in which we are working. With those two, we can find the wavelength (\( \lambda \)) of the note by dividing the speed of sound (\( v_{sound} \)) by the frequency (\( f \)):</p>
<div class="well math">$$ \lambda\ =\ v_{sound}\ \div\ f $$</div>
<p>For example, if the lowest note were middle C (261.63 <small>Hz</small>), we would take the speed of sound (34600 cm/second) and divide by the frequency, 261.63, to get its wavelength:</p>
<div class="well math">$$ 34600\ /\ 261.63\ =\ 132.25\ cm $$</div>
<p>Finally, to arrive at our <em>effective</em> tube length \( L_{eff} \) we simply divide in half (for a flute that is open at both ends):</p>
<div class="well math">$$ (34600\ /\ 261.63)\ \times\ .5\ =\ 66.125\ cm $$</div>
<p>So, for a theoretical flute that was intended to have middle C as its lowest note, we would start by making the flute about 66 cm, and then slowly trim it down from there until the flute produced the desired note&hellip;thus arriving at our <em>actual length</em> (our variable \( A \)).</p>
</div>
<h2>The Procedure</h2>
<p>The procedure at this point for making our flute, using the below tools to do the heavy mathematical lifting, looks like this:</p>
<ol>
<li>Start by specifying your environment variables (temperature and humidity). This will give you a more accurate speed of sound calculation. <em>Note:</em> you might want to play around with these numbers, and the reason is this: while the temperature and humidity of the room you&rsquo;re working in will naturally be a starting point, ultimately it&rsquo;s important to think of the temperature <em>inside</em> the flute — this temperature will be raised by the player&rsquo;s breath. I usually bump the temperature up a few degrees to account for this.</li>
<li>Using the generated \( L_{eff} \) values in <em>Chart #1</em> as reference for the length of the flute at the lowest note, first make the flute, with <em>just the embouchure and blowhole completed</em>, and cut flute to length so lowest note can be played to pitch. </li>
<li>Once that is done, measure from the <em>center of the blowhole</em> to the far end of the flute: this value is the <code>Actual Length</code> that you&rsquo;ll need to input below (along with some other specs about your flute).</li>
<li>Once you have the <code>Actual Length</code>, fill out the &ldquo;Tonehole Placement Calculator&rdquo; form below to get the calculated tonehole location, for each note.</li>
</ol>
<div class="panel panel-default">
<div class="panel-heading">
<h3 class="panel-title">Temperature and Humidity</h3>
</div>
<div class="panel-body">
<p class="text-muted">Use custom temperature and humidity to calculate the speed of sound that matches your playing environment. <small>(Think <em>inside</em> the flute — ultimately it will be a few degrees warmer than the room temperature.)</small></p>
<form class="form-inline embed" id="update-leff-chart">
<div class="form-group">
<div class="input-group">
<input type="number" class="form-control" value="70" min="32" max="86" step="1" name="temperature">
<div class="input-group-addon">&deg;F</div>
</div>
</div>
<div class="form-group">
<div class="input-group">
<input type="number" class="form-control" value="50" min="0" max="100" step="1" name="humidity">
<div class="input-group-addon">% humidity</div>
</div>
</div>
<button type="submit" class="btn btn-sm btn-primary" id="leff-updater">Update Chart</button>
</form>
<p class="text-muted">Speed of sound: <span class="sos"></span> cm/s</p>
</div>
</div>
<h3>Chart #1</h3>
<p>Based on the variables above, the below chart shows the calculated values of wavelength and \( L_{eff} \) for all of the common notes found on a three-hole Fulani flute. You can refer to this chart to determine the <em>approximate initial length</em> of the flute for the desired lowest note:</p>
<div id="leff-chart">
<p><i class="fa fa-spin fa-spinner"></i> Loading chart...</p>
</div>
<h3>The Tonehole Location Calculator</h3>
<p>At this point, theoretically, you would have a flute with just a blowhole and no toneholes. The flute should be able to play the lowest note, and as such, you should know the <code>Actual Length</code> value. Now, fill in the rest of the variables below as they pertain to your flute, and submit the form.</p>
<p class="highlight-text bg-warning"><i class="fa fa-info-circle"></i> If you&rsquo;re just kicking the tires to see how it works, trying selecting the &ldquo;Key of G&rdquo; preset, and filling in &ldquo;65&rdquo; for the Actual Length. Feel free to change the other values.</p>
<hr>
<div id="tonehole-calculator">
<p><i class="fa fa-spin fa-spinner"></i> Loading calculator...</p>
</div>
<hr>
<div id="form-results"></div>
<h3>Conclusion</h3>
<p>And there you have it! Once you&rsquo;ve submitted the form, you should see the locations of the toneholes for each of the notes you specified. If you were careful with your initial calculations and measurements, these locations should be fairly accurate — but start by making the tonehole very small (just big enough to sound a note), and then <em>slowly</em> increase the size of the hole until the desired note is achieved. The bigger the hole, the sharper the note becomes. Furthermore, enlarging the hole <em>towards the embouchure end</em> of the flute will raise the note&rsquo;s pitch more, while enlarging it towards the other end (away from the blowhole) will help keep the note lower (in case you overshot and need to compensate).</p>
<hr>
<p class="highlight-text bg-info">
<i class="fa fa-question-circle"></i>
This tool was created by <a href="http://davekobrenski.com" target="_blank">Dave Kobrenski</a> and is for educational and reference purposes. If you find it useful, <a href="http://www.davekobrenski.com/connect/">let me know</a>.
</p>
</div>
</div></div><div class="row">
<div class="col-md-12">
<div class="post-footer-actions">
<div class="post-cta"><p class="post-categories " style="float:none!important">
Posted in: <a href="/articles/category/Flute-Making-Tools">Flute-Making-Tools</a>, <a href="/articles/category/Articles">Articles</a>
</p><div class="clearfix"><br></div></div> 
</div>
</div>
</div>
<div class="row hidden">
<div class="col-md-12">
<hr>
</div>
</div><section class="post-author-details">
<h3 class="author-title">About the Author</h3>
<div class="row">
<div class="author-avatar col-sm-2 col-md-2">
<img src="https://secure.gravatar.com/avatar/d8cc43cb14273c7c2031cf7c8ab895eb?s=150&amp;d=identicon" class="img-responsive img-circle">
</div>
<div class="author-bio col-sm-10 col-md-10">
<h3 class="author-name">
About the Author<span class="hidden">: <em>Dave Kobrenski</em></span>
</h3>
<p><a href="http://davekobrenski.com" class="external">Dave Kobrenski</a> is a musician, artist, author, and performer. Between 2001 and 2016, he traveled extensively in West Africa to study music with master musicians such as Famoudou Konaté, Nansady Keita, Sayon Camara, and other musicians of the region. He studies the African flute with a master of the Malinké flute tradition, Lanciné Condé.</p>
<p>Dave plays the Fulani flute, kamale ngoni (10-string Mande harp), djembe, balafon, and guitar, and currently performs with the <a href="http://donkilomusic.com" class="external">Donkilo! Afro Funk Orkestra</a>, as well as with <a href="http://landaya.com" class="external">Sayon Camara and Landaya</a>, and various other groups.</p>
<p>Dave is the author of the book, <a href="http://djolibacrossing.com" class="external">Djoliba Crossing: Journeys into West African Music and Culture</a>.</p>
</div>
</div>
</section>
</div>
