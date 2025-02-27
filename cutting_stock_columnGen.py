# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 17:37:41 2025

@author: 000010478
"""

from pulp import *
#Conunto de patrones existentes en el momento
P=[[3,1,1]]
d=[20,36,25]
l=[2,5,9]
L=20
def primal(P):
    x=[]
    fo=0
    for i in range(len(P)):
        x.append(pulp.LpVariable('x_'+str(i),0,1000, cat='Integer'))
        fo+=x[-1]
    primal=LpProblem('Primal', LpMinimize)
    for j in range(len(P[0])): #Iteramos sobre los productos que tenemos
        tmp=0    
        for i in range(len(P)):
            tmp+=P[i][j]*x[i]
        primal+=tmp>=d[j], 'Demanda del producto '+str(j)
    primal+=fo, "Función objetivo"
    print(primal)
    primal.solve()
    res=[xi.value() for xi in x]
    Z=primal.objective.value()
    return res, Z

#res, Z=primal(P)
#print('Primal:',res, Z)

def dual(P):
    y=[]
    fo=0
    for i in range(len(P[0])):
        y.append(pulp.LpVariable('y_'+str(i),0,1000))
        fo+=d[i]*y[-1]
    dual=LpProblem('Dual', LpMaximize)
    for i in range(len(P)): #Iteramos sobre las variables de decisión actualmente disponibles
        tmp=0    
        for j in range(len(P[0])):
            tmp+=P[i][j]*y[j]
        dual+=tmp<=1, 'Restriccion '+str(i)
    dual+=fo, "Función objetivo"
    print(dual)
    dual.solve()
    res=[yi.value() for yi in y]
    Z=dual.objective.value()
    return res, Z

#resd, Zd = dual(P)
#print('Dual:',resd, Zd)

def secundario(y,l,L):
    u=[]
    fo=1
    for i in range(len(y)):
        u.append(pulp.LpVariable('u_'+str(i),0,1000, cat='Integer'))
        fo-=y[i]*u[-1]
    secondary=LpProblem('Secondary', LpMinimize)
    tmp=0
    for j in range(len(l)): #Iteramos sobre los productos que tenemos
        tmp+=l[j]*u[j]
    secondary+=tmp<=L, 'Longitud máxima de la pieza'
    secondary+=fo, "Función objetivo"
    print(secondary)
    secondary.solve()
    res=[ui.value() for ui in u]
    Z=secondary.objective.value()
    return res, Z, secondary
#resS, Zs, secondary=secundario(resd, l,L)
#print('Secundario: ', resS)

val=[]
for i in range(10):
    res,Z=primal(P)
    val.append(Z)
    resd,Zd=dual(P)
    resS, Sz, secondary=secundario(resd, l, L)
    if(resS in P):
        break
    P.append(resS)


"""
primal+=4*x1>=25, 'Producto 1'
primal+=2*x2>=20, 'Producto 2'
primal+=2*x3>=15, 'Producto 3'
primal+=x1+x2+x3, 'Función objetivo'
print('Problema primal')
primal.solve()
for v in primal.variables():
   if(v.varValue>0):
    print(v.name, "=", v.varValue)
    
y1=pulp.LpVariable('y1',0,1000)
y2=pulp.LpVariable('y2',0,1000)
y3=pulp.LpVariable('y3',0,1000)
dual=LpProblem('Dual', LpMaximize)
dual+=4*y1<=1, 'Rest 1'
dual+=2*y2<=1, 'Rest 2'
dual+=2*y3<=1, 'Rest 3'
dual+=25*y1+20*y2+15*y3, 'Función objetivo'
print('\n\nProblema dual')
dual.solve()
for v in dual.variables():
   if(v.varValue>0):
    print(v.name, "=", v.varValue)    
    

#Problema secundario
u1=pulp.LpVariable('u1',0,1000, cat='Integer')
u2=pulp.LpVariable('u2',0,1000, cat='Integer')
u3=pulp.LpVariable('u3',0,1000, cat='Integer')
second=LpProblem('Dual', LpMinimize)
second+=5*u1+7*u2+9*u3<=20, 'Rest 1'
second+=1-y1.value()*u1-y2.value()*u2-y3.value()*u3, 'Función objetivo'
print('\n\nProblema secundario')
second.solve()
for v in second.variables():
   if(v.varValue>0):
    print(v.name, "=", v.varValue)    
    
"""