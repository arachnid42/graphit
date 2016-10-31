from exceptions import *


class GraphNodeData(object):

    def __init__(self, label, x, y):
        self.label = label
        self.x = x
        self.y = y


class GraphNode(object):

    def __init__(self, data):
        self.__data = data

    def get_label(self):
        if isinstance(self.__data, GraphNodeData):
            return self.__data.label
        else:
            return self.__data

    def get_coordinates(self):
        if isinstance(self.__data, GraphNodeData):
            return self.__data.x, self.__data.y
        else:
            return None


class Graph(object):

    def __init__(self, directed=False, coords=True):
        self.is_directed = directed
        self.has_coordinates = coords
        self.mapper = {}

    def add_vertex(self, label, x=None, y=None):

        # if the vertex with the same label and/or coordinates
        # present in a graph, don't insert this vertex
        if self.find_vertex_by_label(label) or self.find_vertex_by_coordinates(x, y):
            return False

        # validation of vertex data is passed
        # creating a vertex in a graph
        if self.has_coordinates:
            if x is not None and y is not None:
                if isinstance(x, int) and isinstance(y, int):
                    self.mapper[GraphNode(GraphNodeData(label, x, y))] = []
                    return True
                else:
                    raise NotIntegerCoordinates("Vertex coordinates must be integers!")
            else:
                raise NoCoordinatesPassed("No vertex coordinates passed while required!")
        else:
            self.mapper[GraphNode(label)] = []
            return True

    def find_vertex_by_label(self, label):
        for node in self.mapper:
            if node.get_label() == label:
                return node
        return None

    def find_vertex_by_coordinates(self, x, y):
        if not self.has_coordinates:
            raise GraphHasNoCoordinatesForVertices("The graph instance has vertices with no coordinates!")
        else:
            for node in self.mapper:
                coords = node.get_coordinates()
                if coords[0] == x and coords[1] == y:
                    return node
