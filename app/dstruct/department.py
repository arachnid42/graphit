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


class NotPoint2DObject(Exception):
    """ Custom exception

    Indicates about the fact that passed in parameters
    are not instances of Point2D class

    """


class SomeValuesWereOverrided(Exception):
    """ Custom exception

    Some values of self.vertices were overrided
    by a new data which should not happen ever

    """


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
            self.point2d_vector = arg  # physical measurements of department boundaries
            self.area = self.calculate_area()
            self.centroid = self.calculate_centroid()
            self.vertices = {"centroid": self.centroid}  # all vertices to be used as graph points
        else:
            raise BadInitParameters("passed init parameters are not acceptable!")

    def add_vertices(self, vertices):
        """ Add vertices to be used as graph points

        :param vertices: dictionary of keys that are unique
               labels of points and values are Point2D objects.
        :return: True - all vertices was added successfully.
                 False - otherwise.

        """

        # TODO: rewrite with ray casting stuff
        if not self.__verify_points(vertices.values()):
            raise NotPoint2DObject
        # else:
        #     try:
        #         previous_len = len(self.vertices)
        #         self.vertices.update(vertices)  # updates value if key exists; otherwise adds key-value
        #         if len(self.vertices) == previous_len + len(vertices):
        #             return True
        #         else:
        #             raise SomeValuesWereOverrided
        #     except:
        #         return False  # something completely went wrong

    def __fits_boundary(self, point):
        """ Checks whether a Point2D object lays in department boundary

        Implemented as a ray casting algorithm (https://en.wikipedia.org/wiki/Ray_casting)

        :param point - Point2D object to check
        :return True - point is in department boundary. False - otherwise.

        """

        intersection_count = 0  # how many times ray intersects polygon sides
        for i in range(len(self.point2d_vector)):
            p_i = self.point2d_vector[i]
            p_i_next = self.point2d_vector[(i+1) % len(self.point2d_vector)]
            if p_i.y >= p_i_next:
                intersects = self.__ray_intersects_side(point, p_i_next, p_i)
            else:
                intersects = self.__ray_intersects_side(point, p_i, p_i_next)
            if intersects:
                intersection_count += 1
        if intersection_count % 2 == 1:
            return True
        return False

    def __ray_intersects_side(self, ray_p, a_p, b_p):
        """ Inner method to determine whether a ray intersects a segment

        This method checks whether a horizpntal ray casted from a point
        intersects an input segment.

        :param ray_p: Point2D object of a point from which a ray
               casted
        :param a_p: Point2D object of a lower point of a segment
               (a_p.y =< b_p.y)
        :param b_p: Point2D object of a higher point of a segment

        :return: True - ray intersects a segment. False - otherwise.

        """

        

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

    @staticmethod
    def __verify_points(points):
        """ Make sure all items in a tuple/list are Point2D objects

        :param points - tuple to verify

        :return bool True - all the items in p_tuple are Point2D
                objects. False otherwise.

        """

        for p in points:
            if not isinstance(p, Point2D):
                return False
        return True
