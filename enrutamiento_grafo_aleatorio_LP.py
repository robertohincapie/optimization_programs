import networkx as nx
from pulp import *
import matplotlib.pyplot as plt
plt.close('all')
import numpy as np
from funciones import grafo

n=200
G=nx.DiGraph()
x,y,edges=grafo(L=100, N=n, d=15)
d_org=[np.sqrt((x[i]-100)**2+(y[i]-100)**2) for i in range(n)]
s=np.argmin(d_org)
t=np.argmax(d_org)

nodos={}
dist=[]
for i in range(n):
    nodos['N'+str(i)]=(x[i], y[i])
for i,j in edges:
    dij=np.sqrt((x[i]-x[j])**2+(y[i]-y[j])**2)
    dist.append(('N'+str(i), 'N'+str(j), dij))

for k,pos in nodos.items():
    G.add_node(k, pos=pos)
for a,b,d in dist: 
    G.add_edge(a,b,weight=d)
    G.add_edge(b,a,weight=d)
    
pos=nx.get_node_attributes(G,'pos')
nx.draw(G,pos, with_labels=True, font_size=4)
#nx.draw_networkx_edge_labels(G, pos)

#Creación automática de un problema
prob = LpProblem("Problema_enrutamiento", LpMinimize)
#Crear las variables
x={}
for a,b in G.edges:
    x[a,b] = pulp.LpVariable("x_"+a+'_'+b, 0, 1000)

#Restricciones de cada nodo. 
S='N'+str(s) #Nodo de origen
T='N'+str(t) #Nodo de destino
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
    if(b!=0):
        print(tmp)
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
        
