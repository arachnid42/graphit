from app.dstruct.point2d import *
from math import fabs
from copy import copy


class BadInitParameters(Exception):
    """ Custom exception

    Indicates about bad passed in parameters to a
    Department constructor (__init__()). Typical
    reasons are less then 3 points passed or points
    passed are not Point2D instances.

    """
    pass


class IllegalLabel(Exception):
    """ Custom exception

    Illegal label passed in (probably with "." in it)

    """


class NotPoint2DObject(Exception):
    """ Custom exception

    Indicates about the fact that passed in parameters
    are not instances of Point2D class

    """


class ValueExists(Exception):
    """ Custom exception

    Value for a particular key exists in self.vertices or
    the same value is stored with a different key

    """


class PointNotInPolygon(Exception):
    """ Custom exception

    Point to insert not belongs to a polygon boundary so
    can't be inserted

    """


class Department(object):
    def __init__(self, label, *arg):
        """ Constructor

        :param label - String label of a department
               without "." in it (preferably without
               spaces also but it's not mandatory)
        :param *arg - tuple of Point2D objects in an
               ordered way, i.e. to represent a polygon
               points one by one counter-clockwise.

        """

        if "." in label:
            raise IllegalLabel
        if len(arg) > 2 and self.__verify_points(arg):
            self.label = label
            self.point2d_vector = arg  # physical measurements of department boundaries
            self.area = self.calculate_area()
            self.centroid = self.calculate_centroid()
            self.vertices = {"centroid": self.centroid}  # all vertices to be used as graph points
        else:
            raise BadInitParameters("passed init parameters are not acceptable!")

    def get_vertices_count(self):
        return len(self.vertices)

    def add_vertices(self, vertices):
        """ Add vertices to be used as graph points

        :param vertices: dictionary of keys that are unique
               labels of points and values are Point2D objects.

        """

        if not self.__verify_points(vertices.values()):
            raise NotPoint2DObject
        else:
            for vertex_label in vertices:
                if "." in vertex_label:
                    raise IllegalLabel
                if vertex_label not in self.vertices.keys() and \
                        not self.find_point_by_coordinates(vertices[vertex_label]):
                    if self.__fits_boundary(vertices[vertex_label]):
                        self.vertices[vertex_label] = vertices[vertex_label]
                    else:
                        raise PointNotInPolygon
                else:
                    raise ValueExists

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
            if p_i.y >= p_i_next.y:
                intersects = self.__ray_intersects_side(point, p_i_next, p_i)
            else:
                intersects = self.__ray_intersects_side(point, p_i, p_i_next)
            if intersects:
                intersection_count += 1
        if intersection_count % 2 == 1:
            return True
        return False

    @staticmethod
    def __ray_intersects_side(p_ray, p_a, p_b):
        """ Inner method to determine whether a ray intersects a segment

        This method checks whether a horizontal ray casted from a point
        intersects an input segment.

        :param p_ray: Point2D object of a point from which a ray
               casted
        :param p_a: Point2D object of a lower point of a segment
               (p_a.y =< p_b.y)
        :param p_b: Point2D object of a higher point of a segment

        :return: True - ray intersects a segment. False - otherwise.

        """

        p_ray = copy(p_ray)  # enforce not changing a passed in object
        if p_ray.y == p_a.y or p_ray.y == p_b.y:
            p_ray.y += 0.0000000000001  # deal with ray-on-vertex issue
        if p_ray.y < p_a.y or p_ray.y > p_b.y:  # point is above or below a segment
            return False
        elif p_ray.x > max(p_a.y, p_b.y):  # point is out of a segment box
            return False
        else:
            if p_ray.x < min(p_a.x, p_b.x):  # point is to the left of a segment (ray is ok)
                return True
            else:
                if p_a.x != p_b.x:  # tg of a segment
                    tg_ab = (p_b.y - p_a.y) / (p_b.x - p_a.x)
                else:
                    tg_ab = float("inf")
                if p_a.x != p_ray.x:  # tg of a ray point
                    tg_raya = (p_ray.y - p_a.y) / (p_ray.x - p_a.x)
                else:
                    tg_raya = float("inf")
                if tg_raya >= tg_ab:  # point is to the left of a segment - ray is ok
                    return True
                return False

    def calculate_centroid(self):
        """ Calculate a centroid (center) point of the department

        :return Point2D that holds a center point of the department

        """

        c_x = c_y = 0
        for p_ind in range(0, len(self.point2d_vector)):
            p_i = self.point2d_vector[p_ind]
            p_i_next = self.point2d_vector[(p_ind + 1) % len(self.point2d_vector)]
            fact = p_i.x * p_i_next.y - p_i_next.x * p_i.y
            c_x += (p_i.x + p_i_next.x) * fact
            c_y += (p_i.y + p_i_next.y) * fact

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

        return d_area / 2

    def __str__(self):
        strg = "Department: %s\n-------------------------\n" % self.label
        for point in self.point2d_vector:
            strg += str(point) + "\n"

        return strg + "\n"

    def find_point_by_coordinates(self, point):
        """ Find any points in self.vertices that has the same coordinates as a given one

        :param point - Point2D object to seek in self.vertices

        :return: string key in self.vertices if point was found.
                 None otherwise.

        """

        for k, v in self.vertices.items():
            if v.x == point.x and v.y == point.y:
                return k
        return None

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
