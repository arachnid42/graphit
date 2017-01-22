from app.core.facility_handler import *
import json


class JSONAssembler(object):
    """ Assembles visualization data JSON on request """

    def __init__(self, conf_path, force_rebuild=False, date_boundaries=None):
        """ Init method

        Fetch cached facility version and initialize
        all the fields necessary to build and cache
        visualization JSON.

        :param conf_path: string path to configuration file
        :param force_rebuild - boolean flag to force rebuild
               both facility instance and JSON file. In other
               words - ignore cached version and override them

        """

        # assign rebuild flag
        self.force_rebuild = force_rebuild

        # init/restore Facility class
        self.fh = FacilityHandler(conf_path, force_rebuild=self.force_rebuild, date_boundaries=date_boundaries)
        self.facility = self.fh.facility
        self.viz_json_dump_path = self.fh.conf['viz_json_dump_path']

    def get_viz_json(self):
        """ Assemble visualization JSON or get a cached version

        :return string JSON assembled

        """

        if not self.force_rebuild and os.path.isfile(self.viz_json_dump_path):
            return self.get_cached_json()
        else:

            # clear previously JSON dict
            viz_dict = self.get_json_base()

            # stage 1: compose factory layout part
            for dep in self.facility.get_departments():
                viz_dict['facility'][dep.label] = {}
                viz_dict['facility'][dep.label]["boundaries"] = []
                viz_dict['facility'][dep.label]["points"] = {}

                # adding department boundaries
                for point in dep.point2d_vector:
                    viz_dict['facility'][dep.label]["boundaries"].append(point.get_coords_list())

                # adding department inner points
                for p_name, p_coords in dep.vertices.items():
                    viz_dict['facility'][dep.label]["points"][p_name] = p_coords.get_coords_list()

            # stage 2: compose edges part
            for edge in self.facility.d_graph.get_edges():
                viz_dict['edges'].append(edge)

            # stage 3: insert additional information
            viz_dict['self_edges_total_weight'] = self.fh.self_edges_weight
            viz_dict['date_boundaries'] = [self.fh.date_from, self.fh.date_to]

            # get nodes involved in a net
            involved_nodes_count = 0
            for edge_list in self.facility.d_graph.mapper.values():
                if edge_list:
                    involved_nodes_count += 1

            # append result into JSON
            viz_dict['involved_edges_count'] = involved_nodes_count

            # backup json
            self.dump_to_file(viz_dict)

            return json.dumps(viz_dict)

    @staticmethod
    def get_json_base():
        """ Get base JSON to append to

        :return: python dictionary instance

        """

        return {'facility': {}, "edges": []}

    def get_cached_json(self):
        """ Pick up JSON from a system and return it """

        with open(self.viz_json_dump_path, 'rb') as f:
            return f.read()

    def dump_to_file(self, viz_dict):
        """ Dump visualization JSON data """

        # retrieve base dump directory from config
        base_dir = '/'.join(self.viz_json_dump_path.split("/")[:-1]) + "/"

        # check whether base dir exists
        # and if not create it
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)

        # dump data
        with open(self.viz_json_dump_path, 'w') as f:
            json.dump(viz_dict, f)
