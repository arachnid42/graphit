from app.dstruct.graph import *
from app.dstruct.department import *


class NonpositiveMaxCoordinates(Exception):
    """ Custom exception

    Indicates that passed in to a Facility constructor max
    coordinates are nonpositive, which is unacceptable.

    """
    pass


class WrongTypeOfMaxCoordinates(Exception):
    """ Custom exception

    Indicates that passed in to a Facility constructor max
    coordinates are not both of type integer/float.

    """
    pass


class DepartmentGraph(Graph):
    """ Class-wrapper to simplify department-graph mapping """

    def __init__(self):
        """ Constructor to initialize all the necessary fields """
        super(DepartmentGraph, self).__init__(coordinates=True, explicit_weight=True, aggregate_weight=True)
        self.departments = []

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
                self.dgraph = DepartmentGraph()
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
            return self.dgraph.add_department(department)

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
                return False
        return True
