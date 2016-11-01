#!/usr/bin/env python3

from graph import Graph
import numpy as np

# creating an undirected graph with vertices coordinates instance
graph1 = Graph(coordinates=True, directed=False)

# parse an input file and create a graph
with open("data/graph1.txt") as f:
    for line in f:
        if line[0] == "#" or not line:
            continue
        data_list = line.split()
        if len(data_list) == 3:
            graph1.add_vertex(data_list[0], int(data_list[1]), int(data_list[2]))
        elif len(data_list) == 4:
            graph1.add_edge(data_list[0], data_list[1])
        else:
            raise Exception("Something terrible has happened!")

# print(graph1)
# print("# adjacency matrix")
# graph1.build_adjacency_matrix(print_out=True)
# print("\n# 2-hop matrix")
# graph1.build_2hop_matrix(print_out=True)

dist_mtrx = graph1.floyd_warshall_shortest_paths(print_out=True)

dist_mtrx[dist_mtrx == np.inf] = 0
print("The graph diameter is %i" % int(dist_mtrx.max()))
