# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 17:37:41 2025

@author: 000010478
"""

from pulp import *
import matplotlib.pyplot as plt

# Conunto de planificaciones disponibles
S=[[1,0,1,0,1,0,1,0,0,0,0,0,0,0,1,0,1,0,1,0,1,0,0,0,0,0,0,0,1,0,1,0,1,0,1,0,0,0,0,0,0,0,1,0,1,0,1,0,1,0,0,0,0,0,0,0,1,0,1,0],
[0,0,1,0,1,0,1,0,1,0,0,0,0,0,0,0,1,0,1,0,1,0,1,0,0,0,0,0,0,0,1,0,1,0,1,0,1,0,0,0,0,0,0,0,1,0,1,0,1,0,1,0,0,0,0,0,0,0,1,0],
[0,0,0,0,1,0,1,0,1,0,1,0,0,0,0,0,0,0,1,0,1,0,1,0,1,0,0,0,0,0,0,0,1,0,1,0,1,0,1,0,0,0,0,0,0,0,1,0,1,0,1,0,1,0,0,0,0,0,0,0],
[0,0,0,0,0,0,1,0,1,0,1,0,1,0,0,0,0,0,0,0,1,0,1,0,1,0,1,0,0,0,0,0,0,0,1,0,1,0,1,0,1,0,0,0,0,0,0,0,1,0,1,0,1,0,1,0,0,0,0,0],
[0,1,0,1,0,1,0,1,0,0,0,0,0,0,0,1,0,1,0,1,0,1,0,0,0,0,0,0,0,1,0,1,0,1,0,1,0,0,0,0,0,0,0,1,0,1,0,1,0,1,0,0,0,0,0,0,0,1,0,1],
[0,0,0,1,0,1,0,1,0,1,0,0,0,0,0,0,0,1,0,1,0,1,0,1,0,0,0,0,0,0,0,1,0,1,0,1,0,1,0,0,0,0,0,0,0,1,0,1,0,1,0,1,0,0,0,0,0,0,0,1],
[0,0,0,0,0,1,0,1,0,1,0,1,0,0,0,0,0,0,0,1,0,1,0,1,0,1,0,0,0,0,0,0,0,1,0,1,0,1,0,1,0,0,0,0,0,0,0,1,0,1,0,1,0,1,0,0,0,0,0,0],
[0,0,0,0,0,0,0,1,0,1,0,1,0,1,0,0,0,0,0,0,0,1,0,1,0,1,0,1,0,0,0,0,0,0,0,1,0,1,0,1,0,1,0,0,0,0,0,0,0,1,0,1,0,1,0,1,0,0,0,0]]
rho=20 #Número de personas necesarias en cualquiera de los turnos

def primal(S):
    y = []
    fo = 0
    for i in range(len(S)):
        y.append(LpVariable('y_'+str(i), 0, 1000, cat='Integer'))
        fo += y[-1]
    primal = LpProblem('Primal', LpMinimize)
    for j in range(len(S[0])):  # Iteramos sobre las piezas que necesitamos cortar
        tmp = 0
        for i in range(len(S)):
            tmp += S[i][j]*y[i]
        primal += tmp >= rho, 'Demanda del trabajadores en el turno '+str(j)
    primal += fo, "Función objetivo"
    #print(primal)
    primal.solve()
    res = [yi.value() for yi in y]
    Z = primal.objective.value()
    return res, Z


def dual(S):
    mu = []
    fo = 0
    for i in range(len(S[0])):
        mu.append(LpVariable('mu_'+str(i), 0, 1000))
        fo += rho*mu[-1]
    dual = LpProblem('Dual', LpMaximize)
    for i in range(len(S)):  # Iteramos sobre las variables de decisión actualmente disponibles
        tmp = 0
        for j in range(len(S[0])):
            tmp += S[i][j]*mu[j]
        dual += tmp <= 1, 'Restriccion '+str(i)
    dual += fo, "Función objetivo"
    #print(dual)
    dual.solve()
    res = [mui.value() for mui in mu]
    Z = dual.objective.value()
    return res, Z


def secundario(mu):
    x = []
    M=100
    fo = 1
    for i in range(len(mu)):
        x.append(pulp.LpVariable('x_'+str(i+1), 0, 1, cat='Binary'))
        fo -= mu[i]*x[-1]
    secondary = LpProblem('Secondary', LpMinimize)
    #Restricciones del problema secundario
    #Definición de semanas: 
    t=list(range(1,len(S[0])+1))
    sem=[list(range(i,min(i+14, max(t)+1))) for i in t if (i-1)%14==0]
    for i, si in enumerate(sem): #Cada semana
        tmp = 0
        for ti in si: 
            tmp+=x[ti-1]
        secondary+=tmp<=4, "Número de turnos en la semana "+str(i)
    #No más de un turno seguido
    for ti in t[:-1]:
        secondary+=x[ti-1]+x[ti]<=1, "Turnos seguidos en ti="+str(ti)
    #Luego de un turno de noche, no se pueden tener turnos de día en los dos días siguientes: 
    for ti in t[:-1]:
        if(ti%2==0): #Es un turno de noche, par
            if(ti+2<len(x)):
                secondary+=x[ti]+x[ti+2]<=M*(1-x[ti-1])
            else:
                secondary+=x[ti]<=M*(1-x[ti-1])
                
    secondary += fo, "Función objetivo"
    #print(secondary)
    secondary.solve()
    res = [int(xi.value()) for xi in x]
    Z = secondary.objective.value()
    return res, Z
# resS, Zs, secondary=secundario(resd, l,L)
# print('Secundario: ', resS)


val = []
vZs = []
mRes=[]
mResD=[]
for i in range(800):
    res, Z = primal(S)
    mRes.append(res)
    val.append(Z)
    resd, Zd = dual(S)
    mResD.append(resd)
    resS, Zs = secundario(resd)
    vZs.append(Zs)
    if (Zs > -1e-6):
        break
    print(i,Z)
    S.append(resS)
    
for xi, si in zip(res, S):
    if(xi>0):
        print('El Schedule: ',si)
        print('Se repite ',xi,' veces')
        print('---------------------')
        
