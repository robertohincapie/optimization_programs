# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 17:37:41 2025

@author: 000010478
"""

from pulp import *
import matplotlib.pyplot as plt

# Conunto de patrones existentes en el momento
P = [[0, 2, 0, 1], [6, 1, 1, 0]]
D = [40, 30, 35, 8]
h = [20, 50, 120, 200]
L = 300


def primal(P):
    x = []
    fo = 0
    for i in range(len(P)):
        x.append(pulp.LpVariable('x_'+str(i), 0, 1000, cat='Integer'))
        fo += x[-1]
    primal = LpProblem('Primal', LpMinimize)
    for j in range(len(P[0])):  # Iteramos sobre las piezas que necesitamos cortar
        tmp = 0
        for i in range(len(P)):
            tmp += P[i][j]*x[i]
        primal += tmp >= D[j], 'Demanda del producto '+str(j)
    primal += fo, "Función objetivo"
    print(primal)
    primal.solve()
    res = [xi.value() for xi in x]
    Z = primal.objective.value()
    return res, Z


def dual(P):
    y = []
    fo = 0
    for i in range(len(D)):
        y.append(pulp.LpVariable('y_'+str(i), 0, 1000))
        fo += D[i]*y[-1]
    dual = LpProblem('Dual', LpMaximize)
    for i in range(len(P)):  # Iteramos sobre las variables de decisión actualmente disponibles
        tmp = 0
        for j in range(len(P[0])):
            tmp += P[i][j]*y[j]
        dual += tmp <= 1, 'Restriccion '+str(i)
    dual += fo, "Función objetivo"
    print(dual)
    dual.solve()
    res = [yi.value() for yi in y]
    Z = dual.objective.value()
    return res, Z


def secundario(y, l, L):
    u = []
    fo = 1
    for i in range(len(y)):
        u.append(pulp.LpVariable('u_'+str(i), 0, 1000, cat='Integer'))
        fo -= y[i]*u[-1]
    secondary = LpProblem('Secondary', LpMinimize)
    tmp = 0
    for j in range(len(h)):  # Iteramos sobre los productos que tenemos
        tmp += h[j]*u[j]
    secondary += tmp <= L, 'Longitud máxima de la pieza'
    secondary += fo, "Función objetivo"
    print(secondary)
    secondary.solve()
    res = [ui.value() for ui in u]
    Z = secondary.objective.value()
    return res, Z, secondary
# resS, Zs, secondary=secundario(resd, l,L)
# print('Secundario: ', resS)


val = []
vZs = []
for i in range(10):
    res, Z = primal(P)
    val.append(Z)
    resd, Zd = dual(P)
    resS, Zs, secondary = secundario(resd, h, L)
    vZs.append(Zs)
    if (Zs > -1e-6):
        break
    P.append(resS)
plt.close('all')
dy = 20
y = 0
ind = 0
for pi in P:
    d = 0
    for i in range(len(pi)):
        for k in range(int(pi[i])):
            plt.plot([d, d+h[i], d+h[i], d, d], [y, y, y+dy, y+dy, y], '-k')
            d += h[i]
    plt.text(1.01*L, y+dy/2, 'Usado '+str(int(res[ind]))+' veces')
    y += 2*dy
    ind += 1

plt.axis('equal')
plt.xlim(-50,L+150)