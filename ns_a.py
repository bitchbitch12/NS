# -*- coding: utf-8 -*-
"""Copy of NS - 3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1oYV1X1_6pMcr8WSBrmqSYAE2Q84m0Z_l
"""

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
from random import randint
import math
from collections import defaultdict

df = pd.read_csv(
    "/content/drive/MyDrive/sem-9/NS/facebook_combined.txt.gz",
    compression="gzip",
    sep=" ",
    names=["start_node", "end_node"],
)

df

G = nx.from_pandas_edgelist(df, "start_node", "end_node")

pos = nx.spring_layout(G, iterations=15, seed=1721)
fig, ax = plt.subplots(figsize=(15, 9))
ax.axis("off")
plot_options = {"node_size": 10, "with_labels": False, "width": 0.15}
nx.draw_networkx(G, pos=pos, ax=ax, **plot_options)

G.number_of_nodes()

G.number_of_edges()

nx.degree_centrality(G)

nx.average_clustering(G)

def clustering_coefficient(G):
  nodes, edges = G.nodes(), G.edges()
  neighbors = defaultdict(list)
  for i in edges:
    neighbors[i[0]].append(i[1])
    neighbors[i[1]].append(i[0])
  coefficients = dict.fromkeys(neighbors, 0)
  for value in neighbors.items():
    for i in range(len(value[1])):
      for j in range(i):
        if ((value[1][i], value[1][j]) in edges) or ((value[1][j], value[1][i]) in edges):
          coefficients[value[0]] += 1

    if coefficients[value[0]] != 0:
      coefficients[value[0]] /= math.comb(len(value[1]), 2)

  return coefficients

result = clustering_coefficient(G)
result

nx.average_shortest_path_length(G)

def shortest_path(graph, node1, node2):
    path_list = [[node1]]
    path_index = 0
    previous_nodes = {node1}
    if node1 == node2:
        return path_list[0]
    while path_index < len(path_list):
        current_path = path_list[path_index]

        last_node = current_path[-1]
        next_nodes = graph[last_node]
        if node2 in next_nodes:
            current_path.append(node2)
            return current_path
        for next_node in next_nodes:
            if not next_node in previous_nodes:
                new_path = current_path[:]
                new_path.append(next_node)
                path_list.append(new_path)
                previous_nodes.add(next_node)
        path_index += 1
    return []

nodes = list(G.nodes())
cnt = 0
tot_pl = 0
avg_path_length = 0
for i in range(len(nodes)):
  for j in range(i):
    print(i, end = "->")
    print(j, end = ":")
    val = shortest_path(G, nodes[i], nodes[j])
    print(val)
    tot_pl += len(val) - 1
    cnt += 1

print("Average Path length for Graph G: ", tot_pl/cnt)

pl = nx.average_shortest_path_length(G)
print(pl)

l = math.log(G.number_of_nodes())/math.log(pl)
l

"""## random graph"""

rg = nx.gnp_random_graph(4039, 0.11, seed = 5)

rg.number_of_edges()

pos = nx.spring_layout(rg, iterations=15, seed=1721)
fig, ax = plt.subplots(figsize=(15, 9))
ax.axis("off")
plot_options = {"node_size": 10, "with_labels": False, "width": 0.15}
nx.draw_networkx(rg, pos=pos, ax=ax, **plot_options)

nx.degree_centrality(rg)

nx.average_clustering(rg)

result = clustering_coefficient(rg)
result

rg_pl = nx.average_shortest_path_length(rg)
print(rg_pl)

rg_l = math.log(rg.number_of_nodes())/math.log(rg_pl)
rg_l

"""## random graph 2"""

rg2 = nx.gnp_random_graph(4039, 0.1, seed = 5)

rg2.number_of_edges()

result = clustering_coefficient(rg2)
result

rg_pl2 = nx.average_shortest_path_length(rg2)
print(rg_pl2)

rg_l2 = math.log(rg2.number_of_nodes())/math.log(rg_pl2)
rg_l2

"""##Metrics"""



import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import math
from collections import defaultdict

G = nx.gnp_random_graph(10, 0.7, seed = 5)

