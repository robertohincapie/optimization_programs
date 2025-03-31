# -*- coding: utf-8 -*-
"""
Created on Sun Mar 23 09:05:12 2025

@author: 000010478
"""
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import heapq
from scipy.spatial import distance_matrix
plt.close('all')
M=9 #Número de subestaciones #Por ahora fijo, para poder distribuir uniformemente
N=400 #Número de puntos de conexion
L=10000 #Tamaño de la región

ru=np.random.uniform(low=-L, high=L, size=(N,2))
re=[]
for xe in [-2/3*L,0,2/3*L]:
    for ye in [-2/3*L,0,2/3*L]:
        re.append([xe,ye])
re=np.array(re)

edges=[]
d=distance_matrix(re,ru)
d2=distance_matrix(ru,ru)
for i in range(M):
  G=nx.Graph()
  G.add_node('SE'+str(i),pos=(re[i,0],re[i,1]))
  for j in range(N):
    G.add_node(j, pos=(ru[j,0],ru[j,1]))
    G.add_edge('SE'+str(i),j, weight=d[i,j])
  for j in range(N-1):
    for k in range(j+1,N):
      G.add_edge(j,k, weight=d2[j,k])
  Tree=nx.minimum_spanning_tree(G)
  for a,b in Tree.edges():
    if(a!='SE'+str(i) and b!='SE'+str(i)):
      edges.append((a,b,Tree.edges[a,b]['weight']))
edges=list(set(edges))

G=nx.Graph()
for j in range(N):
  G.add_node(j, pos=(ru[j,0],ru[j,1]))
for a,b,w in edges:
  G.add_edge(a,b, weight=w)
Tree=nx.minimum_spanning_tree(G)

#Programacion de los enlaces que se pueden quitar aleatoriamente
edges=[]
for a,b in Tree.edges:
  edges.append((a,b,float(G.edges[a,b]['weight'])))
for i in range(M):
  dist=[np.linalg.norm(re[i]-rj) for rj in ru]
  for k in range(2):
    j=np.argmin(dist)
    edges.append(('SE'+str(i),int(j), float(dist[j])))
    dist[j]=1e10

plt.figure(figsize=(12,12))
plt.plot(ru[:,0],ru[:,1],'r.')
plt.plot(re[:,0],re[:,1],'bo', markersize=10)
G=nx.Graph()
for a,b,w in edges:
  G.add_edge(a,b,weight=w)
  if(str(a)[0]=='S'):
    x1,y1=re[int(a[2])]
  else:
    x1,y1=ru[a]
  if(str(b)[0]=='S'):
    x2,y2=re[int(b[2])]
  else:
    x2,y2=ru[b]
  plt.plot([x1,x2],[y1,y2],'k-')
plt.axis('equal')
fixed=[]
conmutados=[]
for i in range(N):
  if(G.degree(i)==1):
    plt.plot(ru[i,0],ru[i,1],'ms')
    #Voy a calcular las rutas a las 4 subestaciones desde cada nodo extremo.
    P=[]
    for s in range(M):
      path=nx.shortest_path(G,source=i,target='SE'+str(s))
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
    fixed=list(set(fixed+PA[:-1]))
    for j in range(len(PA)-1):
      x1,y1=ru[PA[j]]
      x2,y2=ru[PA[j+1]]
      plt.plot([x1,x2],[y1,y2],'-r')
for i in range(N):
  if(G.degree(i)>2 and i not in fixed):
    plt.plot(ru[i,0],ru[i,1],'gs')
    conmutados.append(i)
for a,b,w in edges:
  if(str(a)[0]=='S'):
    conmutados.append(b)
    plt.plot(ru[b,0],ru[b,1],'gs')
  if(str(b)[0]=='S'):
    conmutados.append(a)
    plt.plot(ru[a,0],ru[a,1],'gs')

edges2=[]
for a,b,w in edges:
  if(a not in conmutados and b not in conmutados):
    edges2.append((a,b,w,'fixed'))
  else:
    edges2.append((a,b,w,'sw'))

plt.figure(figsize=(12,12))
plt.plot(ru[:,0],ru[:,1],'r.')
plt.plot(re[:,0],re[:,1],'bo', markersize=10)
for a,b,w,tipo in edges2:
  if(str(a)[0]=='S'):
    x1,y1=re[int(a[2])]
  else:
    x1,y1=ru[a]
  if(str(b)[0]=='S'):
    x2,y2=re[int(b[2])]
  else:
    x2,y2=ru[b]
  if(tipo=='fixed'):
    plt.plot([x1,x2],[y1,y2],'k-')
  else:
    plt.plot([x1,x2],[y1,y2],'r-')
plt.axis('equal')

#Construcción para coincidir con el código anterior
puntos=[]
for i,r in enumerate(re):
    puntos.append([r[0], r[1], 0])
for i,r in enumerate(ru):
    puntos.append([r[0], r[1], np.random.uniform(1,10)]) #Se pondrá una demanda uniforme entre 1 y 10

