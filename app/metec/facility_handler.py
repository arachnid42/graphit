from app.dstruct.facility import *
from app.dstruct.department import *
import _pickle as pkl
import json
import os


class FacilityHandler(object):
    """ High level handler for a Facility class

    It saves, caches and prepares all the data
    that is needed for a visualization on a client
    side.

    NOTE: it's a bare back class that doesn't verify
    anything before actually doing things, so it would
    fail on incorrect input etc. (which was done deliberately)

    """

    def __init__(self, path_to_conf_file):
        """ Initialize facility

        It checks whether cached version of facility object exists
        in a system under /app/data/ and revovers it. If there is no
        cached version available, it pickups factory_layout.json from
        /app/data/, creates a facility object and dumps it locally under
        /app/data directory.

        :param path_to_conf_file - string path to a configuration JSON file
               that holds a path where to dump an object pickle

        """

        self.facility = None

        # load configuration
        with open(path_to_conf_file) as f:
            conf = json.load(f)

        if os.path.isfile(conf["facility_dump_path"]):
            with open(conf["facility_dump_path"], 'rb') as f:
                self.facility = pkl.load(f)
        else:
            self.facility = Facility(conf["facility_boundaries"][0], conf["facility_boundaries"][1])
            self.populate_facility(conf["facility_source_path"])
            self.dump_facility(conf["facility_dump_path"])

    def populate_facility(self, path_to_source):
        """ Parses source file and populates facility class instance

        :param path_to_source - str path to a source JSON file

        """

        with open(path_to_source) as f:
            src = json.load(f)

        for dep_src in src["departments"]:
            p_vect = []
            for point in dep_src["points"]:
                p_vect.append(Point2D(point[0], point[1]))
            dep = Department(dep_src["label"], *p_vect)
            self.facility.add_department(dep)

    def dump_facility(self, path):
        """ Save facility class as object data persistence

        :param path: string where to store backup

        :return: True - saved successfully.
                 False - otherwise.

        """

        with open(path, "wb") as f:
            pkl.dump(self.facility, f, -1)
