from random import sample, random
from math import exp
from copy import deepcopy


class CRAFTOptimization(object):

    def __init__(self, facility_state):
        self.facility_state = facility_state

    def craft_layout_optimization(self):
        """  """

        # calculate initial cost
        best_cost = self.calculate_craft_cost(self.facility_state)

        # get amount of departments
        dep_count = len(self.facility_state.d_graph.mapper)


        iter = 1
        costs = [best_cost]

        # init temp
        temp = 10000
        cool = 0.03

        # get test facility instance
        next_facility_state = deepcopy(self.facility_state)

        while temp > 1:

            next_facility_state.delete_transp_records()

            # permute labels
            dep_labels = next_facility_state.d_graph.get_nodes_labels(sort=True)
            indices = sample(range(0, dep_count), 2)
            # dep_labels_shuffled = sample(deepcopy(dep_labels), dep_count)
            #
            # for i in range(dep_count):
            #     node_a_label = dep_labels[i]
            #     node_b_label = dep_labels_shuffled[i]
            #     next_facility_state.d_graph.find_vertex_node_by_label(node_a_label).set_label(node_b_label)
            #     next_facility_state.d_graph.find_vertex_node_by_label(node_b_label).set_label(node_a_label)

            node_a_label = dep_labels[indices[0]]
            node_b_label = dep_labels[indices[1]]
            next_facility_state.d_graph.find_vertex_node_by_label(node_a_label).set_label(node_b_label)
            next_facility_state.d_graph.find_vertex_node_by_label(node_b_label).set_label(node_a_label)

            # reinsert edges add_transp_record(self, src_label, dest_label, quant, time)
            for node, edge_nodes in deepcopy(self.facility_state.d_graph.mapper).items():
                for edge_node in edge_nodes:
                    next_facility_state.add_transp_record(node.get_label(), edge_node.vertex_node.get_label(),
                                                          edge_node.weight, "2015-05-25 18:00:00")

            next_cost = self.calculate_craft_cost(deepcopy(next_facility_state))

            if self.acceptance_func(best_cost, next_cost, temp) > random():
                best_cost = next_cost
                self.facility_state = deepcopy(next_facility_state)

            print(best_cost)
            print(next_cost)
            if next_cost not in costs:
                costs.append(next_cost)
            print(len(costs))
            print('-----')

            temp *= 1-cool

        return self.facility_state

    @staticmethod
    def acceptance_func(best_cost, current_cost, temp):
        """"""

        if current_cost < best_cost:
            return 1
        else:
            return exp((best_cost - current_cost)/temp)

    @staticmethod
    def calculate_craft_cost(facility_state):
        d_matrix = facility_state.d_graph.get_distance_matrix()
        c_matrix = facility_state.d_graph.get_cost_matrix()
        f_matrix = facility_state.d_graph.get_flow_matrix()
        cost = 0

        dep_labels = facility_state.d_graph.get_nodes_labels(sort=True)
        print(matrix_to_string(dep_labels, d_matrix))
        print(matrix_to_string(dep_labels, f_matrix))
        exit(0)

        for i in range(facility_state.d_graph.get_vertices_count()):
            for j in range(i, facility_state.d_graph.get_vertices_count()):
                cost += d_matrix[i][j] * c_matrix[i][j] * f_matrix[i][j]

        return cost

def matrix_to_string(key_list, matrix):
    """ Form a string representation of an adjacency matrix of the graph

    :param key_list - list of sorted vertex labels of the graph
    :param matrix - numpy matrix that holds adjacancy matrix of
           the graph object.

    :return: string adjacency matrix representation with labels

    """

    strg = "  "
    for label in key_list:
        strg += "%s " % label
    strg += "\n"

    for row, i in zip(matrix, key_list):
        strg += "%s " % i
        for item in row:
            strg += "%s " % int(item)
        strg += "\n"

    return strg
