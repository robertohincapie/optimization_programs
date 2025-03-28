# -*- coding: utf-8 -*-
"""
Created on Sun Mar 23 09:05:12 2025

@author: 000010478
"""
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
plt.close('all')
viridis = matplotlib.colormaps['viridis']
#Carga de los datos desde el archivo json
import json
with open('red.json', 'r') as file:
    info = json.load(file)
puntos=info['puntos']
links=info['enlaces']

with open('red.json','w') as file: 
    file.write(json.dumps(info))
    
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

#Análisis de los grupos de nodos
G=nx.Graph()
for i in range(len(puntos)):
    tipo='SE' if i <4 else 'Tr'
    G.add_node(i, tipo=tipo)
    for i,j,tipo in links: 
        if(tipo!='x'):
            G.add_edge(i,j)    

comps=list(nx.connected_components(G))
n=len(comps)
grupos={}
for i,ci in enumerate(comps):
    c=viridis(i/n)
    demanda=0
    pos=np.array([0,0])
    for ni in ci:
        demanda+=puntos[ni][2]
        pos=pos+np.array([puntos[ni][0], puntos[ni][1]])
        plt.plot(puntos[ni][0], puntos[ni][1], 'o', color=c, markersize=puntos[ni][2])
    grupos[i]={'nodos':ci, 'demanda':demanda, 'pos':pos/len(ci), 'color':c}
pasos=[]
for i,j in gates:
    for k,v in grupos.items(): 
        if(i in v['nodos']):
            a=k
        if(j in v['nodos']):
            b=k
    pasos.append((a,b))
    
plt.figure()
for k,v in grupos.items():
    if(v['demanda']>0):
        plt.plot(v['pos'][0],v['pos'][1], 'o', color=v['color'], markersize=v['demanda']/3)
    else:
        plt.plot(v['pos'][0],v['pos'][1], 'sk', markersize=20)
for a,b in pasos: 
    plt.plot([grupos[a]['pos'][0], grupos[b]['pos'][0]], 
             [grupos[a]['pos'][1], grupos[b]['pos'][1]], '-k')
plt.axis('equal')
        
        
        