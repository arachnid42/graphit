import unittest
from app.dstruct.point2d import *


class TestPoint2D(unittest.TestCase):
    """ Unit tests for app/dstruct/point2d.py module """

    def test_point_init(self):
        self.assertRaises(NotNumericCoordinatesPassed, Point2D, "2", "2")
        self.assertRaises(NotNumericCoordinatesPassed, Point2D, "2", "f")
        self.assertRaises(NotNumericCoordinatesPassed, Point2D, "f", "2")
        self.assertRaises(NotNumericCoordinatesPassed, Point2D, "f", "f")
        self.assertRaises(NotNumericCoordinatesPassed, Point2D, "2", 2)
        self.assertRaises(NotNumericCoordinatesPassed, Point2D, 2, "2")
        self.assertRaises(NotNumericCoordinatesPassed, Point2D, 2, None)
