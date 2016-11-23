import unittest
from app.dstruct.facility import *
from app.dstruct.department import *


class TestFacility(unittest.TestCase):

    def test_facility_init(self):
        """ Test initialization of a facility instance """

        self.assertRaises(WrongTypeOfMaxCoordinates, Facility, "one", "dozen")
        self.assertRaises(WrongTypeOfMaxCoordinates, Facility, "one", 10)
        self.assertRaises(WrongTypeOfMaxCoordinates, Facility, 10, "dozen")

        self.assertRaises(NonpositiveMaxCoordinates, Facility, -1, -10)
        self.assertRaises(NonpositiveMaxCoordinates, Facility, 1, -10)
        self.assertRaises(NonpositiveMaxCoordinates, Facility, -1, 10)

    def test_add_department(self):
        """ Test department addition to a facility object instance """

        fac = Facility(100, 100)
        dep = Department("Nodal Brainwashers Dep 20", Point2D(0, 0), Point2D(2, 2), Point2D(0, 2))
        dep.add_vertices({"point": Point2D(1, 1.5), "point2": Point2D(1.5, 1.5)})
        fac.add_department(dep)  # deeper tests are redundant as graph was tested separately
        # TODO: finish

    def test_add_transp_record(self):
        pass
        # TODO: finish