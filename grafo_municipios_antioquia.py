# -*- coding: utf-8 -*-
"""
Created on Sat Feb  1 11:22:56 2025

@author: 000010478
"""

import networkx as nx
import matplotlib.pyplot as plt

# Crear un grafo no dirigido
G = nx.Graph()

# Añadir los municipios como nodos
municipios = [
    "Medellín", "Bello", "Itagüí", "Envigado", "Apartadó", "Turbo", "Rionegro", 
    "Barbosa", "Copacabana", "La Estrella", "Sabaneta", "Caldas", "Chigorodó", 
    "Girardota", "Caucasia", "Carepa", "Puerto Berrío", "Yarumal", "Sonsón", "Marinilla"
]
G.add_nodes_from(municipios)

# Añadir las aristas con sus pesos (distancias en km)
edges = [
    ("Medellín", "Bello", 10), ("Medellín", "Itagüí", 12), ("Medellín", "Envigado", 14),
    ("Medellín", "Sabaneta", 16), ("Medellín", "La Estrella", 18), ("Medellín", "Copacabana", 20),
    ("Medellín", "Barbosa", 40), ("Medellín", "Girardota", 30), ("Medellín", "Rionegro", 45),
    ("Bello", "Copacabana", 8), ("Bello", "Girardota", 25),
    ("Itagüí", "Envigado", 6), ("Itagüí", "Sabaneta", 8),
    ("Apartadó","Medellín", 294),
    ("Envigado", "Sabaneta", 5),
    ("Sabaneta", "La Estrella", 6),
    ("La Estrella", "Caldas", 15),
    ("Caldas", "Medellín", 25),
    ("Copacabana", "Girardota", 20),
    ("Girardota", "Barbosa", 15),
    ("Barbosa", "Rionegro", 35),
    ("Rionegro", "Marinilla", 20), ("Rionegro", "Sonsón", 60),
    ("Marinilla", "Sonsón", 50),
    ("Apartadó", "Turbo", 80), ("Apartadó", "Carepa", 20), ("Apartadó", "Chigorodó", 30),
    ("Turbo", "Carepa", 60),
    ("Carepa", "Chigorodó", 25),
    ("Caucasia", "Puerto Berrío", 150), ("Caucasia", "Yarumal", 120),
    ("Medellín", "Puerto Berrío", 171)
]

# Añadir las aristas al grafo
G.add_weighted_edges_from(edges)

# Dibujar el grafo
pos = nx.spring_layout(G, seed=42)  # Diseño para organizar los nodos
nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=200, font_size=10, font_weight="bold")

# Dibujar las etiquetas de las aristas (distancias)
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

# Mostrar el grafo
plt.title("Grafo de municipios de Antioquia (20 más poblados)")
plt.axis('equal')
plt.show()