from exceptions import *


class VertexNodeData(object):
    """ An optional class to hold a graph vertex data if coordinates are enabled """

    def __init__(self, label, x, y):
        self.label = label
        self.x = x
        self.y = y


class VertexNode(object):
    """ A class to hold a graph vertex """

    def __init__(self, data):
        self.__data = data

    def get_label(self):
        if isinstance(self.__data, VertexNodeData):
            return self.__data.label
        else:
            return self.__data

    def get_coordinates(self):
        if isinstance(self.__data, VertexNodeData):
            return self.__data.x, self.__data.y
        else:
            return None


class EdgeNode(object):
    """ A class to hold graph edge data such as weight and reference node """

    def __init__(self, node, weight):
        self.node = node
        self.weight = weight


class Graph(object):
    """ Graph class that keeps track over oll the graph components """

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
        """

        # if the vertex with the same label and/or coordinates
        # present in a graph, don't insert this vertex
        if self.find_vertex_node_by_label(label) or self.find_vertex_node_by_coordinates(x, y):
            print("Vertex with passed label/coordinates is already exist")
            return False

        # validation of vertex data is passed
        # creating a vertex in a graph
        if self.has_coordinates:
            if x is not None and y is not None:
                if isinstance(x, int) and isinstance(y, int):
                    self.mapper[VertexNode(VertexNodeData(label, x, y))] = []
                    return True
                else:
                    raise NotIntegerCoordinates("Vertex coordinates must be integers!")
            else:
                raise NoCoordinatesPassed("No vertex coordinates passed while required!")
        else:
            self.mapper[VertexNode(label)] = []
            return True

    def add_edge(self, va_label, vb_label):
        node_a = self.find_vertex_node_by_label(va_label)
        node_b = self.find_vertex_node_by_label(vb_label)
        if not node_a or not node_b:
            print("Both or one of the nodes doesn't exist in a graph! Edge is not added.")
            return False
        else:
            if not self.__is_connected(node_a, node_b):
                self.mapper[node_a].append(node_b)
            if not self.is_directed:
                if not self.__is_connected(node_b, node_a):
                    self.mapper[node_b].append(node_a)
            return True

    def find_vertex_node_by_label(self, label):
        for node in self.mapper:
            if node.get_label() == label:
                return node
        return None

    def find_vertex_node_by_coordinates(self, x, y):
        if not self.has_coordinates:
            raise GraphHasNoCoordinatesForVertices("The graph instance has vertices with no coordinates!")
        else:
            for node in self.mapper:
                coords = node.get_coordinates()
                if coords[0] == x and coords[1] == y:
                    return node

    def __is_connected(self, node_a, node_b):
        """ Backend private method for determining whether two vertices are connected

        :param node_a - VertexNode object that holds first node
        :param node_b - VertexNode object that holds second node

        :return True - nodes are connected; False - otherwise
        """

        if node_b in self.mapper[node_a]:
            return True
        return False

    def __str__(self):

        stats = "# stats\nvertices: " + str(len(self.mapper)) + "\n"
        vertices = "# vertices\n"
        edges = "# edges\n"

        # variable to hold edges count
        edges_count = 0

        for node in self.mapper:
            vertices += str(node.get_label()) + "\t" + str(node.get_coordinates()) + "\n"

        for node, neighbours in self.mapper.items():
            for neighbour in neighbours:
                edges_count += 1
                edges += str(node.get_label()) + "\t" + str(neighbour.get_label()) + "\n"

        if not self.is_directed:
            edges_count //= 2

        stats += "edges: " + str(edges_count) + "\n"
        return "%s\n%s\n%s" % (vertices, edges, stats)
