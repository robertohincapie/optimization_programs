# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 06:33:23 2024

@author: 000010478
"""

import networkx as nx
from pulp import *
import matplotlib.pyplot as plt
G=nx.DiGraph()
nodos={'A':(0,0), 'B':(1,1),'C':(2,1),'D':(2,-1),'E':(3,0),'F':(1,-1)}
dist=[('A','B',2), ('A','F',1), 
      ('B','C',3), ('B','F',1),
      ('C','D',5), ('C','E',2), 
      ('D','E',1), ('D','F',4)]
for k,pos in nodos.items():
    G.add_node(k, pos=pos)
for a,b,d in dist: 
    G.add_edge(a,b,weight=d)
    G.add_edge(b,a,weight=d)
    
pos=nx.get_node_attributes(G,'pos')
nx.draw(G,pos, with_labels=True)
nx.draw_networkx_edge_labels(G, pos)

#Creación automática de un problema
prob = LpProblem("Problema_enrutamiento", LpMinimize)
#Crear las variables
x={}
for a,b in G.edges:
    x[a,b] = pulp.LpVariable("x_"+a+'_'+b, 0, 1000)

#Restricciones de cada nodo. 
S='A' #Nodo de origen
T='E' #Nodo de destino
for ni in G.nodes:
    tmp=0
    for _,n_out in G.out_edges(ni):
        tmp+=x[ni,n_out]
    for n_in,_ in G.in_edges(ni):
        tmp-=x[n_in,ni]
    b=0
    if ni==S:
        b=1
    if ni==T:
        b=-1
    prob += tmp==b, "Flujo en el nodo "+ni

#Función objetivo
tmp=0
for a,b in G.edges:
    w=G.edges[a,b]['weight']
    tmp+=w*x[a,b]
    
prob += tmp, "Función objetivo"

#Solución del problema
prob.solve()
for v in prob.variables():
    if(v.varValue>0):
        print(v.name, "=", v.varValue)
        _,a,b=v.name.split('_')
        x1, y1=G.nodes[a]['pos']
        x2, y2=G.nodes[b]['pos']
        plt.plot([x1,x2],[y1,y2],'-r',linewidth=3)
        
