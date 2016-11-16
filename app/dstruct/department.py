from app.dstruct.point2d import *
from math import fabs


class BadInitParameters(Exception):
    """ Custom exception

    Indicates about bad passed in parameters to a
    Department constructor (__init__()). Typical
    reasons are less then 3 points passed or points
    passed are not Point2D instances.

    """
    pass


class Department(object):
    def __init__(self, label, *arg):
        """ Constructor

        :param label - String label of a department
        :param *arg - tuple of Point2D objects in an
               ordered way, i.e. to represent a polygon
               points one by one counter-clockwise.

        """

        if len(arg) > 2 and self.__verify_points(arg):
            self.label = label
            self.point2d_vector = arg
            self.area = self.calculate_area()
            self.centroid = self.calculate_centroid()
        else:
            raise BadInitParameters("passed init parameters are not acceptable!")

    @staticmethod
    def __verify_points(p_tuple):
        """ Make sure all items in a tuple are Point2D objects

        :param p_tuple - tuple to verify

        :return bool True - all the items in p_tuple are Point2D
                objects. False otherwise.

        """
        for p in p_tuple:
            if not isinstance(p, Point2D):
                return False
        return True

    def calculate_centroid(self):
        """ Calculate a centroid (center) point of the department

        :return Point2D that holds a center point of the department

        """
        c_x = c_y = 0
        for p_ind in range(0, len(self.point2d_vector)-1):
            p_i = self.point2d_vector[p_ind]
            p_i_next = self.point2d_vector[(p_ind + 1) % len(self.point2d_vector)]
            c_x += (p_i.x + p_i_next.x) * (p_i.x * p_i_next.y - p_i_next.x * p_i.y)
            c_y += (p_i.y + p_i_next.y) * (p_i.x * p_i_next.y - p_i_next.x * p_i.y)

        return Point2D(c_x/(6*self.area), c_y/(6*self.area))

    def calculate_area(self):
        """ Calculate an area of the department

        :return float area of the department

        """
        d_area = 0
        for p_ind in range(0, len(self.point2d_vector)):
            p_i = self.point2d_vector[p_ind]
            p_ip1 = self.point2d_vector[(p_ind + 1) % len(self.point2d_vector)]
            d_area += p_i.x * p_ip1.y - p_ip1.x * p_i.y

        return fabs(d_area) / 2

    def __str__(self):
        strg = "Department: %s\n-------------------------\n" % self.label
        for point in self.point2d_vector:
            strg += str(point) + "\n"

        return strg + "\n"
