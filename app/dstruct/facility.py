from app.dstruct.graph import Graph
from app.dstruct.department import Department


class NonpositiveMaxCoordinates(Exception):
    pass


class WrongTypeOfMaxCoordinates(Exception):
    pass


class Facility(object):
    def __init__(self, max_x, max_y):
        if (isinstance(max_x, int) and isinstance(max_y, int)) or \
                (isinstance(max_x, float) and isinstance(max_y, float)):
            if max_x > 0 and max_y > 0:
                self.max_x = max_x
                self.max_y = max_y
                self.departments = []
                self.graph = Graph(coordinates=True, explicit_weight=True, aggregate_weight=True)
            else:
                raise NonpositiveMaxCoordinates("facility max_x and max_y must be positive!")
        else:
            raise WrongTypeOfMaxCoordinates("facility max_x and max_y must be both integers or both floats!")

