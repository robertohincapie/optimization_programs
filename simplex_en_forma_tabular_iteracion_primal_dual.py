from prettytable import PrettyTable
import numpy as np
import matplotlib.pyplot as plt

class LP:
  def __init__(self, A, b, c, vars, basicVars, tipo='max'):
    self.A=A
    self.b=b
    self.c=c
    self.vars=vars
    self.col={v:i+1 for i,v in enumerate(vars)}
    self.col['Z']=0
    self.col['B']=len(vars)+1
    self.tipo=tipo
    colZ=np.zeros(shape=(len(A)+1,1))
    colZ[0]=1
    Z=np.hstack((A,b))
    Z=np.vstack((np.hstack((-c,[[0]])),Z))
    Z=np.hstack((colZ,Z))
    self.Z=Z
    self.basicVars=[]
    self.setBasicVars(basicVars)
    print('Matriz original')
    self.dibujar_matriz()
  def setBasicVars(self, basicVars): #Esta función no solamente agrega
    #las variables básicas, sino que reorganiza la matriz para que las
    #B queden de primeras
    basicasAnteriores=self.basicVars.copy()
    self.basicVars=basicVars
    self.nobasicVars=sorted(list(set(self.vars)-set(self.basicVars)))
    z2=[self.Z[:,0]]
    col2={}
    pos=1
    vars2=[]
    for vi in self.basicVars:
        z2.append(self.Z[:,self.col[vi]])
        col2[vi]=pos
        pos+=1
        vars2.append(vi)
    for vi in self.nobasicVars:
        z2.append(self.Z[:,self.col[vi]])
        col2[vi]=pos
        pos+=1
        vars2.append(vi)
    z2.append(self.Z[:,-1])
    col2['Z']=0
    col2['B']=len(self.vars)+1
    z2=np.array(z2).T
    self.Z=z2
    self.col=col2
    self.vars=vars2
    self.pivot()
    #self.dibujar_matriz()
  def dibujar_matriz(self):
    # Specify the Column Names while initializing the Table
    cols=[' ']
    for v in self.vars:
      if v in self.basicVars:
        cols.append(v+'(*)')
      else:
        cols.append(v)
    cols=cols+['B']
    myTable = PrettyTable(cols)
    for i in range(len(self.Z)):
      row=[]
      #if(i==0):
      #  for j in range(len(self.Z[i])):
      #    row.append(str(np.round(self.Z[i][j],3)))
      #else:
      BV=list(self.col.keys())[list(self.col.values()).index(i)]
      row.append(BV)
      for j in range(1,len(self.Z[i])):
        row.append(str(np.round(self.Z[i][j],3)))
      myTable.add_row(row)
    print(myTable)
  def fila_por_escalar(self, Varfila, escalar):
    fila=list(self.col.keys())[list(self.col.values()).index(Varfila)]
    self.Z[fila,:]=self.Z[fila,:]*escalar
  def sumar_fila_por_escalar(self, Varfila, escalar, Varfila_objeto):
    #fila=list(self.col.keys())[list(self.col.values()).index(Varfila)]
    fila=self.col[Varfila]
    #fila_objeto=list(self.col.keys())[list(self.col.values()).index(Varfila_objeto)]
    fila_objeto=self.col[Varfila_objeto]
    self.Z[fila_objeto,:]=self.Z[fila_objeto,:]+self.Z[fila,:]*escalar
  def pivotar(self, Varfila):
    fila=self.col[Varfila]
    col=fila
    self.Z[fila,:]=self.Z[fila,:]/self.Z[fila,col]
    for i in range(len(self.Z)):
      if(i!=fila):
        self.Z[i,:]=self.Z[i,:]-self.Z[i,col]*self.Z[fila,:]
  def analizarVariableQueSale(self, entrante):
    col=self.col[entrante]
    factor=(self.Z[:,-1]/self.Z[:,col])[1:]
    cad=''
    for bvi, fi in zip(self.basicVars, factor):
      cad=cad+'Variable básica: '+bvi+', límite de variable entrante: '+str(fi)+'\n'
    print('\nAnalizando salida ante la variable entrante '+entrante+':\n', cad)
  def cambiarVariablesBasicas(self, entrante, saliente):
    bv=self.basicVars.copy()
    bv[bv.index(saliente)]=entrante
    self.setBasicVars(bv)
    
  def paso(self): 
    #Revisamos la variable entrante. Depende del tipo del problema
    coefs=[self.Z[0,self.col[v]] for v in self.nobasicVars]
    if(self.tipo=='max'): #Es maximizar, se elige la más negativa
      ind=np.argmin(coefs)
      if(coefs[ind]>0): #Ya es la solución optima
        print('Ya se encuentra en la solución óptima')
        return True
    else:
      ind=np.argmax(coefs)
      if(coefs[ind]<0): #Ya es la solución optima
        print('Ya se encuentra en la solución óptima')
        return True
    #Significa que podemos continuar. 
    entrante=self.nobasicVars[ind]
    print('Variable entrante: ',entrante)
    #Se debe determinar la variable saliente. 
    col=self.col[entrante]
    factor=()[1:]
    vmin=1e10
    saliente=''
    for bvi in self.basicVars:
      if(self.Z[self.col[bvi],col]>0):
        v=self.Z[self.col[bvi],-1]/self.Z[self.col[bvi],col]
        if(v<vmin):
          vmin=v
          saliente=bvi
    print('Variable saliente:', saliente)
    self.cambiarVariablesBasicas(entrante=entrante, saliente=saliente)
    self.pivot()
    self.dibujar_matriz()
  def pivot(self):
    for bvi in self.basicVars:
      self.pivotar(bvi)
  def getAb(self):
    return np.array([self.Z[1:,self.col[vi]] for vi in self.basicVars]).T
  def getA(self):
    return np.array([self.Z[1:,self.col[vi]] for vi in self.basicVars+self.nobasicVars]).T
  def getCb(self):
    return np.array([self.Z[0,self.col[vi]] for vi in self.basicVars])
  def getC(self):
    return np.array([self.Z[0,self.col[vi]] for vi in self.basicVars+self.nobasicVars])
  def getDualSol(self):
    Ab=self.getAb()
    Cb=self.getCb()
    B=self.Z[1:,-1]
    y=np.matmul(Cb,np.linalg.pinv(Ab))
    Zd=np.dot(B,y)
    rest=np.matmul(self.getA().T,y)-self.getC()
    print('\nVariables duales:',y,'\nSolución dual:',Zd, '\nRestricciones:',rest)
    
