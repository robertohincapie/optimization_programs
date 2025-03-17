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
from funciones import grafo
from funciones import guardarRed

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

cap=50
for k,pos in nodos.items():
    G.add_node(k, pos=pos, demanda=demand[k])
for a,b,d in dist: 
    G.add_edge(a,b,weight=d, capacity=cap, uso=0)
    #G.add_edge(b,a,weight=d, capacity=cap)

transmision={'G':(0.0,0.0)}
pos=[(-L/2, -L/2), (L/2, -L/2), (-L/2, L/2), (L/2, L/2)]
Nse=3
for i in range(Nse): #Número de subestaciones
   transmision['SE'+str(i+1)]=np.array(pos[i])+np.random.randn(2)*L/4
   
for k,pos in transmision.items():
    G.add_node(k, pos=pos, demanda=0)
    for k2,pos2 in nodos.items():
        dist=np.sqrt((pos[0]-pos2[0])**2+(pos[1]-pos2[1])**2)
        if(dist<2000*d and k!='G'):
            G.add_edge(k2,k, weight=dist, uso=0, capacity=cap)            
for i in range(Nse):
    G.add_edge('G','SE'+str(i+1),weight=0.001, capacity=1000*cap, uso=0)


def esau_williams(G):
    Tree=nx.Graph()
    Tree.add_node('G', pos=G.nodes['G']['pos'], demanda=0)
    for ni in G.nodes: 
        if(ni[0]=='S'):
            Tree.add_node(ni, pos=G.nodes[ni]['pos'], demanda=0)
            Tree.add_edge(ni, 'G', weight=G.edges[ni,'G']['weight'], 
                          capacity=G.edges[ni,'G']['capacity'], uso=0)
    #Listas de las subestaciones, generador y nodos del grafo original
    SE=[node for node in Tree.nodes if node[0]=='S']
    Gen=['G']
    nodos=[node for node in G.nodes if node[0]=='N']
    g={}
    for ni in nodos: 
        dmin=1e10
        for se in SE: 
            d=np.linalg.norm(np.array(G.nodes[ni]['pos'])-np.array(G.nodes[se]['pos']))
            if(d<dmin):
                dmin=d
                g[ni]=(se,d)
    #print(g)
    #Inicializados los enlaces Gates, es necesario construir los ramales del modelo. 
    #Hay una estructura árbol, que es necesario alimentar. 
    #La iteración termina cuando los gates están terminados. 
    cont=500
    no_conectados=[]
    while(len(g)>0 and cont>0):
        cont-=1
        #Se debe calcular el nodo más cercano a alguno de los nodos disponibles. 
        dmin=1e10
        for ni,dist in g.items(): #Nodos actualmente como gates
            #print('\nGate analizado: ',ni, dist)
            for n2 in G.neighbors(ni): #Vecinos del nodo. 
                #print('Vecino analizado: ',n2)
                if(n2 in Tree.nodes):
                    if(G.edges[ni, n2]['weight']<dmin):
                        dmin=G.edges[ni, n2]['weight']
                        candidate=(ni,n2)
        print('\nCandidato: ',dmin, candidate)
        #Revisando la ruta y la capacidad
        if(dmin<1e8): #Ya no hay enlace posible por capacidad. 
            path=nx.shortest_path(Tree, candidate[1], 'G')
            posible=True
            for i in range(len(path)-1):
                if(Tree.edges[path[i], path[i+1]]['uso']+G.nodes[candidate[0]]['demanda']>Tree.edges[path[i], path[i+1]]['capacity']):
                    posible=False
            if(posible): #Se puede conectar al nodo candidato. 
                n_in=candidate[0]
                dst=candidate[1]
                Tree.add_node(n_in, pos=G.nodes[n_in]['pos'], demanda=G.nodes[n_in]['demanda'])
                Tree.add_edge(n_in, dst,  weight=G.edges[n_in, dst]['weight'], 
                              capacity=G.edges[n_in, dst]['capacity'], uso=0)
                path=nx.shortest_path(Tree, n_in, 'G')
                for i in range(len(path)-1):
                    Tree.edges[path[i], path[i+1]]['uso']+=G.nodes[candidate[0]]['demanda']
                del g[n_in]
                print('Se agregó al árbol')
            else: 
                print('Por capacidad no se agregó al árbol')
                G.remove_edge(candidate[0],candidate[1])
        else: 
            print(g)
            if(candidate[0] in g.keys()):
                del g[candidate[0]]
            print('Se remueve el nodo ',candidate[0], 'pues no tuvo conexión')
            n_in=candidate[0]
            no_conectados.append({'k':n_in, 'pos':G.nodes[n_in]['pos'], 'demanda':G.nodes[n_in]['demanda']})
    for dic in no_conectados: 
        Tree.add_node(dic['k'], pos=G.nodes[n_in]['pos'], demanda=G.nodes[n_in]['demanda'])
    return Tree
tree=nx.minimum_spanning_tree(G)
colores=['#ccd1d1', '#f5cba7', '#a3e4d7', '#d2b4de', '#f5b7b1', '#f7dc6f']

#Capacidad utilizada actual: 
color_map = []
for ni in tree.nodes:
    if(ni[0]=='G'):
        color_map.append('yellow')
    if(ni[0]=='S'):
        color_map.append('yellow')
    if(ni[0]=='N'):
        nodo=ni
        dem=demand[nodo]
        path=nx.shortest_path(tree, 'G', nodo)
        SE=int(path[1][2])
        color=colores[SE-1]
        for i in range(1,len(path)-1):
            tree.edges[path[i], path[i+1]]['uso']+=dem
        color_map.append(color)

width = [tree[u][v]['uso'] for u,v in tree.edges]
Wmax=np.max(width)
Wm=10
width=[w*(Wm-1)/Wmax+1 for w in width]

#post=nx.get_node_attributes(tree,'pos')
#plt.figure()
#nx.draw(tree,post, with_labels=True, font_size=8, node_size=200, node_color=color_map, width=width, edgecolors='black', alpha=0.8)
#plt.axis('equal')


Tree=esau_williams(G)
post=nx.get_node_attributes(Tree,'pos')

width = [Tree[u][v]['uso'] for u,v in Tree.edges]
Wmax=np.max(width)
Wm=10
width=[w*(Wm-1)/Wmax+1 for w in width]

color_map=[]
for ni in Tree.nodes:
    if(ni[0]=='G'):
        color_map.append('yellow')
    if(ni[0]=='S'):
        color_map.append('yellow')
    if(ni[0]=='N'):
        path=nx.shortest_path(Tree, 'G', ni)
        SE=int(path[1][2])
        color=colores[SE-1]
        color_map.append(color)

plt.figure()
nx.draw(Tree,post, with_labels=True, font_size=8, node_size=200, node_color=color_map,  width=width, edgecolors='black', alpha=0.8)
edgeLbl={(u,v):Tree.edges[u,v]['uso'] for u,v in Tree.edges}
nx.draw_networkx_edge_labels(Tree, post, edgeLbl, font_size=6)

plt.axis('equal')
guardarRed(Tree, 'RedDistribucion.nx')