# -*- coding: utf-8 -*-
"""
Created on Sat Mar  8 15:25:58 2025

@author: 000010478
"""

from pulp import *
import numpy as np

class nodo: 
    def __init__(self, vars, constraints, obj, cad=''):
        self.id=''.join(np.random.choice([c for c in 'abcdefghijklmnopqrstuvwxyz'],10))
        self.procesado=False
        self.hijos=[]
        self.constraints=constraints
        self.vars=vars
        self.vars_from_name={vi.name:vi for vi in vars}
        self.obj=obj
        self.prob=LpProblem('Problema_original', LpMaximize)
        self.prob+=obj, 'Función objetivo'
        for i, co in enumerate(self.constraints):
            self.prob+=co, 'Restricción '+str(i)
        if(len(cad)>0):
            self.cad=cad
        else:
            self.cad=str(self.prob)
        sol=self.prob.solve()
        self.feasible=sol==1
        self.valores={}
        if(self.feasible):
            self.valores['Obj']=self.prob.objective.value()
            for vi in self.vars:
                self.valores[vi.name]=vi.varValue
        self.checkEntero()
        self.to_string()
    def to_string(self):
        if(self.feasible):
            cad='Solución del problema'
            for n,v in self.valores.items():
                cad2=''
                if(self.entero[n]):
                    cad2='(*)'
                cad=cad+'\n'+n+cad2+'='+str(v)
        else:
            cad='El problema no es factible'
        self.cad=self.cad+'\n'+cad
    def print(self):
        print(self.cad)
        
    def checkEntero(self):
        tol=1e-10
        self.entero={'Obj':False}
        for vi in self.vars:
            if(np.abs(vi.varValue-np.round(vi.varValue))<tol):
                self.entero[vi.name]=True
            else:
                self.entero[vi.name]=False
    def procesar(self, nodos):
        if(not(self.procesado)):
            #print('Se va a procesar el nodo')
            self.procesado=True
            if(self.feasible): #Si no es factible, no se puede procesar
                #determinamos las variables que no son enteras. De manera aleatoria elegimos una de ellas. 
                v=[n for n,ent in self.entero.items() if not(ent) and n!='Obj']
                #print(v)
                if(len(v)>0): #Hay variables por restringir a enteras
                    n=np.random.choice(v)
                    valor=self.valores[n]
                    variable=self.vars_from_name[n]
                    r1=variable<=np.floor(valor)
                    r2=variable>=np.ceil(valor)
                    na=nodo(self.vars, self.constraints+[r1], self.obj, str(r1))
                    nb=nodo(self.vars, self.constraints+[r2], self.obj, str(r2))
                    self.hijos=[na, nb]
                    nodos.append(na)
                    nodos.append(nb)                    
                    
x=LpVariable('x',0,1000)
y=LpVariable('y',0,1000)
#Problema 1
restricciones1=[5*x+3*y<=15, x+4*y<=10]
obj1=2*x+5*y

#Problema 2
restricciones2=[x<=5.5, y<=16.5, x+y<=10, x-3*y<=4]
obj2=3*x+2*y

nodos=[nodo([x,y], restricciones2, obj2)]
cont=10
while(cont>=0 and not(all([ni.procesado for ni in nodos]))):
    cont-=1
    for ni in nodos: 
        ni.procesar(nodos)

cad='digraph G {\n'
for ni in nodos:
    if(ni.feasible):
        color='lightgreen'
        if(len(ni.hijos)==0):
            color='steelblue1'
    else:
        color='lightcoral'
    cad=cad+'    '+ni.id+' [shape=box, style=filled, fillcolor='+color+', color=black, label="'+ni.cad+'"];\n'
for ni in nodos:
    if(len(ni.hijos)>0):
        for hi in ni.hijos:
            cad=cad+ni.id + '->' + hi.id + ';\n'


cad=cad+'}'
with open('salida.gv','w') as file:
    file.write(cad)
    
#Puede mirar el resultado del grafo de visualización en: 
#https://dreampuf.github.io/GraphvizOnline/