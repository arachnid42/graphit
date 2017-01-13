class NotNumericCoordinatesPassed(Exception):
    """ Custom exception

    Indicates about bas input arguments to a Point2D constructor.
    The only reason: x and y are not of float or int types (both
    must be of the same type).

    """
    pass


class Point2D(object):
    """ Self-descriptive class; 2D point with x and y coordinates """

    def __init__(self, x, y):
        """ Constructor for a 2D point

        :param x - float x coordinate of a point
        :param y - float y coordinate of a point

        """

        if not ((isinstance(x, int) or isinstance(x, float)) and (isinstance(y, int) or isinstance(y, float))):
            raise NotNumericCoordinatesPassed("x and y must be integers or floats!")

        self.x = float(x)
        self.y = float(y)

    def get_coords_list(self):
        """  """

        return [self.x, self.y]

    def __str__(self):
        return "Point(%f, %f)" % (self.x, self.y)
