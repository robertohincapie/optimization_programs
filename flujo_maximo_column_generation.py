import networkx as nx
from pulp import *
import matplotlib.pyplot as plt
plt.close('all')
import numpy as np
from funciones import grafo, dibujarRed
n=50
G=nx.DiGraph()
x,y,edges=grafo(L=100, N=n, d=60)
d_org=[np.sqrt((x[i]-100)**2+(y[i]-100)**2) for i in range(n)]
s=np.argmin(d_org)
t=np.argmax(d_org)

nodos={}
dist=[]
for i in range(n):
    nodos[i]=(x[i], y[i])
for i,j in edges:
    dij=np.sqrt((x[i]-x[j])**2+(y[i]-y[j])**2)
    dist.append((i, j, dij))

cap=10

for k,pos in nodos.items():
    G.add_node(k, x=pos[0], y=pos[1])
for a,b,d in dist: 
    cap=np.random.randint(low=5, high=10)
    G.add_edge(a,b,weight=d, capacity=cap)
    G.add_edge(b,a,weight=d, capacity=cap)
    
dibujarRed(G)
caminos=[]
path=nx.shortest_path(G, s, t, weight="weight")
caminos.append(path)

def camino_incluye_enlace(camino, a, b):
    for i in range(len(camino)-1):
        if(a==camino[i] and b==camino[i+1]):
            return True
    return False

condicion=True #Vamos a considerar que podemos continuar mejorando el problema
cont=400
while(condicion and cont>=0):
    cont-=1
    plt.figure()
    dibujarRed(G)
    for path in caminos: 
        for i in range(len(path)-1):
            a,b=path[i], path[i+1]
            plt.plot([x[a], x[b]], [y[a], y[b]], '-r')
    condicion=False
    #Problema maestro, flujo máximo. 
    print("Problema primario")
    prob = LpProblem("Problema_flujo_maximo", LpMaximize)
    #Crear las variables
    fi=[]
    for i in range(len(caminos)):
        fi.append(pulp.LpVariable("Fi_"+str(i), 0, 1e6))
    #Restricciones de cada enlace: 
    for a,b in G.edges:
        tmp=0
        for i, path in enumerate(caminos):
            if(camino_incluye_enlace(path, a, b)):
                tmp+=fi[i]
        prob += tmp<=G.edges[a,b]['capacity'], "Capacidad en el enlace "+str(a)+","+str(b)
    tmp=0
    for i in range(len(caminos)):
        tmp+=fi[i]
    
    prob += tmp, "Función objetivo"
    prob.solve()
    print('Valor de la función objetivo: '+str(prob.objective.value()))
    
    #Construcción del problema secundario
    print("Problema secundario")
    
    prob2 = LpProblem("Problema_Secundario_flujo_maximo", LpMinimize)
    #Crear las variables
    pi={}
    fo=0
    for a,b in G.edges:
        pi[(a,b)]=pulp.LpVariable("Pi_"+str(a)+","+str(b), 0, 1e6)
        fo+=G.edges[a,b]['capacity']*pi[(a,b)]
    
    #Restricciones de cada camino
    for c, path in enumerate(caminos):
        tmp=0
        for i in range(len(path)-1):
            tmp+=pi[(path[i],path[i+1])]
        prob2+=tmp>=1, "Restricción del camino "+str(c)
    prob2 += fo, "Función objetivo"
    prob2.solve()
    
    #Miremos los enlaces que quedaron con un valor igual a 1 y los eliminaremos del grafo
    G2=G.copy()
    for v in prob2.variables(): 
        if(v.value()>0):
            _,par=v.name.split('_')
            a,b=par.split(',')
            G2.remove_edge(int(a), int(b))
            plt.plot([x[int(a)], x[int(b)]], [y[int(a)], y[int(b)]], '-g', linewidth=5)
    if(nx.has_path(G2, s,t)):
        #Hay camino posible:
        condicion=True
        path=nx.shortest_path(G2, s, t, weight="weight")
        caminos.append(path)
        print('Se agrega camino, ahora tenemos :'+str(len(caminos)))
        