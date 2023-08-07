# Triangulation

Why quality?

![quality](../f/f_triang/quality.png "quality")

Quotation from [Deming](https://en.wikipedia.org/wiki/W._Edwards_Deming)

> *Knowledge of variation*: the range and causes of variation in quality, and use of statistical sampling in measurements;
> *Improve constantly* and forever the system of production and service, to improve quality and productivity, and thus constantly decrease costs.
> *Break down barriers* between departments. People in research, design, sales, and production must work as a team, to foresee problems of production and usage that may be encountered with the product or service.
> In god we trust, *everybody else bring data*

## Cell coverage

We take one location
![one_location](../f/f_triang/one_location.png "one location")
_example of a location_

We download the local street network
![network](../f/f_triang/local_network.png "local network")
_local network_

We download the cell coverage in the network area
![cell coverage](../f/f_triang/touching_bse.png "touching bse")
_cell coverage around the location_

We classify the cells by radius and we plot the coverage centroid
![classify_bse](../f/f_triang/classify_bse.png "classify bse")
_display cells by technology wich influences the area_

We select the most precise cells, some of them happen to be subway cells
![precise_bse](../f/f_triang/precise_bse.png "precise bse")
_selection of the techologies with good spatial resolution_

We can simplify the geometries taking only the closest and most precise cells centroids
![neighboring_base](../f/f_triang/neighboring_bse.png "neighboring cells")
_neighboring cells represented by centroid and radius_

and than we try to sum up a portion of activities into some geometries

![cell_geometry](../f/f_triang/cell_geometry.png "cell geometry")
_we map the location into a geometry (mtc, zip5)_

But for some technology we have centroids outside the coverage area

![cell_no_coverage](../f/f_triang/centroid_no_coverage.png "cell no coverage")
_some centroids are not contained in any area_

## Stability comparison

We want to evaluate count stability using the dominant cell method. 

The first test is done moving the center of the overlapping mapping by a displacement (in meters)

![stability_displacement](../f/f_triang/stability_displacement.png "stability displacement")
_stability of counts after displacement_

We than check the stability of counts by area 

![stability_area](../f/f_triang/stability_area.png "stability area")
_stability of counts after area increase (edge in meters)_

Number of counts strongly increase with mapping area (until 50%).



## definition

An _activity_ is made of many _events_. Currently we define the _dominant cell_ as the cell where most of the events took place. 
For every cell we assign a position which is the centroid of the _BSE_ (Best Server Estimation), an estimation of the area where the cell has the best ground coverage without intersection of other cells with the same technology.
Hence, each activity position is located at the centroid of each dominant cell.
![poly_cilac](../f/f_triang/poly_cilac.png "f_triang/poly_cilac")
_The polygon shows the location we want to isolate, the arrows the neighbouring cell centroids_

The density profile of the activities is then centered around the centroid position.
![dens_cilac](../f/f_triang/dens_cilac.png "f_triang/dens_cilac")

We can divide the space where each cell centroid sits at the vertex of a Delaunay triangle.
![poly_delaunay](../f/f_triang/poly_delaunay.png "f_triang/poly_delaunay")
_Delaunay triangulation on cell centroids_

### Triangulation

If we average over all vertex positions we have a more sparse activity distribution. We can even define a standard error for each activity [filter_activities.py](). 
$$ s_x = \sqrt{\frac{ \sum_i (\hat x - x_i)^2 }{N-2}} \qquad s_r = \sqrt{s_x^2 + s_y^2} $$
The standard error define the uncertanty on the activity position.

![activity_triang](../f/f_triang/activity_triang.png "f_triang/activity_triang")
_The dots represent the average activity position, the dot size represent the standard error of the position_

Which translate in a broader density profile.
![density_trian](../f/f_triang/density_triang.png "f_triang/density_trian")
_Density profile of triangulated activities, density spreads over the space_

For each polygon we take the distribution of standard error of the positions inside the polygon.
![error_dist](../f/f_triang/error_dist.png "f_triang/error_dist")
_distribution of the standard errors all over the activities_

The median of the standard error distribution defines a buffer radius
![poly_buffer](../f/f_triang/poly_buffer.png "f_triang/poly_buffer")
_The buffer radius (in green) circulates around the polygon defining the precision of activity positions per location_

### Octree binning
To overcome anonymization problems we transform coordinates in [geohash](https://github.com/hkwi/python-geohash).

Geohash is a indexed short string which contains information about the position and the bounding box of a square. The number of digits sets the precision (i.e. the size of the bounding box) using a [octree](https://en.wikipedia.org/wiki/Octree). Neighbouring boxes have similar indices. 

![octree](../f/f_triang/octree.svg "octree 2d")
_2d representation of an octree_

![octree](../f/f_triang/octree.png "octree 3d")
_3d usage of an octree_


To anonymize the data we loop until we find the minimum number of digits for each geohash string: [fenics_finite.py](). 
```python
vact.loc[:,"geohash"] = vact[['x_n','y_n']].apply(lambda x: geohash.encode(x[0],x[1],precision=8),axis=1)
def clampF(x):
    return pd.Series({"n":sum(x['n']),"sr":np.mean(x['sr'])})
lact = vact.groupby('geohash').apply(clampF).reset_index()
for i in range(3):
    setL = lact['n'] < 30.
    lact.loc[:,"geohash2"] = lact['geohash']
    lact.loc[setL,"geohash"] = lact.loc[setL,'geohash2'].apply(lambda x: x[:(8-i-1)])
    lact = lact.groupby('geohash').apply(clampF).reset_index()
```
At the end we produce a table similar to this one:

| geohash | count | deviation |
|-------|----|---------| 
|    t1hqt|   34|  0.1|
|   t1hqt3|   42|  0.4|
| t1hqt3zm|   84|  0.8|
|   t1hqt6|   44|  0.6|
|   t1hqt8|   78|  0.8|
|   t1hqt9|  125|  0.6|
|  t1hqt96|   73|  0.3|
|  t1hqt97|   38|  0.5|
|  t1hqt99|   46|  0.4|

In post processing we can then reconstruct the geometry:
![geohash binning](../f/f_triang/geohash_binning.png "geohash binning")
_Overcome the anonimization problem using geohash binning_

This allows us to have the larger precision allowded without count loss.

For each box we can estimate the precision
![geohash buffer](../f/f_triang/geohash_buffer.png "geohash buffer")
_Overcome the anonimization problem using geohash binning_

Alternatively we can apply a double binary octree
![octree binning](../f/f_triang/octree_binning.png "octree binning")
_counts on a octree binning_

Advantages
* no mapping
* no BSE
* no data loss
* custom geometries (postprocessing - no deploy)
* no double counting
* highest allowed resolution

Cons
* no unique counts per polygon
* postprocessing always required
* land use mapping might have more accuracy

![mapping generation](../f/f_triang/mapping_generation.svg "mapping generations")
_evolution of mappings_

Which was calculated by a simple halfing of each edge:
```python
   BBox = [5.866,47.2704,15.0377,55.0574]
    spaceId = ''
    for i in range(precision):
        marginW = marginH = 0b00
        dH = (BBox[3] - BBox[1])*.5
        dW = (BBox[2] - BBox[0])*.5
        if x < (BBox[0] + dW):
            BBox[2] = BBox[2] - dW
        else:
            marginW = 0b01
            BBox[0] = BBox[0] + dW
        if y < (BBox[1] + dH):
            BBox[3] = BBox[3] - dH
        else:
            marginH = 0b10
            BBox[1] = BBox[1] + dH
        spaceId = spaceId + str(marginW + marginH)
```

In post processing we can reconstruct the geometry and interpolate the missing boxes.

### Space deformation

The spatial resolution is given by the distribution of cells which modifies the definition of space around. We represent each cell centroid as a trapezoid whose center corresponds to the cell centroid and the area to a portion of the BSE area [fenics_finite.py](). 
We define an [Helfrich Hamiltonian](http://dauvi.org/Fiziko/Report.pdf) on a manifold: $z = z(x,y)$ to define the curvature of space caused by the cell position:
$$ F(z) = \frac{1}{2} \int d x d y (k_{ben}(\nabla^2 z)^2 + k_{stif} (\nabla z)^2 ) $$
Where the bending and stiffness parameters are controlled by the parameters $k_{ben}$ and $k_{stif}$. 

To solve the equation we chose a square mesh and we apply [finite differences](http://dauvi.org/Fiziko/Report.pdf#equation.8.4.4) method on the lattice representing the space.
The solution of the equation is done numerically applying a [Jacobi iteration](http://dauvi.org/doc_allink/classForces.html#abcac13d7754b73f6f22b2900a0d46d7d) on a 5x5 square matrix to convolve with the square lattice representing the space. $k_{ben}$ and $k_{stif}$ represent the [weights for the Laplacian](http://dauvi.org/doc_allink/ForcesIntegration_8cpp_source.html) $\Delta$ and the square Laplacian term $\Delta^2$.

![addyn_sol](../f/f_triang/addyn_sol.png "f_triang/addyn_sol")
_Solution of the Helfrich Hamiltonian on a square lattice, the cylinders represent the cell centroids_
The boundary conditions and the constraints are given by the red and blue beads which are not moved during the iterations.
We can increase the resolution interpolating the lattice points.

![addyn_surf](../f/f_triang/addyn_surf.png "f_triang/addyn_surf")
_discretization of the lattice solution_

To normalize the effect of the space curvature on the activity positions we move each activity by the gradient of the space deformation
$$ \nabla z = \frac{\partial z}{\partial x}  \hat x+ \frac{\partial z}{\partial y} \hat y $$

![space gradient](../f/f_triang/space_gradient.png "gradient of the space deformation")
_gradient of the space deformation on the x and y directions_

If we invert the gradiant we obtain the displacement induced by the cell geography
![cell deformation](../f/f_triang/cell_deformation.png "cell deformation")
_vector field of the displacement and centroids_

We can see how the single activities have moved.
![activity shift](../f/f_triang/activity_shift.png "shift of activities")
_shift of activities, purple to blue_

We then recalculate the density plot based on the new positions.

![density gradient](../f/f_triang/density_respace.png "density plot after displacement")
_density plot after displacement_

We move the single activities according to the gradient.
![activity respace](../f/f_triang/poly_shift.png "activities after displacement")
_new activity position after displacement_

On top of the cell space distortion we apply the underlying network
![network neighbor](../f/f_triang/network_neighbor.png "network neighbor")
_underlying netwok, each street class has a different color_

We discretize the network, apply a width depending on the street speed and apply a smooting filter.
![network sample](../f/f_triang/network_sample.png "network sample")
_smoothed filter on network_

Similarly we can create a displacement map based on the street network.
![network quiver](../f/f_triang/network_shift.png "network quiver")
_displacement due to the street network_


To summarise the whole scheme of the procedure is described in this scheme:
![density flux](../f/f_triang/dens_flux.png "density plot after each operation")
_density plot after each operation and overview on the procedure_

The procedure show how to create a more realistic density plots. Further tuning is necessary.

Finally we update the mapping  [etl_roda.py](). 


