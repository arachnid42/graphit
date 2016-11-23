from math import sqrt, isinf, isnan
from copy import copy
import numpy as np
from itertools import permutations

""" graph.py

    Graph module that represents a directed/undirected graph
    data structure with a support of vertex coordinates and
    edge weights (Euclidean distance or explicit value) as
    well as weights aggregation.

    The key feature of this module is key aggregation that
    allows to compose a graph on the fly while  keeping track
    on how many entries in a parsed data "mention" a particular
    edge in graph (which could correspond to a movement from one
    point to another).

    """


class NoCoordinatesPassed(Exception):
    """ Custom exception

    No coordinates passed during a vertex
    creation while they are necessary.

    """
    pass


class NotIntegerCoordinates(Exception):
    """ Custom exception

    Passed in coordinates are not of type
    integer which is not acceptable exception

    """
    pass


class GraphHasNoCoordinatesForVertices(Exception):
    """ Custom exception

    Called functionality requires graph vertices
    to have coordinates but they don't have them

    """
    pass


class BadInitParameters(Exception):
    """ Custom exception

    Passed in parameters are not of the type
    that is required

    """
    pass


class BadEdgeWeight(Exception):
    """ Custom exception

    Passed in edge weight is not an acceptable
    value

    """
    pass


class FailedToParseInputData(Exception):
    """ Custom exception

    Module has failed to import swog-like source
    from a file given

    """

    pass


class VertexNodeData(object):
    """ An optional class to hold a graph vertex data if coordinates are enabled """

    def __init__(self, label, x, y):
        """ Class instance initialization

        :param label - string vertex label
        :param x - x coordinate of a vertex
        :param y - y coordinate of a vertex

        """
        self.label = label
        self.x = x
        self.y = y


class VertexNode(object):
    """ A class to hold a graph vertex """

    def __init__(self, data):
        """ Class instance initialization

        :param data - label of a vertex if has_coordinates is
               False. Otherwise VertexNodeData object.

        """
        self.__data = data

    def get_label(self):
        """ Return a label of a vertex

        :return: string label of a vertex

        """
        if isinstance(self.__data, VertexNodeData):
            return self.__data.label
        else:
            return self.__data

    def get_coordinates(self):
        """ Return coordinates of a vertex

        :return: tuple of (x,y) coordinates of a
                 vertex if has_coordinates is True.
                 Otherwise returns None.

        """
        if isinstance(self.__data, VertexNodeData):
            return self.__data.x, self.__data.y
        else:
            return None


class EdgeNode(object):
    """ A class to hold graph edge data such as weight and reference node """

    def __init__(self, vertex_node, weight=None):
        """ Class instance initialization

        :param vertex_node - VertexNode object that holds
               a vertex that this edge is pointing to
        :param weight - weight of an edge. Defaults to None
               but can't remain None due to a class architecture.

        """
        self.vertex_node = vertex_node
        self.weight = weight

    def __str__(self):
        return "Edge to %s with weight %s" % (self.vertex_node.get_label(), str(self.weight))


