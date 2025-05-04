import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from scipy.spatial import distance_matrix

M=9 #Número de subestaciones #Por ahora fijo, para poder distribuir uniformemente
N=400 #Número de puntos de conexion
L=10000 #Tamaño de la región

def dibujarRed(G, size=(8,8), ax=None, conectividad=False):
  dem=[G.nodes[i]['demanda'] for i in G.nodes]
  dmax=np.max(dem)
  K=5/dmax
  if(not(ax)):
      plt.figure(figsize=size)
  for i in G.nodes:
    tipo=G.nodes[i]['tipo']
    dem=G.nodes[i]['demanda']
    size=K*dem+1
    if(tipo=='Tr'):
      plt.plot(G.nodes[i]['pos'][0],G.nodes[i]['pos'][1],'ko', markersize=size)
    if(tipo=='End'):
      plt.plot(G.nodes[i]['pos'][0],G.nodes[i]['pos'][1],'m.', markersize=size)
    if(tipo=='sw'):
      plt.plot(G.nodes[i]['pos'][0],G.nodes[i]['pos'][1],'xr', markersize=size)
    if(tipo=='SE'):
      plt.plot(G.nodes[i]['pos'][0],G.nodes[i]['pos'][1],'sb', markersize=15)
    #if(tipo=='Source'):
    #  plt.plot(G.nodes[i]['pos'][0],G.nodes[i]['pos'][1],'*r', markersize=20)
  for a,b in G.edges:
    tipo=G.edges[a,b]['tipo']
    x1,y1=G.nodes[a]['pos']
    x2,y2=G.nodes[b]['pos']
    if(G.nodes[a]['tipo']!='Source' and G.nodes[b]['tipo']!='Source'): #No se dibuja el enlace a la red de transmisión
      if(tipo=='sw'):
        plt.plot([x1,x2],[y1,y2],'-r')
      if(tipo=='fijo'):
        plt.plot([x1,x2],[y1,y2],'-k')
      if(tipo=='tmp'):
        plt.plot([x1,x2],[y1,y2],':c')

  plt.axis('equal');
  if(conectividad):
    for ni in G.nodes:
      if(nx.has_path(G, source='G', target=ni)):
        plt.plot(G.nodes[ni]['pos'][0],G.nodes[ni]['pos'][1],'or', markersize=10)

ru=np.random.uniform(low=-L, high=L, size=(N,2))
re=[]
for xe in [-2/3*L,0,2/3*L]:
    for ye in [-2/3*L,0,2/3*L]:
        re.append([xe,ye])
re=np.array(re)
edges=[]
d=distance_matrix(re,ru)
d2=distance_matrix(ru,ru)

#Se crea un primer grafo de todos los nodos sin subestaciones.
G=nx.Graph()
for i in range(N):
  G.add_node(i, tipo='Tr', pos=tuple(ru[i]), demanda=np.random.randint(low=1, high=11))
for j in range(N-1):
  for k in range(j+1,N):
    G.add_edge(j,k, weight=d2[j,k], tipo='tmp')
G=nx.minimum_spanning_tree(G)

G.add_node('G', tipo='Source', pos=(0,0), demanda=0)
for i in range(M):
  G.add_node('SE_'+str(i), tipo='SE', pos=tuple(re[i]), demanda=0)
  G.add_edge('SE_'+str(i), 'G', weight=0, tipo='fijo')
  dist=[np.linalg.norm(re[i]-rj) for rj in ru]
  for k in range(2):
    j=np.argmin(dist)
    G.add_edge('SE_'+str(i),int(j), weight=float(dist[j]), tipo='sw')
    G.nodes[int(j)]['tipo']='sw'
    dist[j]=1e10

dibujarRed(G)

for i in range(N):
  if(G.degree(i)==1): #Los nodos extremos, que tienen grado 1. Son un extremo de un camino
    G.nodes[i]['tipo']='End'
    #Voy a calcular las rutas a las 4 subestaciones desde cada nodo extremo.
    P=[]
    for s in range(M):
      path=nx.shortest_path(G,source=i,target='SE_'+str(s))
      P.append(path)
    i=0
    cond=True
    Lmax=np.min([len(pi) for pi in P])
    PA=[]
    while(cond and i<Lmax):
      nodes=[pi[i] for pi in P]
      i+=1
      if(len(set(nodes))==1 and len(nodes)==len(P) and str(nodes[0])[0]!='S'):
        PA.append(nodes[0])
      else:
        cond=False
    for j in range(len(PA)-1):
      G.edges[PA[j], PA[j+1]]['tipo']='fijo'
#Los nodos que tienen grado mayor a 2, lo que no sea fijo, queda sw.
for i in range(N):
  if(G.degree(i)>2):
    e=list(G.edges(i))
    for a,b in e:
      if(G.edges[a,b]['tipo']!='fijo'):
        G.edges[a,b]['tipo']='sw'
