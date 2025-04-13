# -*- coding: utf-8 -*-
"""
Created on Fri Mar 28 16:05:41 2025

@author: 000010478
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance_matrix
from scipy.interpolate import griddata
plt.close('all')
#problema de asignación de sitios de atención de fallas
M=100 #Puntos disponibles para atención de fallas
N=600 #Puntos de atención de fallas
L=10000
rf=np.random.uniform(-L, L, size=(N,2))
ri=np.random.uniform(-L, L, size=(M,2))

d=distance_matrix(ri, rf)

#Método para convertir la distancia a valores alfa_i,j si cumplen con la distancia mínima
def getAlfa(d, dmin):
    alfa=np.zeros_like(d, dtype=int)
    for i in range(len(alfa)):
        for j in range(len(alfa[0])):
            alfa[i,j]=1 if d[i,j]<=dmin else 0
    return alfa

#Método que encuentra los sitios requeridos para cubrir a los sitios de falla de
#acuerdo con la matriz alfa. 
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
            
    return [int(u) for u in used], covered

#Problema que a partir de las estaciones usadas, encuentra el retardo máximo de la red
def problema_retardo(used, d):
    print('Problema de retardo')
    d2=d[used, :]
    d2=np.min(d2, axis=0)
    return np.max(d2), d2

#Problema que elige las activas de un grupo de disponibles, tomando solo N
#y cubriendo a todos los usuarios
def problema_activacion(disponibles, d, N): 
    print('Problema de activación')
    d2=d[disponibles, :]
    dm=np.min(d2)
    num=N+1
    while(num>N):
        alfa=getAlfa(d2,dm)
        used2, covered2=setcover(alfa)
        pr2=len(covered2)/len(d2[0])
        print(pr2, len(used2))
        if(pr2>=1):
            num=len(used2)
            used=used2            
        #print(len(used2),pr2, dm)
        dm+=10
    return [disponibles[u] for u in used]

def problema_adicionar(retardo, rf, ri, ax=None):
    print('Problema de agregar punto de posible cuadrilla')
    x,y=np.meshgrid(np.linspace(-L,L,50),np.linspace(-L,L,50))
    z=griddata(rf, retardo, (x,y), method='nearest')
    z2=z-np.min(z)
    z2=z2/np.sum(z2)
    if(not ax):
        plt.figure()
    plt.contourf(x,y,z,50)
    N=len(x)*len(x[0])
    plt.colorbar()
    plt.axis('equal')
    ind=np.random.choice(a=range(N), p=z2.reshape(N))
    i,j=np.unravel_index(ind, (len(x),len(x[0])))
    rc=np.array([x[i,j], y[i,j]])
    dist=[np.linalg.norm(rc-r) for r in ri]
    elegida=np.argmin(dist)
    plt.plot(ri[elegida][0], ri[elegida][1], 'xr')
    return elegida

#Vamos a comenzar con la posición más cercana al CM de las fallas
cm=rf.mean(axis=0)
dist=[np.linalg.norm(r-cm) for r in ri]

disponibles=[np.argmin(dist)]
SF=6
ind=1
for i in range(50):
    ax=plt.subplot(2,3,ind)
    ind+=1
    used=problema_activacion(disponibles, d, 4)
    alfa, retardo=problema_retardo(used, d)
    elegida=problema_adicionar(retardo, rf, ri, ax)
    for u in used: 
        plt.plot(ri[u][0], ri[u][1], 'ks')
    for di in disponibles: 
        plt.plot(ri[di][0], ri[di][1], 'xy')
    
    plt.title('Alfa actual: '+str(alfa))
    disponibles.append(elegida)
    if(ind>SF):
        plt.figure()
        ind=1
