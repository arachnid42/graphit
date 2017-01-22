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


class DepartmentNotAdded(Exception):
    """ Custom exception

    Some of department points were not added
    so overall insertion process failed

    """


class DepartmentNotExist(Exception):
    """ Custom exception

    Departments involved in transportation
    record insertion don't exist (one or
    both).

    """


class TransportationGraph(Graph):
    """ Class-wrapper to simplify department-graph mapping """

    def __init__(self):
        """ Constructor to initialize all the necessary fields """
        super(TransportationGraph, self).__init__(coordinates=True, explicit_weight=True, aggregate_weight=True)
        self.departments = []
        # map transportation (graph edges, weight appended and time when it happened)
        # to be able to filter not aggregated transportation records by date
        self.transp_time = {}

    def add_department(self, department):
        """ Load new department vertices into a graph

        :param department - instance of a Department
               class that stores information about
               particular factory department

        """

        inserted_count = 0
        for vertex_label, vertex_point in department.vertices.items():
            # adding separate department vertices with <department_label>.<department_vertex_label> labels
            if self.add_vertex("%s.%s" % (department.label, vertex_label), vertex_point.x, vertex_point.y):
                inserted_count += 1
        if not inserted_count == len(department.vertices):
            raise DepartmentNotAdded("department was not added!")
        else:
            self.departments.append(department)

    def add_transp_record(self, src_label, dest_label, quant, time):
        """ Add a transportation record

        Add a record about transportation (movement)
        of a particular quantity of items on a factory
        floor.

        :param src_label - string label of a source department point
               in a format <department_label>.<department_vertex_label>
        :param dest_label - string label of a destination department
               point in the same format as above
        :param quant - int quantity of items transported
        :param time - datetime object that holds a time when a
               transportation happened
        :raises NodeNotExists, SelfEdgesNotSupported
        """

        edge = self.add_edge(src_label, dest_label, quant)
        self.transp_time[edge] = [quant, time]


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

        if (isinstance(max_x, int) or isinstance(max_x, float)) and \
                (isinstance(max_y, int) or isinstance(max_y, float)):
            if max_x > 0 and max_y > 0:
                self.max_x = float(max_x)
                self.max_y = float(max_y)
                self.d_graph = TransportationGraph()
            else:
                raise NonpositiveMaxCoordinates("facility max_x and max_y must be positive!")
        else:
            raise WrongTypeOfMaxCoordinates("facility max_x and max_y must be integers or floats!")

    def add_department(self, department):
        """ Add department to a facility instance

        :param department - instance of a Department
               class that stores information about
               particular factory department

        :return True - department was inserted successfully.
                False - otherwise.

        """
        if self.__fits_boundary(department):
            self.d_graph.add_department(department)
            return True
        else:
            return False

    def get_department_by_label(self, label):
        """ Get facility department by it's label

        :return: Department class instance matching
                 the label passed in as a parameter

        """

        return [dep for dep in self.d_graph.departments if dep.label == label][0]

    def get_departments(self):
        """ Get all departments of a facility

        :return: list of Department objects

        """

        return self.d_graph.departments

    def __fits_boundary(self, department):
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

        :param src_label - string label of a source department point
               in a format <department_label>.<department_vertex_label>
        :param dest_label - string label of a destination department
               point in the same format as above
        :param quant - int quantity of items transported
        :param time - string date and time when transportation happened
               i.e. 2015-05-25 18:00:00

        """

        if not isinstance(quant, int):
            raise NotIntQuantity

        try:
            dt = datetime.strptime(time, "%Y-%m-%d %X")  # example: 2015-05-25 18:00:00
        except ValueError:
            raise BadTimeFormat("Transportation time parsing failed!")
        self.d_graph.add_transp_record(src_label, dest_label, quant, dt)  # raises errors on failure
