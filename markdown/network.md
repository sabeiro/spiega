# Network
### Library
```python
import osmnx as ox
import networkx as nx
```
Graph:
```python
graph1 = ox.load_graphml(filename="germany_split_motorway_motorwaylink.graphml")
graph2 = ox.load_graphml( filename="germany_split_trunk_trunk_link.graphml")
graph3 = ox.load_graphml( filename="germany_split_primlink.graphml")
graph4 = ox.load_graphml( filename="germany_split_prim.graphml")
graph5 = ox.load_graphml( filename="germany_split_seclink.graphml")
```
Compose:
```python
c_graphs = [graph1, graph2, graph3, graph4, graph5]
composed_G = nx.compose_all(c_graphs)
```
Simplify:
```python
simp_G = ox.simplify_graph(composed_G)
connected_G = max(nx.strongly_connected_component_subgraphs(simp_G), key=len)
graph_proj = ox.project_graph(connected_G)
ox.save_graphml(graph_proj, filename="allGermany_allstreetsUntilSec_proj.graphml")
```
### Create network
```python
import networkx as nx
G=nx.Graph()
G.add_node(1)
G.add_nodes_from([2,3])
H=nx.path_graph(10)
G.add_nodes_from(H)
G.add_node(H)
G.add_edge(1,2)
e=(2,3)
G.add_edge(*e)
G.add_edges_from([(1,2),(1,3)])
G.add_edges_from(H.edges())
G.remove_node(H)
G.clear()
G.add_edges_from([(1,2),(1,3)])
G.add_node(1)
G.add_edge(1,2)
G.add_node("spam")
G.add_nodes_from("spam")
G.number_o../f/f_nodes()
G.number_o../f/f_edges()
G.nodes()
G.edges()
G.neighbors(1)
G.remove_nodes_from("spam")
G.nodes()
G.remove_edge(1,3)
H=nx.DiGraph(G)
H.edges()
edgelist=[(0,1),(1,2),(2,3)]
H=nx.Graph(edgelist)
G.add_edge(1,3)
G[1][3]['color']='blue'
FG=nx.Graph()
FG.add_weighted_edges_from([(1,2,0.125),(1,3,0.75),(2,4,1.2),(3,4,0.375)])
for n,nbrs in FG.adjacency_iter():
    for nbr,eattr in nbrs.items():
        data=eattr['weight']
        if data<0.5: print('(%d, %d, %.3f)' % (n,nbr,data))

for (u,v,d) in FG.edges(data='weight'):    
    if d<0.5: print('(%d, %d, %.3f)'%(n,nbr,d))

G = nx.Graph(day="Friday")
G.graph
G.graph['day']='Monday'
G.graph
import matplotlib.pyplot as plt
nx.draw(G)
nx.draw_random(G)
nx.draw_circular(G)
nx.draw_spectral(G)
plt.show()
```
