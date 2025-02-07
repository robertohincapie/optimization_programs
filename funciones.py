# -*- coding: utf-8 -*-

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
                links.append((j,i))
    
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

def crearG(x,y,links, directed=True):
    if(directed):
        G=nx.DiGraph()
    else:
        G=nx.Graph()
    for i in range(len(x)):
        G.add_node(i, x=x[i], y=y[i])
    for a,b in links: 
        d=np.sqrt((x[a]-x[b])**2+(y[a]-y[b])**2)
        G.add_edge(a,b,weight=d)
    return G

def guardarRed(G, file):
    with open(file,'w') as f:
        if(type(G)==nx.Graph):
            f.write('Graph\n')
        else:
            f.write('DiGraph\n')
        for ni in G.nodes:
            f.write('Node:'+ni+'->'+str(G.nodes[ni])+'\n')
        for a,b in G.edges:
            f.write('Edge:'+a+','+b+'->'+str(G.edges[a,b])+'\n')
            
def leerRed(file): 
    #Node:N12->{'pos': (87.9173728798823, 93.96499245301027), 'demanda': 3}
    #Edge:G,SE1->{'weight': 0.001, 'capacity': 50000, 'uso': 77}
    with open(file, 'r') as f:
        lines=f.read().split('\n')
    if(lines[0]=='Graph'):
        G=nx.Graph()
    else:
        G=nx.DiGraph()
    for i in range(1,len(lines)):
        tipo,info=lines[i][0:4], lines[i][5:]
        print(tipo, info)
        if(tipo=='Node'): #Se agrega un nodo
            info=info.replace('array([','(')
            info=info.replace('])',')')
            
            name, data=info.split('->')
            G.add_node(str(name), **eval(data))
        if(tipo=='Edge'): #Se agrega un nodo
            name, data=info.split('->')
            a,b=name.split(',')
            G.add_edge(str(a),str(b), **eval(data))
            
    return G

def dibujarRed(G):
    pos={k:np.array([G.nodes[k]['x'], G.nodes[k]['y']]) for k in G.nodes}
    nx.draw(G, pos=pos)
    nx.draw_networkx_labels(G, pos=pos)
    plt.axis('equal')
    