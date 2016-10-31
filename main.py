#!/usr/bin/env python3

from graph import Graph

# creating an undirected graph with vertices coordinates instance
graph1 = Graph(directed=False, coordinates=True)

# parse an input file and create a graph
with open("data/graph1.txt") as f:
    for line in f:
        if line[0] == "#":
            continue
        data_list = line.split()
        if len(data_list) == 3:
            graph1.add_vertex(data_list[0], int(data_list[1]), int(data_list[2]))
        elif len(data_list) == 4:
            print(data_list)
            graph1.add_edge(data_list[0], data_list[1])
        else:
            raise Exception("Something terrible has happened!")

# print a result graph
print(graph1)