class Graph(object):
    """ Graph class that keeps track over oll the graph components

    Default weight of an edge with coordinates enabled is Euclidean
    distance between respective coordinates of two vertices that the
    edge connects.

    """

    def __init__(self, directed=False, coordinates=False, explicit_weight=False, aggregate_weight=False):
        """ Init method of a class

        :param directed - bool whether a graph created is directed. Defaults to False.
        :param coordinates - bool whether graph vertices have coordinates in a 2d space.
               Defaults to False.
        :param explicit_weight - bool whether to use explicitly passed weights for edges.
               Defaults to False.
        :param aggregate_weight - bool whether aggregate edge weights when encounter the
               edge that is already present in a graph. If enabled, every time the new edge
               passed and the graph already contains this edge with a certain weight assigned
               to it, the present weight would be incremented with a weight of passed in edge
               data. Defaults to False.

        :exception BadInitParameters - raised if passed in parameters are not of type bool
        """

        # validate whether input params are booleans
        if not (isinstance(directed, bool) and isinstance(coordinates, bool) and isinstance(explicit_weight, bool) and
                    isinstance(aggregate_weight, bool)):
            raise BadInitParameters("Init parameters must be of type bool!")

        # input passed validation
        self.is_directed = directed
        self.has_coordinates = coordinates
        self.use_explicit_weight = explicit_weight
        self.aggregate_weight = aggregate_weight
        self.mapper = {}

    def add_vertex(self, label, x=None, y=None):
        """ Add a vertex to a graph

        :param label - string name of a vertex to create
        :param x - x coordinate of a vertex to create (if coordinates flag is enabled).
               If coordinates are not enabled, method ignores x's value. Defaults to None.
        :param y - y coordinate of a vertex to create (if coordinates flag is enabled).
               If coordinates are not enabled, method ignores y's value. Defaults to None.
        :exception NotIntegerCoordinates - raised if passed in vertex coordinates are not
                   of type integer.
        :exception NoCoordinatesPassed - raised when no coordinates flag is enabled and no
                   coordinates (x and y) are passed.

        :return VertexNode of a vertex inserted or None if insertion has failed.
        """

        # arguments check
        if self.has_coordinates and (x is None or y is None):
            raise NoCoordinatesPassed("No vertex coordinates passed while required!")
        if self.has_coordinates and not ((isinstance(x, int) or isinstance(x, float)) and
                                         (isinstance(y, int) or isinstance(y, float))):
            raise NotIntegerCoordinates("Vertex coordinates must be integers!")

        # if the vertex with the same label and/or coordinates
        # present in a graph, don't insert this vertex
        if self.find_vertex_node_by_label(label) or (self.find_vertex_node_by_coordinates(x, y) if
                                                     self.has_coordinates else False):
            print("Vertex with passed label/coordinates is already exist")
            return None

        # creating a vertex in a graph
        if self.has_coordinates:
            v_node = VertexNode(VertexNodeData(label, x, y))
            self.mapper[v_node] = []
            return v_node
        else:
            v_node = VertexNode(label)
            self.mapper[v_node] = []
            return v_node

    def add_edge(self, va_label, vb_label, weight=None):
        """ Add an edge between vertices A and B to a graph

        :param va_label - string label of a vertex A
        :param vb_label - string label of a vertex B
        :param weight - int weight of a vertex if
               use_explicit_weight is enabled.
               Ignored otherwise. Defaults to None.

        :return - tuple of EdgeNodes of edges if
                  at least one edge was added or
                  it's weight were incremented in
                  occasion of undirected graph.
                  If only one of two edges was added
                  the other one would be None.
                - EdgeNode of edge added or it's
                  weight was updated when graph is
                  directed.
                - None if no edges was not added
        """

        node_a = self.find_vertex_node_by_label(va_label)
        node_b = self.find_vertex_node_by_label(vb_label)
        if not node_a or not node_b:
            print("Both or one of the nodes doesn't exist in a graph! Edge is not added.")
            return None
        else:
            return self.__add_edge(node_a, node_b, weight)

    def __add_edge(self, node_a, node_b, weight):
        """ Handle backend job to add an edge between two nodes

        Counts in use_explicit_weight and aggregated_weight flags to
        add an edge and it's weight in a right way

        :param node_a - VertexNode object that holds a node A
        :param node_b - VertexNode object that holds a node B
        :param weight - weight of an edge

        :return - tuple of EdgeNodes of edges if they were added
                  or their weights were successful in occasion of
                  undirected graph.
                - EdgeNode of edge added or it's weight was updated
                  when graph is directed.
                - None if edge was not added
        """

        if self.__is_connected(node_a, node_b) and self.__is_connected(node_b, node_a):
            if self.aggregate_weight:
                edge_node = self.__get_edge(node_a, node_b)
                edge_node.weight = edge_node.weight + weight
                print("Edge was already present but it's weight was incremented")
                if not self.is_directed:
                    edge_node_b = self.__get_edge(node_b, node_a)
                    edge_node_b.weight = edge_node_b.weight + weight
                    return edge_node, edge_node_b
                return edge_node
            else:
                return None
        else:
            edge_node = EdgeNode(node_b)
            if self.use_explicit_weight:
                if isinstance(weight, int) or isinstance(weight, float):
                    edge_node.weight = weight
                else:
                    raise BadEdgeWeight("Edge weight is not a number!")
            else:
                if self.has_coordinates:
                    na_coords = node_a.get_coordinates()
                    nb_coords = node_b.get_coordinates()
                    def_weight = sqrt((na_coords[0] - nb_coords[0]) ** 2 + (na_coords[1] - nb_coords[1]) ** 2)
                    edge_node.weight = def_weight

            if not self.__is_connected(node_a, node_b):
                self.mapper[node_a].append(edge_node)
            elif self.is_directed:
                return None
            if not self.is_directed:
                if not self.__is_connected(node_b, node_a):
                    edge_node_copy = copy(edge_node)
                    edge_node_copy.vertex_node = node_a
                    self.mapper[node_b].append(edge_node_copy)
                    return edge_node, edge_node_copy
                return edge_node, None
            return edge_node

    def find_vertex_node_by_label(self, label):
        for node in self.mapper:
            if node.get_label() == label:
                return node
        return None

    def find_vertex_node_by_coordinates(self, x, y):
        """ Find VertexNode given it's coordinates if it exists

        :param x - int x coordinate
        :param y - int y coordinate

        :return VertexNode node that has coordinates (x,y). If
                there is no such node returns None.

        :exception GraphHasNoCoordinatesForVertices - method was
                   called despite a fact that this graph instance
                   doesn't store coordinates for it's vertices.
        """

        if not self.has_coordinates:
            raise GraphHasNoCoordinatesForVertices("The graph instance has vertices with no coordinates!")
        else:
            for node in self.mapper:
                coords = node.get_coordinates()
                if coords[0] == x and coords[1] == y:
                    return node
            return None

    def __is_connected(self, node_a, node_b):
        """ Backend private method for determining whether two vertices are connected

        :param node_a - VertexNode object that holds node A
        :param node_b - VertexNode object that holds node B

        :return True - nodes are connected; False - otherwise
        """

        for edge_node in self.mapper[node_a]:
            if edge_node.vertex_node == node_b:
                return True
        return False

    def __get_edge(self, node_a, node_b):
        """ Return an edge between two node object given that it exists

        :param node_a - VertexNode object that holds node A
        :param node_b - VertexNode object that holds node B

        :return: EdgeNode that connects node A and node B
        """

        for edge_node in self.mapper[node_a]:
            if edge_node.vertex_node == node_b:
                return edge_node

    def build_adjacency_matrix(self, print_out=False):
        """ Build an adjacency matrix of the graph

        :param print_out - boolean print a matrix to a console.
               Defaults to False.

        :return: NumPy matrix that represents adjacency matrix
                 of the graph
        """

        # init a matrix
        n = self.get_vertices_count()
        matrix = np.zeros(shape=(n, n))

        # prepare a list of label-index mapping
        key_list = sorted([k.get_label() for k in self.mapper])

        for vertex_node, edge_nodes in self.mapper.items():
            for edge_node in edge_nodes:
                matrix[key_list.index(vertex_node.get_label())][key_list.index(edge_node.vertex_node.get_label())] = 1

        if print_out:
            print(self.matrix_to_string(key_list, matrix))
        return matrix

    def build_2hop_matrix(self, print_out=False):
        """ Build a 2-hop matrix of the graph

       :param print_out - boolean print a matrix to a console.
              Defaults to False.

       :return: NumPy matrix that represents 2-hop matrix
                of the graph
       """

        adj_mtrx = self.build_adjacency_matrix()
        hop_mtrx = np.linalg.matrix_power(adj_mtrx, 2)

        if print_out:
            print(self.matrix_to_string(sorted([k.get_label() for k in self.mapper]), hop_mtrx))
        return hop_mtrx

    @staticmethod
    def matrix_to_string(key_list, matrix):
        """ Form a string representation of an adjacency matrix of the graph

        :param key_list - list of sorted vertex labels of the graph
        :param matrix - numpy matrix that holds adjacancy matrix of
               the graph object.

        :return: string adjacency matrix representation with labels

        """

        strg = "  "
        for label in key_list:
            strg += "%s " % label
        strg += "\n"

        for row, i in zip(matrix, key_list):
            strg += "%s " % i
            for item in row:
                if isinf(item) or isnan(item):
                    strg += "- "
                    continue
                strg += "%s " % int(item)
            strg += "\n"

        return strg

    def get_vertices_count(self):
        """ Return an amount of vertices in the graph

        :return: int amount of vertices in the graph
        """

        return len(self.mapper)

    def floyd_warshall_shortest_paths(self, print_out=False):
        """ Calculate all the shortest paths between all possible (i,j) vertices pairs

        Uses Floyd-Warshall algorithm with a fixed weight of edges equal to 1. Read more at
        https://en.wikipedia.org/wiki/Floyd%E2%80%93Warshall_algorithm

        :return tuple of NumPy matrix of shortest distances between any of two vertices and
                NumPy nxt matrix to use for a path recovery

        """

        n = self.get_vertices_count()  # getting an amount of vertices in the graph
        vert_list = sorted([k.get_label() for k in self.mapper])  # getting a list of all vertex labels
        dist = np.full((n, n), np.inf)
        nxt = np.full((n, n), np.nan)

        for vertex_node, edge_nodes in self.mapper.items():
            for edge_node in edge_nodes:
                dist[vert_list.index(vertex_node.get_label())][vert_list.index(edge_node.vertex_node.get_label())] = 1
                nxt[vert_list.index(vertex_node.get_label())][vert_list.index(edge_node.vertex_node.get_label())] = \
                    ord(edge_node.vertex_node.get_label())

        for k in range(0, n):
            for i in range(0, n):
                for j in range(0, n):
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
                        nxt[i][j] = nxt[i][k]

        if print_out:
            print(self.matrix_to_string(vert_list, dist))
            print(self.matrix_to_string(vert_list, nxt))
        return dist, nxt

    def get_shortest_path_astar(self, va_label, vb_label, trace_area=False, interactive=False):
        """ Return shortest path between two nodes that was found by A* algorithm

        :param va_label - string label of a node A
        :param vb_label - string label of a node B
        :param trace_area - bool to enable tracing of
               the amount of graph's nodes visited
        :param interactive - bool to enable verbose output
               of searching progress with pauses on every
               iteration

        :return tuple - list of vertices labels that is the
                the shortest path and integer which is an
                amount of nodes visited (if trace_area is
                enabled). Just a list with trace_area=False.
                None if not path was found.
        """

        # initialization
        vert_list = sorted([k.get_label() for k in self.mapper])  # getting a list of all vertex labels
        closed_set = []
        open_set = [va_label]
        came_from = {}
        g_score = {}
        f_score = {}

        # to store an amount of visited nodes
        visited = []

        for vert_label in vert_list:
            g_score[vert_label] = float("Inf")
            f_score[vert_label] = float("Inf")
        g_score[va_label] = 0
        f_score[va_label] = self.calculate_euclidean_distance(va_label, vb_label)

        if interactive:
            print(" * searching for a shortest path from %s to %s" % (va_label, vb_label))
            print(" * init ended. Entering main loop ...")

        # main loop
        while open_set:
            current = min({k: v for k, v in f_score.items() if k in open_set}.items(), key=lambda x: x[1])[0]
            if current not in visited:
                visited.append(current)
            if interactive:
                print(" * open_set is " + str(open_set))
                print(" * current set to %s" % current)
            if current == vb_label:
                if interactive:
                    print(" * reached target vertex. Reversing path ...")
                total_path = [current]
                while current in came_from:
                    current = came_from[current]
                    total_path.append(current)
                if trace_area:
                    return total_path[::-1], len(visited)
                else:
                    return total_path[::-1]

            open_set.remove(current)
            closed_set.append(current)
            for neighbour_label in self.get_all_neughbours_labels(current):
                if neighbour_label not in visited:
                    visited.append(neighbour_label)
                if interactive:
                    print(" * processing neighbour %s" % neighbour_label)
                if neighbour_label in closed_set:
                    if interactive:
                        print("    * already visited this node. Skipping ...")
                    continue
                tentative_g_score = g_score[current] + self.calculate_euclidean_distance(current, neighbour_label)
                if neighbour_label not in open_set:
                    open_set.append(neighbour_label)
                elif tentative_g_score >= g_score[neighbour_label]:
                    if interactive:
                        print("    * this path is worse then previously discovered. Continuing ...")
                    continue

                came_from[neighbour_label] = current
                g_score[neighbour_label] = tentative_g_score
                f_score[neighbour_label] = g_score[neighbour_label] + self.calculate_euclidean_distance(neighbour_label,
                                                                                                        vb_label)
                if interactive:
                    print("    * the path to %s has f_score %f" % (neighbour_label, f_score[neighbour_label]))

            if interactive:
                input()
        # no path found
        return None

    def calculate_euclidean_distance(self, va_label, vb_label):
        """ Calculate Euclidean distance between vertices if coordinates was enabled

        :param va_label - string label of a node A
        :param vb_label - string label of a node B
        :return: float distance between A and B if
                 coordinates was enabled. Otherwise
                 None.
        """

        if not self.has_coordinates:
            return None

        a_coords = self.find_vertex_node_by_label(va_label).get_coordinates()
        b_coords = self.find_vertex_node_by_label(vb_label).get_coordinates()
        return sqrt((a_coords[0] - b_coords[0]) ** 2 + (a_coords[1] - b_coords[1]) ** 2)

    def get_shortest_path(self, va_label, vb_label, nxt):
        """ Return a shortest path between two nodes using a next matrix from the floyd_warshall_shortest_paths()

        :param va_label - string label of a node A
        :param vb_label - string label of a node B
        :param nxt - NumPy array from floyd_warshall_shortest_paths()

        :return list of labels that indicate the shortest path between
                A and B. Return empty list if there is no path.

        """

        vert_list = sorted([k.get_label() for k in self.mapper])  # getting a list of all vertex labels
        if isnan(nxt[vert_list.index(va_label)][vert_list.index(vb_label)]):
            return []
        path = [va_label]
        while va_label != vb_label:
            va_label = chr(int(nxt[vert_list.index(va_label)][vert_list.index(vb_label)]))
            path.append(va_label)
        return path

    def calculate_betweenness_of_vertices(self, nxt):
        """ Calculate a betweenness for every graph's vertex

        :param nxt - NumPy array from floyd_warshall_shortest_paths()

        :return dictionary of betweenness values for each vertex (where
                vertex label is a key and it's betweenness is a value)

        """

        vert_list = sorted([k.get_label() for k in self.mapper])  # getting a list of all vertex labels
        shortest_paths = self.get_all_shortest_paths(nxt)

        # dictionary to hold a betweenness for avery vertex
        vert_betweenness = {}

        for vert in vert_list:
            btwns = 0
            for path in shortest_paths:
                if vert in path:
                    btwns += 1
            if not self.is_directed:
                btwns //= 2
            vert_betweenness[vert] = btwns

        return vert_betweenness

    def get_all_shortest_paths(self, nxt):
        """ Get all shortest paths between all the possible vertex pairs

        :param nxt - NumPy array from floyd_warshall_shortest_paths()

        :return list of all shortest paths between all the possible
                vertex pairs

        """

        vert_list = sorted([k.get_label() for k in self.mapper])  # getting a list of all vertex labels
        shortest_paths = []
        for vertex_pair in permutations(vert_list, 2):
            shortest_paths.append(self.get_shortest_path(vertex_pair[0], vertex_pair[1], nxt))

        return shortest_paths

    def build_transitive_closure(self, adj_mtx, print_out=False):
        """ TODO: docs """

        n = self.get_vertices_count()
        for i in range(0, n):
            for s in range(0, n):
                for t in range(0, n):
                    if adj_mtx[s][i] and adj_mtx[i][t]:
                        adj_mtx[s][t] = 1

        if print_out:
            print(self.matrix_to_string(sorted([k.get_label() for k in self.mapper]), adj_mtx))
        return adj_mtx

    def get_all_neughbours_labels(self, vert_label):
        """ Return a list of all neighbours of the input vertex

        :param vert_label: label of vertex

        :return: list of vertex's neighbours labels
        """

        lst = []
        for edge_node in self.mapper[self.find_vertex_node_by_label(vert_label)]:
            lst.append(edge_node.vertex_node.get_label())

        return lst

    def get_edge_weight(self, va_label, vb_label):
        """ Get a weight of an edge that connects nodes A and B

        :param va_label - string label of a node A
        :param vb_label - string label of a node B

        :return: float weight of an edge that connects
                 nodes A nad B
        """

        a_node = self.find_vertex_node_by_label(va_label)
        edge_node = [v for v in self.mapper[a_node] if v.vertex_node.get_label() == vb_label][0]

        return edge_node.weight

    def init_with_swog_like_source(self, str_file):
        """ Initialize graph with data like in data/graph1.txt

        :param str_file: path to file
        """

        with open(str_file) as f:
            for line in f:
                if line[0] == "#" or not line:
                    continue
                data_list = line.split()
                if len(data_list) == 3:
                    self.add_vertex(data_list[0], int(data_list[1]), int(data_list[2]))
                elif len(data_list) == 4:
                    self.add_edge(data_list[0], data_list[1])
                else:
                    raise FailedToParseInputData("Failed to parse the input data")

    def __str__(self):

        stats = "# stats\nvertices: " + str(len(self.mapper)) + "\n"
        vertices = "# vertices\n"
        edges = "# edges\n"

        # variable to hold edges count
        edges_count = 0

        for vertex_node in self.mapper:
            vertices += str(vertex_node.get_label()) + "\t" + str(vertex_node.get_coordinates()) + "\n"

        for vertex_node, edge_nodes in self.mapper.items():
            for edge_node in edge_nodes:
                edges_count += 1
                edges += str(vertex_node.get_label()) + "\t" + str(edge_node.vertex_node.get_label()) + "\t" + \
                         str(edge_node.weight) + "\n"

        if not self.is_directed:
            edges_count //= 2

        stats += "edges: " + str(edges_count) + "\n"
        return "%s\n%s\n%s" % (vertices, edges, stats)
