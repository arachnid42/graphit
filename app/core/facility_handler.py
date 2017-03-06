from app.dstruct.facility import *
from app.dstruct.department import *
from app.parse.mp_parser import *
from datetime import datetime
import _pickle as pkl
import json
import os


class DBInaccessibleError(Exception):
    """ Custom exception

    Failed to fetch data from a DB

    """
    pass


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
        self.add_info = None  # distances and other extra info from factory_layout.json (list)

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
                try:
                    res = self.insert_all_transp_records(date_boundaries)
                except DBConnectionFailed:
                    raise DBInaccessibleError
                self.self_edges_weight = res[0]
                self.date_from = res[1]
                self.date_to = res[2]
                self.dump_facility(self.conf["facility_dump_path"])
        else:
            self.dump_facility(self.conf["facility_dump_path"])

    def populate_facility(self, path_to_source):
        """ Parses source file and populates facility class instance

        :param path_to_source - str path to a source JSON file

        """

        # load factory_layout.json
        with open(path_to_source) as f:
            src = json.load(f)
            self.add_info = src["distances"]  # it's a list

        # create graph nodes (initialize departments)
        for dep_src in src["departments"]:
            p_vect = []
            for point in dep_src["points"]:
                p_vect.append(Point2D(point[0], point[1]))
            dep = Department(dep_src["label"], *p_vect)
            self.facility.add_department(dep)

    def insert_all_transp_records(self, date_boundaries=None):
        """ Insert all transportation records from parser into facility instance

        :param date_boundaries - (<start>, <end>) list of string dates to filter on.
               Datetime format: "%Y-%m-%d %X" e.g. 2015-05-25 18:00:00

        :return: list [<int_self_edges_weight>, <str_lower_date>, <str_upper_date>]

        """

        mpp = MPParser(self.conf['server'], self.conf['db'], self.conf['uid'], self.conf['pass'],
                       self.conf['mp_query'], self.conf['peg_query'], debug=True)
        res = mpp.parse()  # get parsed transportation
        date_format = "%Y-%m-%d %X"
        self_edges_weight = 0
        date_from = datetime.strptime(date_boundaries[0], date_format) \
            if date_boundaries else datetime.strptime("9999-01-01 00:00:00", date_format)
        date_to = datetime.strptime(date_boundaries[1], date_format) \
            if date_boundaries else datetime.strptime("1002-01-01 00:00:00", date_format)

        # inserting transportation into facility
        for key in res:
            rec = res[key]

            # matching data date boundaries
            if not date_boundaries:
                d_f_cand = rec[2]
                d_t_cand = rec[2]
                if d_f_cand < date_from:
                    date_from = d_f_cand
                if d_t_cand > date_to:
                    date_to = d_t_cand

            # filter out data errors
            if not self.facility.get_department_by_label(rec[0]) or not self.facility.get_department_by_label(rec[1]):
                continue
            if date_boundaries and not datetime.strptime(date_boundaries[0], date_format) <= rec[2] \
                    <= datetime.strptime(date_boundaries[1], date_format):
                continue
            try:
                created_nodes = self.facility.add_transp_record(rec[0]+'.centroid', rec[1]+'.centroid', int(rec[3]))
                extra_data = self.find_distance_and_time_info(rec[0], rec[1])
                distance, time = extra_data if extra_data else [None, None]
                for node in created_nodes:
                    if len(node.info_dict) > 0:
                        continue
                    if distance:
                        node.add_info("distance", distance)
                    if time:
                        node.add_info("time", time)
            except SelfEdgesNotSupported:
                self_edges_weight += int(rec[3])

        return [self_edges_weight, date_from.strftime(date_format), date_to.strftime(date_format)]

    def find_distance_and_time_info(self, node_1, node_2):
        """ Derive information about distance and time of travel between departments from an add_info dict

        :param node_1: string department 1 label
        :param node_2: string department 2 label

        :return: list [distance, time] or None if no information found

        """

        # parse out information about distance and time
        if node_1 in self.add_info:
            if node_2 in self.add_info[node_1]:
                return self.add_info[node_1][node_2]
            else:
                return self.find_distance_and_time_info(node_2, node_1)
        return None


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