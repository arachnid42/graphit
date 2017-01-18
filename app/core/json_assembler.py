from app.core.facility_handler import *
import json


class JSONAssembler(object):
    """ Assembles visualization data JSON on request """

    def __init__(self, conf_path, force_rebuild=False):
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
        fh = FacilityHandler(conf_path, force_rebuild=self.force_rebuild)
        self.facility = fh.facility
        self.viz_dict = {'facility': {}, "edges": []}
        self.viz_json_dump_path = fh.conf['viz_json_dump_path']

    def get_viz_json(self):
        """ Assemble visualization JSON or get a cached version

        :return string JSON assembled

        """

        if not self.force_rebuild and os.path.isfile(self.viz_json_dump_path):
            with open(self.viz_json_dump_path, 'rb') as f:
                return f.readlines()
        else:
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
            edges_parsed = []
            for edge in self.facility.d_graph.get_edges():
                if not self.__check_mirror_edges(edge, edges_parsed):
                    self.viz_dict['edges'].append(edge)
                edges_parsed.append(edge)

            # backup json
            self.dump_to_file()

            return json.dumps(self.viz_dict)

    def dump_to_file(self):
        """ Dump visualization JSON data """

        with open(self.viz_json_dump_path, 'w') as f:
            json.dump(self.viz_dict, f)

    @staticmethod
    def __check_mirror_edges(edge1, edge_lst):
        """ Check whether edge list passed holds a mirror of an edge1 passed

        Example: edge A -> B is a mirror of B -> A for undirected graph

        :param edge1 - list [<src_node_label>, <dest_node_label>, <edge_weight>]
               of the first edge to check
        :param edge_lst - list of edges like above to find a mirror in it

        :return boolean True if edge1 mirror was in edge_lst. False otherwise.

        """

        for edge in edge_lst:
            if edge[0] == edge1[1] and edge[1] == edge1[0]:
                return True
        return False



