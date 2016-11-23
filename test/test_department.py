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
        del dep

        dep = Department("Lviv Coffee Blasters Dep", Point2D(0, 0), Point2D(2, 0), Point2D(2, 2), Point2D(4, 4),
                         Point2D(0, 4))
        self.assertEqual(dep.area, 10)

    def test_calculate_centroid(self):
        """ Test centroid calculation for a department object """

        dep = Department("Ultrasonic Eva Squeezers Factory", Point2D(0, 0), Point2D(2, 0), Point2D(2, 2), Point2D(0, 2))
        self.assertEqual(dep.centroid.x, 1)
        self.assertEqual(dep.centroid.y, 1)
        del dep

        dep = Department("Lviv Coffee Blasters Dep", Point2D(0, 0), Point2D(2, 0), Point2D(2, 2), Point2D(4, 4),
                         Point2D(0, 4))
        self.assertEqual(dep.centroid.x, 4 / 3)
        self.assertEqual(dep.centroid.y, 34 / 15)

    def test_add_vertices(self):
        """ Test adding vertices to be used in a graph to department object """

        # trivial polygon
        dep = Department("Ultrasonic Eva Squeezers Factory", Point2D(0, 0), Point2D(2, 0), Point2D(2, 2), Point2D(0, 2))
        self.assertRaises(ValueExists, dep.add_vertices, {"centroid2": Point2D(1, 1)})
        self.assertRaises(PointNotInPolygon, dep.add_vertices, {"point": Point2D(3, 1)})
        self.assertRaises(PointNotInPolygon, dep.add_vertices, {"point": Point2D(0, 1)})
        self.assertRaises(PointNotInPolygon, dep.add_vertices, {"point": Point2D(2.1, 1)})
        dep.add_vertices({"point": Point2D(1, 1.5), "point2": Point2D(1.5, 1.5)})
        self.assertEqual(dep.get_vertices_count(), 3)
        del dep

        # not so trivial example
        dep = Department("Lviv Coffee Blasters Dep", Point2D(0, 0), Point2D(2, 0), Point2D(2, 2), Point2D(4, 4),
                         Point2D(0, 4))
        self.assertRaises(ValueExists, dep.add_vertices, {"centroid2": dep.centroid})
        x = dep.centroid.x
        y = dep.centroid.y
        self.assertRaises(ValueExists, dep.add_vertices, {"centroid2": Point2D(x, y)})
        self.assertRaises(PointNotInPolygon, dep.add_vertices, {"centroid2": Point2D(3, 2)})
        self.assertRaises(PointNotInPolygon, dep.add_vertices, {"centroid2": Point2D(4, 5)})
        self.assertRaises(PointNotInPolygon, dep.add_vertices, {"centroid2": Point2D(0, 5)})
        self.assertRaises(PointNotInPolygon, dep.add_vertices, {"centroid2": Point2D(3, 1)})
        dep.add_vertices({"point": Point2D(1, 1.5), "point2": Point2D(1.5, 1.5), "point3": Point2D(3.95, 3.99)})
        self.assertEqual(dep.get_vertices_count(), 4)
        self.assertRaises(ValueExists, dep.add_vertices, {"point2": Point2D(1, 1)})