#links, cada nodo empieza desde 0, entonces, a los puntos que son SE, me toca ponerlos de 0 a M
#Los puntos que no son subestación toca sumarles M
links=[]
for a,b,w,tipo in edges2:
    if(str(a)[0]=='S'):
      i=int(a[2])
    else:
      i=a+M
    if(str(b)[0]=='S'):
      j=int(b[2])
    else:
      j=b+M
    if(tipo=='fixed'):
      links.append((i,j,w,''))
    else:
      links.append((i,j,w,'x'))

def fair_spanning_tree_with_fixed_links(G, demand, source, fixed_edges):
    file=open('debug.txt','w')
    T = nx.Graph()
    T.add_nodes_from(G.nodes())
    T.add_edges_from(fixed_edges)

    # Initialize flow from demand
    subtree_flow = {v: demand.get(v, 0) for v in G.nodes()}
    file.write('Subtree Flow'+ str(subtree_flow)+'\n')
    # Initial components (due to fixed edges)
    components = list(nx.connected_components(T))
    file.write('Componentes: \n')
    for ci in components: 
        file.write(str(ci)+'\n')

    for comp in components:
        total_flow = sum(demand.get(v, 0) for v in comp)
        for v in comp:
            subtree_flow[v] = total_flow
    file.write('Subtree Flow' + str(subtree_flow)+'\n')
    iteracion=0
    while not nx.is_connected(T):
        file.write('\nIteracion: '+str(iteracion)+'\n')
        iteracion+=1
        candidate_edges = []

        for u, v in G.edges():
            if T.has_edge(u, v):
                continue

            # Check if they belong to different components
            for comp_u in components:
                if u in comp_u:
                    break
            for comp_v in components:
                if v in comp_v:
                    break
            #print(u,v,comp_u, comp_v)
            if comp_u != comp_v:
                flow = min(subtree_flow[u], subtree_flow[v])
                heapq.heappush(candidate_edges, (flow, u, v))
        file.write('Candidate edges:'+str(candidate_edges)+'\n')
        while candidate_edges:
            flow, u, v = heapq.heappop(candidate_edges)
            if not T.has_edge(u, v):
                file.write('Se agrega el enlace '+str(u)+','+str(v)+' al arbol\n')
                T.add_edge(u, v)
                # Update components and flows
                components = list(nx.connected_components(T))
                for comp in components:
                    total_flow = sum(demand.get(node, 0) for node in comp)
                    for node in comp:
                        subtree_flow[node] = total_flow
                file.write('Componentes luego de agregar el enlace: \n')
                for ci in components: 
                    file.write(str(ci)+'\n')

                file.write('Subtree Flow luego de agregar el enlace: \n'+ str(subtree_flow)+'\n')
                break

    file.close()
    return T


plt.figure()
viridis = matplotlib.colormaps['viridis']
#Carga de los datos desde el archivo json

for i in range(M,len(puntos)):
    x,y,d=puntos[i]
    plt.plot(x,y,'ob', markersize=d)

for i in range(M): 
    x,y,d=puntos[i]
    plt.plot(x,y,'sk', markersize=10)

#for i in range(len(puntos)):
#    x,y,d=puntos[i]
#    plt.text(x,y,str(i))

gates=[]    
for i,j,_,tipo in links:
    plt.plot([puntos[i][0],puntos[j][0]],[puntos[i][1],puntos[j][1]],'-k')
    if(tipo=='x'):
        gates.append((i,j))
        xc=(puntos[i][0]+puntos[j][0])/2
        yc=(puntos[i][1]+puntos[j][1])/2
        plt.plot(xc,yc,'xr')
plt.axis('equal')        

#Armado de la red
G=nx.Graph()
fijos=[]
demand={}
G.add_node('S', tipo='Source')
demand['S']=0
for i in range(len(puntos)):
    tipo='SE' if i <M else 'Tr'
    G.add_node(i, tipo=tipo)
    demand[i]=puntos[i][2]
    if(tipo=='SE'):
        G.add_edge('S',i)
        fijos.append(('S',i))
for i,j,_,tipo in links: 
    G.add_edge(i,j)    
    if(tipo!='x'):
        fijos.append((i,j))

Tree=fair_spanning_tree_with_fixed_links(G, demand, 'S', fijos)

plt.figure()
for i in range(M,len(puntos)):
    x,y,d=puntos[i]
    plt.plot(x,y,'ob', markersize=d)

for i in range(M): 
    x,y,d=puntos[i]
    plt.plot(x,y,'sk', markersize=10)

#for i in range(len(puntos)):
#    x,y,d=puntos[i]
#    plt.text(x,y,str(i))

for i,j in Tree.edges():
    if(str(i)!='S'):
        x1,y1,_=puntos[i]
        x2,y2,_=puntos[j]
        plt.plot([x1,x2],[y1,y2],'-k')
plt.axis('equal')
        