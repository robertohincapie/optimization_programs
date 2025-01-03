# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 17:10:56 2025

@author: 000010478
"""

import networkx as nx
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

