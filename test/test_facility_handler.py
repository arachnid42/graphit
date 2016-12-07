import unittest, os
from app.metec.facility_handler import FacilityHandler


class TestFacilityHandler(unittest.TestCase):

    def test_complex(self):
        """ Test the whole class by testing it's constructor (as it's tightly connected with other methods) """

        cached_file_path = "app/backup/facility.pkl"
        if os.path.isfile(cached_file_path):
            os.remove(cached_file_path)
        fh = FacilityHandler("app/metec/config.json")

        # this test is rather visual as it's hard to evaluate results before we'll see an actual visualization
