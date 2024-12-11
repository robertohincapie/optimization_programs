# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx

def grafo(L,N,d):
    
    x=np.random.uniform(low=-L, high=L, size=N)
    y=np.random.uniform(low=-L, high=L, size=N)
    links=[]
    for i in range(N-1):
        for j in range(i+1,N):
            di=np.sqrt((x[i]-x[j])**2+(y[i]-y[j])**2)
            if(di<=d):
                links.append((i,j))
    
    G=nx.Graph()
    for i in range(N):
        G.add_node(i)
    for a,b in links:
        G.add_edge(a,b)
    
    cond=True
    while(cond):
        cond=False
        graphs = list(nx.connected_components(G))
        #print('Número de subgrafos:', len(graphs))
        if(len(graphs)>1):
            cond=True
            #Buscamos de cada subgrafo con los otros el nodo mas cercano a otro
            dmin=1e10
            for i in range(len(graphs)-1): #Grafo 1
                for j in range(i+1, len(graphs)): #Grafo 2
                    #print('Revisión de los grafos ',i,',',j)
                    for n1 in graphs[i]:
                        for n2 in graphs[j]:
                            d=np.sqrt((x[n1]-x[n2])**2+(y[n1]-y[n2])**2)
                            if(d<dmin):
                                dmin=d
                                ref=(n1, n2, d)
                                #plt.plot(x[n1],y[n1], 'sk')
                                #plt.plot(x[n2],y[n2], 'sk')
    
                                #print(ref)
            n1,n2,d=ref
            G.add_edge(n1,n2)
            links.append((n1,n2))
        #plt.figure()
        #n1, n2, d=ref
        #plt.plot(x[n1],y[n1], 'sb')
        #plt.plot(x[n2],y[n2], 'sb')
        
    #for a,b in links:
    #    plt.plot([x[a], x[b]], [y[a], y[b]],'-b')
    #plt.axis('equal')
    return x,y,links           