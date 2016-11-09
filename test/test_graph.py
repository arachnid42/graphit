import unittest
from app.dstruct.graph import *


class TestGraph(unittest.TestCase):
    """ Unit tests for graph.py module """

    def test_init(self):
        """ Test Graph __init__ behaviour when wrong type of arguments passed """

        self.assertRaises(BadInitParameters, Graph, directed="33")
        self.assertRaises(BadInitParameters, Graph, coordinates="33")
        self.assertRaises(BadInitParameters, Graph, explicit_weight="33")
        self.assertRaises(BadInitParameters, Graph, aggregate_weight="33")

        self.assertRaises(BadInitParameters, Graph, directed=1)
        self.assertRaises(BadInitParameters, Graph, coordinates=1)
        self.assertRaises(BadInitParameters, Graph, explicit_weight=1)
        self.assertRaises(BadInitParameters, Graph, aggregate_weight=1)

        self.assertRaises(BadInitParameters, Graph, directed=1, coordinates=1)
        self.assertRaises(BadInitParameters, Graph, directed=True, coordinates=1)
        self.assertRaises(BadInitParameters, Graph, directed=True, coordinates=1, explicit_weight=True)
        self.assertRaises(BadInitParameters, Graph, directed=1, coordinates=True, explicit_weight="33")

    def test_add_vertex(self):
        """ Test addition of vertices to a graph """

        # test addition of simple vertices to unweighted,
        # undirected graph without vertex coordinates
        graph = Graph()
        graph.add_vertex("boom!")
        graph.add_vertex("dums!")
        graph.add_vertex("shmyak!")
        self.assertEqual(len(graph.mapper), 3)
        graph.add_vertex("shmyak!")
        self.assertEqual(len(graph.mapper), 3)
        del graph

        # test addition of vertices with coordinates to
        # unweighted, undirected graph
        graph = Graph(coordinates=True)
        v_node = graph.add_vertex("boom!", 1, 2)
        self.assertEqual(v_node.get_coordinates(), (1, 2))
        graph.add_vertex("dums!", 3, 4)
        graph.add_vertex("shmyak!", 5, 6)
        self.assertEqual(len(graph.mapper), 3)
        graph.add_vertex("shmyak!", 5, 6)
        self.assertEqual(len(graph.mapper), 3)
        graph.add_vertex("hey", 5, 6)
        self.assertEqual(len(graph.mapper), 3)
        self.assertRaises(NotIntegerCoordinates, graph.add_vertex, "whay!", "one", "two")
        self.assertRaises(NotIntegerCoordinates, graph.add_vertex, "whay!", 1, "two")
        self.assertRaises(NotIntegerCoordinates, graph.add_vertex, "whay!", "one", 2)
        self.assertRaises(NoCoordinatesPassed, graph.add_vertex, "whay!")

    def test_add_edge(self):
        """ Testing addition of edges to a graph """

        # test addition of edges to unweighted,
        # undirected graph without vertex coordinates
        graph = Graph()
        self.assertEqual(graph.add_edge("A", "B"), None)
        node_a = graph.add_vertex("A")
        node_b = graph.add_vertex("B")
        self.assertTrue(graph.add_edge("A", "B") is not None)
        self.assertEqual(graph.mapper[node_a][0].vertex_node == node_b, True)
        self.assertEqual(graph.mapper[node_b][0].vertex_node == node_a, True)

    # def test_get_vertices_count(self):
    #     """ Test getter for an amount of vertices in a graph """
    #
    #     graph = Graph()
    #     graph.add_vertex("boom!")
    #     graph.add_vertex("dums!")
    #     graph.add_vertex("shmyak!")
