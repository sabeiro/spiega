# C++

The complete project documentation under [oxygen](doc_allink/) and [repo](https://github.com/sabeiro/Allink/)

## math libraries

The main math class is [Matematica.h](https://github.com/sabeiro/Allink/blob/master/include/Matematica.h) which includes 

* 2d matrix filtering
* algebric operations
* numeric integration/derivation
* approximated basic functions (Gamma, Bessel, Neumann)
* spectral analysis
* correlation, normalization
* statistical properties, momenta
* interpolation, regression, filtering
* Bezier, splines


## sputtering [2006-2008]

Sputtering of ions on silicon lattice to calculate impurity diffusion

![solid state](../f/f_theo/solid_state.svg "solid state")
_sputtering on ions_

## monte carlo [2006-2013]

Monte Carlo simulations to simulate grand canonical equilibrium of lipid chains around a nanoparticle

![monte_carlo](../f/f_theo/PeptideCover.png "peptide")
_peptide in lipid membrane_

## molecular dynamics [2008-2013]

![openGl](../f/f_theo/NpHole.png "nanoparticle")
_coated nanoparticle_

## visualization with Qt [2006-2013]

The program [Avvis](https://github.com/sabeiro/Allink/tree/master/src/Avvis) was written over 6 years in C++ and Qt (migrated from 4 to 5 to 6)

![avvis](../porfolio/f/avvis_func.png "avvis functions")
_overview of some key features of the program Avvis_

The program was initially used in 2005 to compute basic properties of signals in the search of pink noise and extended until 2012 to basically compute signal processing and plotting.

Features:

* display signals and select specific ranges
* display log, points, lines
* compute spectrum, autocorrelation, running average, integral, derivative
* interpolate on selected ranges, log included
* plot and load style configurations

```c++
void ElementiGrafici::DisegnaPunti(QPainter *p){
  if(PrimaVolta){
    return;
  }
  if(NVisMin < 0 || NVisMax > PuntiMax || NVisMin > NVisMax){
    sprintf(stringa,"Non `e corretto l'ordine 0<=%d<%d<=%d",NVisMin,NVisMax,PuntiMax);
    printf("Non `e corretto l'ordine 0<=%d<%d<=%d\n",NVisMin,NVisMax,PuntiMax);
    ErrPrima->message(stringa);
    return;
  }
  if( IfRiscala != 0 ) GrRiscala();
  GrStampante(p);
  GrConf(nomeConf);
  GrScript(nomeConf,p);
  if( DIS_IF_TYPE(IfDisegna,DIS_TUTTI) ){
    for(int s=0,sColor=0;s<NVar;s++){
      if(v1->IsAbscissa(s)) continue;
      sColor = s;
      p->setBrush( GrLinee[sColor] );
      p->setPen( QPen( GrLinee[sColor],2 ) );
      Quadrati = DIS_IF_TYPE(LineaCome[sColor],LINEA_PUNTO);
      Linee = DIS_IF_TYPE(LineaCome[sColor],LINEA_TRATTO);
      GrSet(p,s);
      sColor++;
    }
  }
```


## visualization with openGL [2006-2013]

The main software is called ElPly and is written to display simuation results:

![openGl](../f/f_theo/ElPoly.png "opengl")
_openGL software_

Main features

* display chains and molecules
* display surfaces (marching cubes)
* navigate
* menu display
* conf file input


![openGl](../f/f_theo/NpDensPhob3d.png "opengl")
_density of lipids around a nanoparticle_


![openGl](../f/f_theo/PlanarLBetaNIntPair2.png "opengl")
_planar membranes_

![openGl](../f/f_theo/Pot3dTiltSmoothed.png "peptide")
_peptide in membrane_


# Gtk

The python 2 code [caciotta leaks](https://github.com/sabeiro/malastro/blob/master/theo/python/CaciottaLeaks.py) was written to create an interface between the erp database and the user.

![caciotta leaks](../f/f_dauvi/caciotta_leaks.png "caciotta leaks")
_Caciotta leaks, database interface to compute milk efficiency in a cheese factory_


```python
import pygtk
import gtk, pango
window = None
flag_checkboxes = 5*[None]
settings = 5*[0]
self.marked_date = 31*[0]

window = gtk.Window(gtk.WINDOW_TOPLEVEL)
window.set_title("CaciottaLeaks")
window.set_border_width(5)
window.connect("destroy", lambda x: gtk.main_quit())

window.set_resizable(False)

vbox = gtk.VBox(False, self.DEF_PAD)
window.add(vbox)
...
```


## finite differences [2010-2013]

A cpp code to compute finite differences up to 4th order

![continuum](../f/f_theo/PepCoreContinuum.png "")
_finite element software_