#Problema 1:
print('Problema primario')
primal=LP(A = np.array([[1,2,1,0,0],[2,1,0,1,0],[5,6,0,0,1]]),
      b = np.array([10,4,50]).reshape(-1,1),
      c = np.array([4,3,0,0,0]).reshape(1,-1),
      vars=['x','y','h1','h2','h3'], basicVars=['h1', 'h2','h3'], tipo='max')

cond=True
vZp=[primal.Z[0,-1]]
while(cond):
    cond=not(primal.paso())
    vZp.append(primal.Z[0,-1])
    #Vamos a mostrar las condiciones de la solución dual: 
    
print('------------------------\n\n')

print('Problema dual')
dual=LP(A = np.array([[1,2,5,-1,0],[2,1,6,0,-1]]),
      b = np.array([4,3]).reshape(-1,1),
      c = np.array([10,4,50,0,0]).reshape(1,-1),
      vars=['y1','y2','y3','h1','h2'], basicVars=['y1', 'h2'], tipo='min')
cond=True
vZd=[dual.Z[0,-1]]
while(cond):
    cond=not(dual.paso())
    vZd.append(dual.Z[0,-1])
plt.close('all')
plt.plot(vZp, 'x-r', label='F.O. problema primal')
plt.plot(vZd, 'o-b', label='F.O. problema dual')
plt.grid()

plt.legend()