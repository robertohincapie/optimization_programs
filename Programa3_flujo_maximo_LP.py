import networkx as nx
from pulp import *
import matplotlib.pyplot as plt
plt.close('all')
import numpy as np
n=200
G=nx.DiGraph()
x=np.random.uniform(low=-100,high=100,size=n)
y=np.random.uniform(low=-100,high=100,size=n)
d_org=[np.sqrt((x[i]-100)**2+(y[i]-100)**2) for i in range(n)]
s=np.argmin(d_org)
t=np.argmax(d_org)

d=35
cap=2
nodos={}
dist=[]
for i in range(n):
    nodos['N'+str(i)]=(x[i], y[i])
for i in range(n-1):
    for j in range(i+1, n):
        dij=np.sqrt((x[i]-x[j])**2+(y[i]-y[j])**2)
        if(dij<=d):
            dist.append(('N'+str(i), 'N'+str(j), dij))

for k,pos in nodos.items():
    G.add_node(k, pos=pos)
for a,b,d in dist: 
    G.add_edge(a,b,weight=d, capacity=cap)
    G.add_edge(b,a,weight=d, capacity=cap)
    
pos=nx.get_node_attributes(G,'pos')
nx.draw(G,pos, with_labels=True, font_size=4)
#nx.draw_networkx_edge_labels(G, pos)

#Creación automática de un problema
prob = LpProblem("Problema_flujo_maximo", LpMaximize)
#Crear las variables
x={}
for a,b in G.edges:
    cap=G.edges[a,b]['capacity']
    x[a,b] = pulp.LpVariable("x_"+a+'_'+b, 0, cap)
a = pulp.LpVariable("Flujo", 0, 1000)

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
        tmp-=a
    if ni==T:
        tmp+=a
    prob += tmp==b, "Flujo en el nodo "+ni
    if(b!=0):
        print(tmp)

prob += a, "Función objetivo"
print(prob)
#Solución del problema
prob.solve()
for v in prob.variables():
    if(v.varValue>0):
        print(v.name, "=", v.varValue)
        if('_' in v.name):
            _,a,b=v.name.split('_')
            x1, y1=G.nodes[a]['pos']
            x2, y2=G.nodes[b]['pos']
            plt.plot([x1,x2],[y1,y2],'-r',linewidth=3)
        
plt.show()