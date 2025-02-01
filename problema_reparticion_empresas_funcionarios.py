# -*- coding: utf-8 -*-
"""
Created on Sat Feb  1 10:16:58 2025

@author: 000010478
"""

#Problema de los funcionarios y la repartición de responsabilidades
from pulp import *
import numpy as np
empresas=[70, 90, 110, 90, 60, 140, 110, 50, 120, 110, 50, 50]
N=5 #Número de funcionarios

prob = LpProblem("Problema_de_asignacion", LpMinimize)
x=[]
alfa=pulp.LpVariable('Carga_maxima',0,1e6)
for i in range(N): #Para cada funcionario
    tmp=[]
    for j in range(len(empresas)): #Para cada empresa
        name='x_'+str(i+1)+'_'+str(j+1)    
        var=pulp.LpVariable(name, cat="Binary") #Creando una variable real entre 0 y 1M.
        tmp.append(var)
    x.append(tmp)

#Carga para cada empleado
for i in range(N): #Para cada funcionario
    tmp=0
    for j in range(len(empresas)): #Para cada empresa
        tmp+=empresas[j]*x[i][j]
    prob+=tmp<=alfa
    
#Restriccion de que cada empresa debe ser atendida por un empleado
for j in range(len(empresas)): #Para cada empresa
    tmp=0
    for i in range(N): #Para cada funcionario
        tmp+=x[i][j]
    prob+=tmp==1

#Funcion objetivo: Minimixzar la carga máxima
prob += alfa, 'Función objetivo'
prob.solve()
for v in prob.variables():
  if(v.varValue>0):
    print(v.name, "=", v.varValue)