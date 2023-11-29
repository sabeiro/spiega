# javascript

# d3

Some d3.js examples are published on [anticolo](https://intertino.it/anticolo)

![d3](../portfolio/f/d3viz.png "d3 overview")
_d3 overview_

Example of [network](https://intertino.it/anticolo/network.php)

![network](../f/f_stage/viz_network.png "network")
_network_

Example of [heatmap](https://intertino.it/anticolo/heatmap.php)

![heatmap](../f/f_stage/viz_heatmap.png "heatmap")
_heatmap_

Example of [sunburst](https://intertino.it/anticolo/sunburst.php)

![sunburst](../f/f_stage/viz_sunburst.png "sunburst")
_sunburst_ 

Example of [circle packt](https://intertino.it/anticolo/circle_pack.php)

![circle pack](../f/f_stage/viz_circlePack.png "circlePack")
_circlePack_ 

Example of [treebox](https://intertino.it/anticolo/treebox.php)

![treebox](../f/f_stage/viz_treebox.png "treebox")
_treebox_ 

![taxonomy](../portfolio/f/taxonomy.png "taxonomy")
_taxonomy_

# R 

![demographics](../portfolio/f/socio_demo.png "socio demo")
_socio demo_

![time series](../portfolio/f/time_series.png "time series")
_time series_

![geo](../portfolio/f/geo.png "geo")
_geo_

![affinity](../portfolio/f/affinity.png "affinity")
_affinity_

![customer_feedback](../portfolio/f/customer_feedback.png "customer_feedback")
_customer feedback_

# openlayer

Openlayers is a really handy map library that supports many the display of different geometrical layers on top of raster or vector maps.

![open layers](../f/f_ride/openlayes.png "openlayers")
_openlayers_



Maps: 

```javascript
//------------------------------initialize-map--------------------------------
// var raster = new ol.layer.Tile({title:"tile",source: new ol.source.Stamen({layer: 'watercolor'})});
var raster = new ol.layer.Tile({title:"tile",source: new ol.source.StadiaMaps({layer: 'stamen_watercolor'})});
raster.setOpacity(0.2);
// var map_label = new ol.layer.Tile({title:"street",visible:false,source: new ol.source.Stamen({layer: 'terrain-labels'})});
var map_label = new ol.layer.Tile({title:"street",visible:false,source: new ol.source.StadiaMaps({layer: 'stamen_terrain_labels'})});
var osmLayer = new ol.layer.Tile({source: new ol.source.OSM()});
var map = new ol.Map({
  layers: [new ol.layer.Group({title:"raster",visible:true,layers:[raster,map_label]})],
  overlays: [overlay],
  target: 'map',
  view: new ol.View({center: ol.proj.fromLonLat([13.435755,52.507976]),zoom: 12})
});

```

layers:

```javascript
function initLayers(spotL){
  var currZoom = map.getView().getZoom();
  line_feature = plotLines(spotL,currZoom);
  line_source = new ol.source.Vector({features:line_feature});
  line_layer = new ol.layer.Vector({title:"lines",source:line_source});
  map.addLayer(line_layer);

  point_feature = plotPoint(spotL,currZoom);
  point_source = new ol.source.Vector({features: point_feature,minResolution:2500});
  point_layer = new ol.layer.Vector({title:"stops",source:point_source});
  map.addLayer(point_layer);
  
  poly_feature = plotPoly(spotL,currZoom);
  poly_source = new ol.source.Vector({features: poly_feature});
  poly_layer = new ol.layer.Vector({title:"poly",source:poly_source});
  map.addLayer(poly_layer)
}
```

styles:

```javascript
//-----------------------projection------------------------------

var current_projection = new ol.proj.Projection({code: "EPSG:4326"});
// var new_projection = raster.getSource().getProjection();
var new_projection = new ol.proj.Projection({code: "EPSG:3857"});
function transform_geometry(element) {
  element.getGeometry().transform(current_projection, new_projection);
}

//---------------------graph-objects------------------------------

function plotLines(spotL,currZoom){
  var n_agent = Object.keys(pathL).length;
  for(var loc in spotL){n_agent = Math.max(n_agent,spotL[loc]['agent']);}
  var line_feature = [];
  var posV = {};
  for(var a=0;a<=n_agent;a++){
	posV[a] = {};
	posV[a]['color'] = colorL[a];
	posV[a]['path'] = [];
  }
  for(var loc in spotL){
	var agent = spotL[loc]['agent']
	if(agent <= 0){continue;}
	var coordinates = [spotL[loc]['x'],spotL[loc]['y']];
	posV[agent]['path'].push(coordinates);
  }
  for(var p in posV){
	var pointL = posV[p]['path'];
	var color = posV[p]['color'];
	var line = new ol.Feature({geometry: new ol.geom.LineString(pointL)});
	var fill = new ol.style.Fill({color:color});
	var stroke = new ol.style.Stroke({color:color,width:2});
	var style = new ol.style.Style({fill: fill,stroke: stroke});
	line.setStyle(style)
	line_feature.push(line)
  }
  line_feature.forEach(transform_geometry);
  return line_feature;
};

function plotPoint(spotL,currZoom){
  var features = new Array();
  for (var key in spotL){
	var agent = spotL[key]['agent'];
	agent = parseInt(agent);
	spotL[key]['agent'] = agent;
	spotL[key]['color'] = colorL[agent];
	var textS = spotL[key]['agent'].toString();
	var coordinates = [spotL[key]['x'],spotL[key]['y']];
	var feat = new ol.Feature(new ol.geom.Point(coordinates));
	var fill = new ol.style.Fill({color: spotL[key]['color']});
	var stroke = new ol.style.Stroke({color: spotL[key]['color'],width:1});
	var style = new ol.style.Style({
	  image: new ol.style.Circle({fill: fill,sstroke: stroke, radius:10})
	  ,fill: fill,stroke: stroke
	  ,text: new ol.style.Text({
	    text: textS,fill: new ol.style.Fill({color: '#fff'})
	  })
	});
	if (currZoom > 12){
	  style = new ol.style.Style({
		image: new ol.style.Circle({fill: fill,sstroke: stroke, radius:5})
		,fill: fill,stroke: stroke
	  });
	}
	feat['color'] = spotL[key]['color'];
	feat['id'] = key;
	feat['agent'] = spotL[key]['agent'];
	feat.setStyle(style);
	features.push(feat);
  }
  features.forEach(transform_geometry);
  return features;
}

function plotPoly(spotL,currZoom){
  var poly = new ol.geom.Polygon( [[[13.4357548 , 52.50797622],[13.43204609, 52.50202178],[13.43254786, 52.50549124],[13.43059576, 52.51060367],[13.43361524, 52.50990525]]])
  var poly_feature = new ol.Feature({name:"poly",geometry:poly})
  return [poly_feature];
};



```
