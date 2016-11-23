from datetime import datetime
from app.dstruct.graph import *


class NonpositiveMaxCoordinates(Exception):
    """ Custom exception

    Indicates that passed in to a Facility constructor max
    coordinates are nonpositive, which is unacceptable

    """
    pass


class WrongTypeOfMaxCoordinates(Exception):
    """ Custom exception

    Indicates that passed in to a Facility constructor max
    coordinates are not both of type integer/float

    """
    pass


class NotIntQuantity(Exception):
    """ Custom exception

    Passed in quantity parameter is nat an integer

    """


class BadTimeFormat(Exception):
    """ Custom exception

    Passed in time is not of the format required

    """


class TransportationInsertionFailed(Exception):
    """ Custom exception

    Transportation record was not inserted
    (input data is valid)

    """


class DepartmentNotExist(Exception):
    """ Custom exception

    Departments involved in transportation
    record insertion don't exist (one or
    both).

    """


class DepartmentGraph(Graph):
    """ Class-wrapper to simplify department-graph mapping """

    def __init__(self):
        """ Constructor to initialize all the necessary fields """
        super(DepartmentGraph, self).__init__(coordinates=True, explicit_weight=True, aggregate_weight=True)
        self.departments = []
        self.transp_time = {}  # map transportations (graph edges) and time when it happened

    def add_department(self, department):
        """ Load new department into a graph

        :param department - instance of a Department
               class that stores information about
               particular factory department

        """
        if self.add_vertex(department.label, department.centroid.x, department.centroid.y):
            self.departments.append(department)
            return True
        else:
            return False

    def add_transp_record(self, src_label, dest_label, quant, time):
        """ Add a transportation record

        Add a record about transportation (movement)
        of a particular quantity of items on a factory
        floor.

        :param src_label - string label of a source department
        :param dest_label - string label of a destination department
        :param quant - int quantity of items transported
        :param time - datetime object that holds a time when a
             transportation happened

        :return True - transportation record was inserted successfully.
                Otherwise raises exception.

        """

        if self.find_vertex_node_by_label(src_label) and self.find_vertex_node_by_label(dest_label):
            edge = self.add_edge(src_label, dest_label, quant)
            if edge:
                self.transp_time[edge] = time
            else:
                raise TransportationInsertionFailed
        else:
            raise DepartmentNotExist


class Facility(object):
    """ Class to represent the whole factory layout

    The layout is located in the first quarter of a
    cartesian coordinate system

    """

    def __init__(self, max_x, max_y):
        """ Facility instance constructor

        :param max_x - float/int maximum allowed x in the
               layout representation
        :param max_y - float/int maximum allowed y in the
               layout representation

        """

        if (isinstance(max_x, int) and isinstance(max_y, int)) or \
                (isinstance(max_x, float) and isinstance(max_y, float)):
            if max_x > 0 and max_y > 0:
                self.max_x = max_x
                self.max_y = max_y
                self.d_graph = DepartmentGraph()
            else:
                raise NonpositiveMaxCoordinates("facility max_x and max_y must be positive!")
        else:
            raise WrongTypeOfMaxCoordinates("facility max_x and max_y must be both integers or both floats!")

    def add_department(self, department):
        """ Add department to a facility instance

        :param department - instance of a Department
               class that stores information about
               particular factory department

        :return True - department was inserted successfully.
                False - otherwise.

        """
        if self.fits_boundary(department):
            return self.d_graph.add_department(department)

    def fits_boundary(self, department):
        """ Check whether all points of a department fall into facility boundary (canvas)

        :param department - instance of a Department
               class that stores information about
               particular factory department

        :return True - department fits boundary and
                can be added. False - otherwise

        """

        for p in department.point2d_vector:
            if not (p.x <= self.max_x and p.y <= self.max_y):
                print("Some of department points are out of facility boundary!")
                return False
        return True

    def add_transp_record(self, src_label, dest_label, quant, time):
        """ Add a transportation record

        Add a record about transportation (movement)
        of a particular quantity of items on a factory
        floor.

        :param src_label - string label of a source department
        :param dest_label - string label of a destination department
        :param quant - int quantity of items transported
        :param time - string date and time when transportation happened
               i.e. 2015-05-25 18:00:00

        :return True - transportation record was inserted successfully.
                False - otherwise.

        """

        if not isinstance(quant, int):
            raise NotIntQuantity

        try:
            dt = datetime.strptime(time, "%Y-%m-%d %X")  # example: 2015-05-25 18:00:00
        except ValueError:
            raise BadTimeFormat("Transportation time parsing failed!")

        return self.d_graph.add_transp_record(src_label, dest_label, quant, dt)

