# -*- coding: utf-8 -*-
"""
Created on Sun Dec 29 19:56:50 2024

@author: 000010478
"""

import networkx as nx
from pulp import *
import matplotlib.pyplot as plt
plt.close('all')
import numpy as np
from generacion_grafos import grafo
n=200
G=nx.Graph()
L=100
d=30
x,y,edges=grafo(L=L, N=n, d=d)
d_org=[np.sqrt((x[i]-100)**2+(y[i]-100)**2) for i in range(n)]
s=np.argmin(d_org)
t=np.argmax(d_org)
nodos={}
dist=[]
demand={}
for i in range(n):
    nodos['N'+str(i)]=(x[i], y[i])
    demand['N'+str(i)]=np.random.randint(low=1, high=5)

for i,j in edges:
    dij=np.sqrt((x[i]-x[j])**2+(y[i]-y[j])**2)
    dist.append(('N'+str(i), 'N'+str(j), dij))

cap=10
for k,pos in nodos.items():
    G.add_node(k, pos=pos)
for a,b,d in dist: 
    G.add_edge(a,b,weight=d, capacity=cap, uso=0)
    #G.add_edge(b,a,weight=d, capacity=cap)

for k,pos in {'G':(0.0,0.0), 'SE1':(-L/2, -L/2), 'SE2':(L/2, -L/2), 
       'SE3':(-L/2, L/2), 'SE4':(L/2, L/2)}.items():
    G.add_node(k, pos=pos)
    for k2,pos2 in nodos.items():
        dist=np.sqrt((pos[0]-pos2[0])**2+(pos[1]-pos2[1])**2)
        if(dist<2*d and k!='G'):
            G.add_edge(k2,k, weight=dist, uso=0)            
G.add_edge('G','SE1',weight=0.001, capacity=100*cap, uso=0)
G.add_edge('G','SE2',weight=0.001, capacity=100*cap, uso=0)
G.add_edge('G','SE3',weight=0.001, capacity=100*cap, uso=0)
G.add_edge('G','SE4',weight=0.001, capacity=100*cap, uso=0)

color_map = []
color_index={}
for node in G:
    color_index[node]=len(color_map)
    if(node[0]=='G'):
        color_map.append('yellow')
    if(node[0]=='S'):
        color_map.append('#aaaaaa')
    if(node[0]=='N'):
        color_map.append('#abe456')
    
tree=nx.minimum_spanning_tree(G)
colores=['#ccd1d1', '#f5cba7', '#a3e4d7', '#d2b4de', '#f5b7b1', '#f7dc6f']

#Capacidad utilizada actual: 
for i in range(n):
    nodo='N'+str(i)
    dem=demand[nodo]
    path=nx.shortest_path(tree, 'G', nodo)
    SE=int(path[1][2])
    color=colores[SE-1]
    for i in range(1,len(path)-1):
        tree.edges[path[i], path[i+1]]['uso']+=dem
        color_map[color_index[path[i+1]]]=color
width = [tree[u][v]['uso'] for u,v in tree.edges]
Wmax=np.max(width)
Wm=10
width=[w*(Wm-1)/Wmax+1 for w in width]

post=nx.get_node_attributes(tree,'pos')
plt.figure()
nx.draw(tree,post, with_labels=True, font_size=8, node_size=200, node_color=color_map, width=width, edgecolors='black', alpha=0.8)
plt.axis('equal')
