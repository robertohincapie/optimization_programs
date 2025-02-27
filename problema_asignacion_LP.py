import networkx as nx
from pulp import *
import matplotlib.pyplot as plt
plt.close('all')
import numpy as np
from funciones import grafo, dibujarRed

n=30 #Número de nodos por asignar y asignables. 
G=nx.DiGraph()
for i in range(n):
    G.add_node('Recurso'+str(i), x=-10, y=i) #Nodos a asignar
    G.add_node('Persona'+str(i), x=10, y=i) #Nodos que requieren la asignacion

afinidad={}
for i in range(n):
    for j in range(n): 
        a,b='Recurso'+str(i), 'Persona'+str(j)
        afinidad[a,b]=np.random.rand()

prob = LpProblem("Problema_asignacion", LpMaximize)
x={}
for i in range(n):
    for j in range(n): 
        a,b='Recurso'+str(i), 'Persona'+str(j)
        x[a,b] = pulp.LpVariable("x_"+a+'_'+b, 0, 10000)

#Restricciones de salida de cada recurso
for i in range(n):
    suma=0
    for j in range(n): 
        a,b='Recurso'+str(i), 'Persona'+str(j)
        suma+=x[a,b]
    prob += suma==1, "El recurso "+str(i)+" solo puede asignarse en total una vez. "

#Restricciones de salida de cada recurso
for j in range(n):
    suma=0
    for i in range(n): 
        a,b='Recurso'+str(i), 'Persona'+str(j)
        suma+=x[a,b]
    prob += suma==1, "La persona "+str(j)+" recibe solo un recurso"
    
#Función objetivo
suma=0
for j in range(n):
    for i in range(n): 
        a,b='Recurso'+str(i), 'Persona'+str(j)
        suma+=x[a,b]*afinidad[a,b]
    
prob += suma, "Función objetivo"

#Solución del problema
prob.solve()
for v in prob.variables():
    if(v.varValue>0):
        print(v.name, "=", v.varValue)
        _,a,b=v.name.split('_')
        G.add_edge(a,b)

dibujarRed(G)