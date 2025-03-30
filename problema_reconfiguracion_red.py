# -*- coding: utf-8 -*-
"""
Created on Sun Mar 23 09:05:12 2025

@author: 000010478
"""
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import heapq

def fair_spanning_tree_with_fixed_links(G, demand, source, fixed_edges):
    """
    Constructs a fair flow-aware spanning tree including mandatory fixed edges.

    Parameters:
        G: networkx.Graph - Undirected graph
        demand: dict - Node -> demand
        source: node - Root of the flow
        fixed_edges: list of edges that must be included in the final tree

    Returns:
        T: networkx.Graph - Final spanning tree
    """
    T = nx.Graph()
    T.add_nodes_from(G.nodes())
    T.add_edges_from(fixed_edges)

    # Initialize flow from demand
    subtree_flow = {v: demand.get(v, 0) for v in G.nodes()}
    #print('Subtree Flow', subtree_flow)
    # Initial components (due to fixed edges)
    components = list(nx.connected_components(T))
    #print('Componentes: ')
    #for ci in components: 
    #    print(ci)

    for comp in components:
        total_flow = sum(demand.get(v, 0) for v in comp)
        for v in comp:
            subtree_flow[v] = total_flow
    #print('Subtree Flow', subtree_flow)
    iteracion=0
    while not nx.is_connected(T):
        #print('\nIteracion: ',iteracion)
        iteracion+=1
        candidate_edges = []

        for u, v in G.edges():
            if T.has_edge(u, v):
                continue

            # Check if they belong to different components
            for comp_u in components:
                if u in comp_u:
                    break
            for comp_v in components:
                if v in comp_v:
                    break
            #print(u,v,comp_u, comp_v)
            if comp_u != comp_v:
                flow = min(subtree_flow[u], subtree_flow[v])
                heapq.heappush(candidate_edges, (flow, u, v))
        #print('Candidate edges:',candidate_edges)
        while candidate_edges:
            flow, u, v = heapq.heappop(candidate_edges)
            if not T.has_edge(u, v):
                #print('Se agrega el enlace ',u,v,'al arbol')
                T.add_edge(u, v)
                # Update components and flows
                components = list(nx.connected_components(T))
                for comp in components:
                    total_flow = sum(demand.get(node, 0) for node in comp)
                    for node in comp:
                        subtree_flow[node] = total_flow
                #print('Componentes luego de agregar el enlace: ')
                #for ci in components: 
                #    print(ci)

                #print('Subtree Flow luego de agregar el enlace: \n', subtree_flow)
                break

    return T


plt.close('all')
viridis = matplotlib.colormaps['viridis']
#Carga de los datos desde el archivo json
import json
with open('red.json', 'r') as file:
    info = json.load(file)
puntos=info['puntos']
links=info['enlaces']

links=[tuple(sorted([l[0],l[1]])+[l[2]]) for l in links]
links=list(set(links))
#with open('red.json','w') as file: 
#    file.write(json.dumps(info))
    
for i in range(4,len(puntos)):
    x,y,d=puntos[i]
    plt.plot(x,y,'ob', markersize=d)

for i in range(4): 
    x,y,d=puntos[i]
    plt.plot(x,y,'sk', markersize=10)

for i in range(len(puntos)):
    x,y,d=puntos[i]
    plt.text(x,y,str(i))

gates=[]    
for i,j,tipo in links:
    plt.plot([puntos[i][0],puntos[j][0]],[puntos[i][1],puntos[j][1]],'-k')
    if(tipo=='x'):
        gates.append((i,j))
        xc=(puntos[i][0]+puntos[j][0])/2
        yc=(puntos[i][1]+puntos[j][1])/2
        plt.plot(xc,yc,'xr')
plt.axis('equal')        

#Armado de la red
G=nx.Graph()
fijos=[]
demand={}
G.add_node('S', tipo='Source')
demand['S']=0
for i in range(len(puntos)):
    tipo='SE' if i <4 else 'Tr'
    G.add_node(i, tipo=tipo)
    demand[i]=puntos[i][2]
    if(tipo=='SE'):
        G.add_edge('S',i)
        fijos.append(('S',i))
for i,j,tipo in links: 
    G.add_edge(i,j)    
    if(tipo!='x'):
        fijos.append((i,j))

Tree=fair_spanning_tree_with_fixed_links(G, demand, 'S', fijos)

plt.figure()
for i in range(4,len(puntos)):
    x,y,d=puntos[i]
    plt.plot(x,y,'ob', markersize=d)

for i in range(4): 
    x,y,d=puntos[i]
    plt.plot(x,y,'sk', markersize=10)

for i in range(len(puntos)):
    x,y,d=puntos[i]
    plt.text(x,y,str(i))

for i,j in Tree.edges():
    if(str(i)!='S'):
        x1,y1,_=puntos[i]
        x2,y2,_=puntos[j]
        plt.plot([x1,x2],[y1,y2],'-k')
plt.axis('equal')
        