#Todo lo que queda lo consideraré fijo
for a,b in G.edges:
  if(G.edges[a,b]['tipo']=='tmp'):
    G.edges[a,b]['tipo']='fijo'

dibujarRed(G)

ind=10
for ni in G.nodes:
  ind-=1
  if(ind>=0):
    print(ni, G.nodes[ni])
ind=10
for a,b in G.edges:
  ind-=1
  if(ind>=0):
    print(a,b, G.edges[a,b])

#Función que arma un arbol a partir de los enlaces fijos de un grafo G
def armarArbol(G):
  Tree=nx.Graph()
  for ni in G.nodes:
      Tree.add_node(ni, pos=G.nodes[ni]['pos'], demanda=G.nodes[ni]['demanda'], tipo=G.nodes[ni]['tipo'])
  for a,b in G.edges:
      if(G.edges[a,b]['tipo']=='fijo'):
          Tree.add_edge(a,b, weight=G.edges[ni,'G']['weight'], tipo=G.edges[ni,'G']['tipo'])
  return Tree
#Función que a partir de un árbol, regresa el componente principal o root y los diferentes componentes no conectados de la red
def getComponentes(Tree):
  componentes=list(nx.connected_components(Tree))
  for i,comp in enumerate(componentes):
    for ni in comp:
      Tree.nodes[ni]['componente']=i
  componentes={i:{'nodos':comp, 'demanda':0, 'links':[]} for i,comp in enumerate(componentes)}
  for ni in Tree.nodes:
    componentes[Tree.nodes[ni]['componente']]['demanda']+=Tree.nodes[ni]['demanda']
  for a,b in G.edges:
    if(G.edges[a,b]['tipo']=='sw'):
      componentes[Tree.nodes[a]['componente']]['links'].append((a,b,Tree.nodes[b]['componente']))
      componentes[Tree.nodes[b]['componente']]['links'].append((b,a,Tree.nodes[a]['componente']))
  root=[i for i,k in componentes.items() if 'G' in k['nodos']][0]
  return componentes, root
def usoCapacidad(Tree):
  C={}
  for a,b in Tree.edges:
    C[a,b]=0
    C[b,a]=0
  for ni in Tree.nodes:
    if(nx.has_path(Tree, source='G', target=ni)):
      path=nx.shortest_path(Tree, source='G', target=ni)
      for i in range(len(path)-1):
        C[path[i], path[i+1]]+=Tree.nodes[ni]['demanda']
        C[path[i+1], path[i]]+=Tree.nodes[ni]['demanda']

  Cmax=np.max([C[a,b] for a,b in C.keys()])
  return C, Cmax

Tree=armarArbol(G)
dibujarRed(Tree)
componentes, root=getComponentes(Tree)
C, Cmax=usoCapacidad(Tree)
print('Cmax=',Cmax)

def conectar(G, componentes, Cmax): #Rutina que busca el nuevo componente que se conecta a root, tal que tenga la menor distancia e incremente lo menos posible la capacidad.
  candidatos={}
  for ca, comp in componentes.items():
    for a,b,cb in comp['links']:
      if(ca!=root and cb==root): #El enlace en el componente permite
        candidatos[a,b]={'Componentes':(ca,cb), 'Cmax':0}
  #De todos los candidatos, si hay, es necesario mirar los enlaces de menor distancia y sobre todo que cumplan con el menor aumento de la capacidad de la red.
  Cmenor=1e10
  mejorCandidato=-1
  for k,v in candidatos.items():
    na, nb=k
    prev=G.edges[na,nb]['tipo']
    #print('Analizando nodos: ',k,' entre componentes ',v)
    G.edges[na,nb]['tipo']='fijo'
    T=armarArbol(G)
    C,Cmax=usoCapacidad(T)
    if(Cmax<Cmenor):
      Cmenor=Cmax
      mejorCandidato=k
    candidatos[k]['Cmax']=Cmax
    G.edges[na,nb]['tipo']=prev
  return Cmenor, mejorCandidato

plt.close('all')
Cm=[]
i=0
plt.figure(figsize=(8,8))
ax=plt.subplot(1,1,1)
while(i<100 and len(componentes)>0):
  print(str(i)+', ', end='')
  i+=1
  Cmenor, bestLink=conectar(G, componentes, 10)
  #print('Iteracion: ',i,', Best link: ',bestLink)
  if(bestLink==-1):
    break
  #for k,co in componentes.items():
  #  if(bestLink[0] in co['nodos']):
  #    print(k,co)
  #  if(bestLink[1] in co['nodos']):
  #    print(k,co)

  Cm.append(int(Cmenor))
  G.edges[*bestLink]['tipo']='fijo'
  Tree=armarArbol(G)
  componentes, root=getComponentes(Tree)
  #if(i%5==0):
  ax.cla()
  dibujarRed(Tree, ax=ax, conectividad=True)
  plt.pause(1)
dibujarRed(Tree)

plt.figure()
plt.plot(Cm)
plt.title('Capacidad máxima')
plt.grid()