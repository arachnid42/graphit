from app.dstruct.facility import *
from app.dstruct.department import *
from app.parse.mp_parser import *
from datetime import datetime
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

    def __init__(self, path_to_conf_file, facility_instance=None, force_rebuild=False, date_boundaries=None):
        """ Initialize facility

        It checks whether cached version of facility object exists
        in a system under /app/data/ and revovers it. If there is no
        cached version available, it pickups factory_layout.json from
        /app/data/, creates a facility object and dumps it locally under
        /app/data directory.

        :param path_to_conf_file - string path to a configuration JSON file
               that holds a path where to dump an object pickle
        :param facility_instance - Facility class instance to initialize with
        :param date_boundaries - (<start>, <end>) list of string dates to filter on.
               Datetime format: "%Y-%m-%d %X" e.g. 2015-05-25 18:00:00

        """

        self.facility = facility_instance

        # load configuration
        with open(path_to_conf_file) as f:
            self.conf = json.load(f)

        if not self.facility:
            if not date_boundaries and not force_rebuild and os.path.isfile(self.conf["facility_dump_path"]):
                with open(self.conf["facility_dump_path"], 'rb') as f:
                    self.facility = pkl.load(f)
            else:
                self.facility = Facility(self.conf["facility_boundaries"][0], self.conf["facility_boundaries"][1])
                self.populate_facility(self.conf["facility_source_path"])
                self.insert_all_transp_records(self.conf["masterplan_csv_path"], self.conf["peg_csv_path"],
                                               date_boundaries)
                self.dump_facility(self.conf["facility_dump_path"])
        else:
            self.dump_facility(self.conf["facility_dump_path"])

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

    def insert_all_transp_records(self, mp_csv_path, peg_csv_path, date_boundaries=None):
        """ Insert all transportation records from parser into facility instance

        :param mp_csv_path - string path to masterplan to init a parser
        :param peg_csv_path - string path to peg to init a parser
        :param date_boundaries - (<start>, <end>) list of string dates to filter on.
               Datetime format: "%Y-%m-%d %X" e.g. 2015-05-25 18:00:00

        """

        mpp = MPParser(mp_csv_path, peg_csv_path, debug=True)
        res = mpp.parse()  # get parsed transportation
        date_format = "%Y-%m-%d %X"

        s_edge_weight = 0
        # ##############################
        # str_tmp = ""
        # #############################

        # inserting transportation into facility
        for key in res:
            rec = res[key]
            # filter out data errors
            if str(rec[0]) in self.conf['error_dep_list'] or str(rec[1]) in self.conf['error_dep_list']:
                continue
            if date_boundaries and not datetime.strptime(date_boundaries[0], date_format) <= datetime.\
                    strptime(rec[2][:-4], date_format) <= datetime.strptime(date_boundaries[1], date_format):
                continue
            try:
                self.facility.add_transp_record(rec[0]+'.centroid', rec[1]+'.centroid', int(rec[3]))
            except SelfEdgesNotSupported:
                # str_tmp += "Self-edge: %s, weight %i, opcodes: %s to %s\n" % (rec[0], rec[3], key[0], key[1])
                s_edge_weight += rec[3]

        # with open("app/backup/self-edges.txt", "w") as f:
        #     f.write(str_tmp)

        print("Self-edges total weight: %i" % s_edge_weight)

    def dump_facility(self, path):
        """ Save facility class as object data persistence

        :param path: string where to store backup

        :return: True - saved successfully.
                 False - otherwise.

        """

        try:
            with open(path, "wb") as f:
                pkl.dump(self.facility, f, -1)
            return True
        except:  # TODO: narrow exceptions
            return False