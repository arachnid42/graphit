from app.core.facility_handler import *
from app.core.craft_optimization import *
from app.parse import *
from copy import deepcopy
import json


class JSONAssembler(object):
    """ Assembles visualization data JSON on request """

    def __init__(self, conf_path):
        """  """

        # init/restore Facility class
        fh = FacilityHandler(conf_path)
        self.facility = fh.facility
        self.viz_dict = {'facility': {}, "edges": []}
        self.viz_json_dump_path = fh.conf['viz_json_dump_path']

    def get_viz_json(self):
        """ """

        # stage 1: compose factory layout part
        for dep in self.facility.get_departments():
            self.viz_dict['facility'][dep.label] = {}
            self.viz_dict['facility'][dep.label]["boundaries"] = []
            self.viz_dict['facility'][dep.label]["points"] = {}

            # adding department boundaries
            for point in dep.point2d_vector:
                self.viz_dict['facility'][dep.label]["boundaries"].append(point.get_coords_list())

            # adding department inner points
            for p_name, p_coords in dep.vertices.items():
                self.viz_dict['facility'][dep.label]["points"][p_name] = p_coords.get_coords_list()

        # stage 2: compose edges part
        for edge in self.facility.d_graph.get_edges():
            if edge[0] == edge[1]:
                continue
            self.viz_dict['edges'].append([edge[0], edge[1], edge[2]])

        # backup json
        self.dump_to_file()

        return json.dumps(self.viz_dict)

    def dump_to_file(self):

        with open(self.viz_json_dump_path, 'w') as f:
            json.dump(self.viz_dict, f)


