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
M=100 #Puntos disponibles para atención de fallas
N=600 #Puntos de atención de fallas
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
while(num>4):
    alfa=getAlfa(d,dm)
    num, pr, used=setcover(alfa)
    print(num, pr, dm)
    dm+=10
solucion(used, d, ri, rf)
    
