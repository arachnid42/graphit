import unittest
from app.dstruct.department import *


class TestDepartment(unittest.TestCase):

    def test_department_init(self):
        """ Test the initialization of department instance """

        self.assertRaises(BadInitParameters, Department, "Nodal Brainwashers Dep", Point2D(2, 3), Point2D(2, 4))
        self.assertRaises(BadInitParameters, Department, "Nodal Brainwashers Dep", Point2D(2, 3), "Unacceptable",
                          Point2D(2, 4))
        dep = Department("Nodal Brainwashers Dep 2.0", Point2D(0, 0), Point2D(2, 2), Point2D(0, 2))
        self.assertEqual(len(dep.point2d_vector), 3)

    def test_calculate_area(self):
        """ Test area calculation for a department object """

        dep = Department("Nodal Brainwashers Dep 3.0", Point2D(0, 0), Point2D(2, 2), Point2D(0, 2))
        self.assertEqual(dep.area, 2)
        dep2 = Department("Lviv Coffee Blasters Dep", Point2D(0, 0), Point2D(2, 0), Point2D(2, 2), Point2D(4, 4),
                          Point2D(0, 4))
        self.assertEqual(dep2.area, 10)

    def test_calculate_centroid(self):
        """ Test centroid calculation for a department object """

        dep = Department("Ultrasonic Eva Squeezers Factory", Point2D(0, 0), Point2D(2, 0), Point2D(2, 2), Point2D(0, 2))
        self.assertEqual(dep.centroid.x, 1)
        self.assertEqual(dep.centroid.y, 1)
        dep2 = Department("Lviv Coffee Blasters Dep", Point2D(0, 0), Point2D(2, 0), Point2D(2, 2), Point2D(4, 4),
                          Point2D(0, 4))
        self.assertEqual(dep2.centroid.x, 4/3)
        self.assertEqual(dep2.centroid.y, 34/15)

    def test_add_vertices(self):
        """ Test adding vertices to be used in a graph to department object """

