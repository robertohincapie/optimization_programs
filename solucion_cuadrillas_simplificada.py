# -*- coding: utf-8 -*-
"""
Created on Fri Mar 28 16:05:41 2025

@author: 000010478
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance_matrix
plt.close('all')
#problema de asignación de sitios de atención de fallas
M=25 #Puntos disponibles para atención de fallas
N=200 #Puntos de atención de fallas

#M=200 #Puntos disponibles para atención de fallas
#N=8000 #Puntos de atención de fallas
L=10000
rf=np.random.uniform(-L, L, size=(N,2))
ri=np.random.uniform(-L, L, size=(M,2))

d=distance_matrix(ri, rf)

def getAlfa(d, dmin):
    alfa=np.zeros_like(d, dtype=int)
    for i in range(len(alfa)):
        for j in range(len(alfa[0])):
            alfa[i,j]=1 if d[i,j]<=dmin else 0
    return alfa
alfa=getAlfa(d,5000)

def setcover(alfa):
    used=[]
    covered=[]
    while(np.max(alfa)>0):
        cov=alfa.sum(axis=1)
        if(max(cov)>0):
            ind=np.argmax(cov)
            used.append(ind)
            covered=list(set(covered+[int(i) for i in range(len(alfa[ind,:])) if alfa[ind,i]==1]))
            alfa[ind,:]*=0
            #print(covered)
            for ci in covered:
                alfa[:,ci]*=0
            
    return len(used), len(covered)/len(alfa[0]), used,

def solucion(used, d, ri, rf):
    d2=d[used, :]
    cx=np.argmin(d2, axis=0)
    d2=np.min(d2, axis=0)
    xf=[r[0] for r in rf]
    yf=[r[1] for r in rf]
    plt.plot(xf, yf, '.k')

    for i in used:
        plt.plot(ri[i][0], ri[i][1], 'ob')
    for i in range(len(cx)):
        plt.plot([rf[i][0], ri[used[cx[i]]][0]], [rf[i][1], ri[used[cx[i]]][1]], ':', color='#aaaaaa')
    plt.axis('equal')
    plt.grid()
    plt.title('Dmax: '+str(np.max(d2)))

dm=np.min(d)+1000
num=20
Nmax=8
while(num>Nmax):
    alfa=getAlfa(d,dm)
    num, pr, used=setcover(alfa)
    print(num, pr, dm)
    dm+=10
solucion(used, d, ri, rf)
    
#Planteamiento del problema equivalente con PuLP
if(M*N<=5000):
    from pulp import *
    #Creacion de variables
    Y={}
    X={}
    for i in range(M):
        Y[i]=LpVariable("Y_"+str(i),lowBound=0, upBound=1, cat="Integer")
        for j in range(N): 
            X[i,j]=LpVariable("X_"+str(i) + "_"+ str(j),lowBound=0, upBound=1, cat="Integer")
    alfa=LpVariable("alfa",lowBound=0)
    #Función objetivo
    prob=LpProblem("Asignacion_cuadrillas",LpMinimize)
    prob+=alfa, "Función objetivo"
    #Restricción de alguien que atienda a cada falla
    for j in range(N):
        tmp=0
        for i in range(M):
            tmp+=X[i,j]
        prob+=tmp==1, "Atención de la falla "+str(j)
    #Restricción de tiempo para cada falla
    for j in range(N):
        tmp=0
        for i in range(M):
            tmp+=X[i,j]*d[i,j]
        prob+=tmp<=alfa, "Retraso de atención a la falla "+str(j)
    #Restricción del número máximo de cuadrillas
    tmp=0
    for i in range(M):
        tmp+=Y[i]
    prob+=tmp<=Nmax, "Número máximo de cuadrillas"
    #Restricción de cuadrilla activa
    for i in range(M):
        tmp=0
        for j in range(N):
            tmp+=X[i,j]
        prob+=tmp<=1000*Y[i], "Activación de la cuadrilla "+str(i) 
    prob.solve()
    plt.figure()
    xf=[r[0] for r in rf]
    yf=[r[1] for r in rf]
    plt.plot(xf, yf, '.k')

    for i,yi in Y.items(): 
        if(yi.varValue==1):
            plt.plot(ri[i][0], ri[i][1], 'ob') #Punto de cuadrilla activo
    for k,xij in X.items():
        i,j=k
        if(xij.varValue==1):
            plt.plot([rf[j][0], ri[i][0]], [rf[j][1], ri[i][1]], ':', color='#aaaaaa')
    plt.axis('equal')
    plt.grid()
    plt.title('Dmax: '+str(prob.objective.value()))