G.degree()

degree_sequence = sorted((d for n, d in G.degree()), reverse=True)
dmax = max(degree_sequence)

fig = plt.figure("Degree of a random graph", figsize=(8, 8))
# Create a gridspec for adding subplots of different sizes
axgrid = fig.add_gridspec(5, 4)

ax0 = fig.add_subplot(axgrid[0:3, :])
Gcc = G.subgraph(sorted(nx.connected_components(G), key=len, reverse=True)[0])
pos = nx.spring_layout(Gcc, seed=10396953)
nx.draw_networkx_nodes(Gcc, pos, ax=ax0, node_size=20)
nx.draw_networkx_edges(Gcc, pos, ax=ax0, alpha=0.4)
ax0.set_title("Connected components of G")
ax0.set_axis_off()

"""## Degree distribution"""

deg = dict(G.degree())

tot = 0
for i in deg:
  tot += deg[i]

tot

nodes = []
degree = []
for i in deg:
  nodes.append(i)
  degree.append(deg[i]/tot)

deg

nodes

degree

sns.barplot(x = nodes, y = degree)

"""## clustering coefficient"""

def clustering_coefficient(G):
  nodes, edges = G.nodes(), G.edges()
  neighbors = defaultdict(list)
  for i in edges:
    neighbors[i[0]].append(i[1])
    neighbors[i[1]].append(i[0])

  coefficients = dict.fromkeys(neighbors, 0)
  for value in neighbors.items():
    for i in range(len(value[1])):
      for j in range(i):
        if ((value[1][i], value[1][j]) in edges) or ((value[1][j], value[1][i]) in edges):
          coefficients[value[0]] += 1

    if coefficients[value[0]] != 0:
      coefficients[value[0]] /= math.comb(len(value[1]), 2)

  return coefficients

result = clustering_coefficient(G)
result

nodes = list(result.keys())
value = list(result.values())

fig = plt.figure(figsize = (10, 5))
plt.bar(nodes, value, width = 0.4)

plt.xlabel("Nodes")
plt.ylabel("Value")
plt.title("CLUSTERING COEFFICIENT")
plt.show()

"""## Average path length"""

print(nx.average_shortest_path_length(G))

print(nx.adjacency_matrix(G))

def shortest_path(graph, node1, node2):
    path_list = [[node1]]
    path_index = 0
    previous_nodes = {node1}
    if node1 == node2:
        return path_list[0]
    while path_index < len(path_list):
        current_path = path_list[path_index]

        last_node = current_path[-1]
        next_nodes = graph[last_node]
        if node2 in next_nodes:
            current_path.append(node2)
            return current_path
        for next_node in next_nodes:
            if not next_node in previous_nodes:
                new_path = current_path[:]
                new_path.append(next_node)
                path_list.append(new_path)
                previous_nodes.add(next_node)
        path_index += 1
    return []

nodes = list(G.nodes())
cnt = 0
tot_pl = 0
avg_path_length = 0
for i in range(len(nodes)):
  for j in range(i):
    print(i, end = "->")
    print(j, end = ":")
    val = shortest_path(G, nodes[i], nodes[j])
    print(val)
    tot_pl += len(val) - 1
    cnt += 1

print("Average Path length for Graph G: ", tot_pl/cnt)

class Node:
  def __init__(self, data):
    self.data = data
    self.ptr = None
class slinkedlist:
  def __init__(self):
    self.head = None
  def insert_beg(self, ndata):
    n = Node(ndata)
    n.ptr = self.head
    self.head = n
  def insert_end(self, ndata):
    nnode = Node(ndata)
    if self.head is None:
      self.head = nnode
      return
    last = self.head
    while last.ptr:
      last = last.ptr
    last.ptr = nnode
  def traversal(self):
    x = self.head
    while x is not None:
      print(x.data, end = "")
      print("->", end = "")
      x = x.ptr

s = slinkedlist()
s.head = Node(1)
o2 = Node(2)
s.head.ptr = o2
o2.ptr = Node(3)
s.traversal()
s.insert_beg(0)
print("\n")
s.traversal()
s.insert_end(4)
print("\n")
s.traversal()